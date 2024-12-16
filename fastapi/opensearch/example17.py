@app.post("/data")
async def handle_data(data: DataModel, user: str):
    try:
        # Generate doc_id based on unique fields
        doc_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{data.name}-{data.username}-{data.address}-{data.language}"))
        existing_doc = repository.get_data(DATA_INDEX, doc_id)

        # Prepare the data for insertion or update, using model_dump to avoid deprecation warning
        data_dict = data.model_dump(exclude_unset=True)  # This will exclude any unset values (fields not in the request)

        if existing_doc.get("found"):
            action = "update"
            # Preserve the existing create_time, set a new update_time
            create_time = existing_doc["_source"].get("create_time", datetime.utcnow().isoformat())
            update_time = datetime.utcnow()  # Update this for the latest change

            # Only update the fields present in the request
            data_dict["update_time"] = update_time.isoformat()

            # Update the data
            repository.update_data(DATA_INDEX, doc_id, data_dict)

        else:
            action = "insert"
            create_time = datetime.utcnow()  # Set creation time for new records
            update_time = create_time        # Same as creation time for a new record

            # Insert the new data along with time stamps
            data_dict.update({
                "create_time": create_time.isoformat(),
                "update_time": update_time.isoformat()
            })
            repository.insert_data(DATA_INDEX, doc_id, data_dict)

        # Log the action
        log_entry = LogModel(
            user=user,
            action=action,
            create_time=create_time,
            update_time=update_time
        )
        repository.insert_data(LOGS_INDEX, None, log_entry.dict())

        return {"status": "success", "action": action, "id": doc_id}

    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

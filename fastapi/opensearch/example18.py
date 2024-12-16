@app.post("/data")
async def handle_data(data: DataModel, user: str):
    try:
        # Generate doc_id based on unique fields
        doc_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{data.name}-{data.username}"))  # Only use the fields you want for doc_id
        existing_doc = repository.get_data(DATA_INDEX, doc_id)

        # Manually filter the data to include only the fields you want in the index
        data_dict = data.model_dump(exclude_unset=True)  # Exclude fields that are not set in the request

        # Only keep required fields, here assuming only name and username are required
        allowed_fields = ['name', 'username']
        filtered_data = {key: value for key, value in data_dict.items() if key in allowed_fields}

        if existing_doc.get("found"):
            action = "update"
            # Preserve the existing create_time, set a new update_time
            create_time = existing_doc["_source"].get("create_time", datetime.utcnow().isoformat())
            update_time = datetime.utcnow()  # Update this for the latest change

            # Add/update the time fields
            filtered_data["update_time"] = update_time.isoformat()

            # Update the document in OpenSearch with filtered fields
            repository.update_data(DATA_INDEX, doc_id, filtered_data)

        else:
            action = "insert"
            create_time = datetime.utcnow()  # Set creation time for new records
            update_time = create_time        # Same as creation time for a new record

            # Insert the new data along with time stamps
            filtered_data.update({
                "create_time": create_time.isoformat(),
                "update_time": update_time.isoformat()
            })
            repository.insert_data(DATA_INDEX, doc_id, filtered_data)

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

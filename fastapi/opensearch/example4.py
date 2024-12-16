@app.post("/data")
async def handle_data(data: DataModel, user: str):
    try:
        # Generate a unique ID based on content for deduplication
        doc_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{data.name}-{data.username}-{data.address}-{data.language}"))

        existing_doc = client.get(index=DATA_INDEX, id=doc_id, ignore=[404])

        if existing_doc.get("found"):
            action = "update"
            client.update(
                index=DATA_INDEX,
                id=doc_id,
                body={"doc": data.dict()}
            )
        else:
            action = "insert"
            client.index(
                index=DATA_INDEX,
                id=doc_id,
                body=data.dict()
            )

        # Log the action
        log_entry = LogModel(user=user, action=action, timestamp=datetime.utcnow())
        client.index(
            index=LOGS_INDEX,
            body=log_entry.dict()
        )

        return {"status": "success", "action": action, "id": doc_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

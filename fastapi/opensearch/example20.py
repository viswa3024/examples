from fastapi import FastAPI, HTTPException
from repository import OpenSearchRepository
from client import client
from data_model import DataModel
from log_model import LogModel
import uuid
from datetime import datetime

app = FastAPI()

# Repository instance
repository = OpenSearchRepository(client)

# Index names
DATA_INDEX = "opensearch-create-data-index"
LOGS_INDEX = "opensearch-create-logs-index"

# Existing handle_data method

@app.post("/data")
async def handle_data(data: DataModel, user: str):
    try:
        doc_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{data.name}-{data.username}"))
        existing_doc = repository.get_data(DATA_INDEX, doc_id)

        # Filter the fields to include only the necessary ones
        data_dict = data.model_dump(exclude_unset=True)  # Exclude unset fields
        allowed_fields = ['name', 'username']
        filtered_data = {key: value for key, value in data_dict.items() if key in allowed_fields}

        # Add time fields
        if existing_doc.get("found"):
            action = "update"
            create_time = existing_doc["_source"].get("create_time", datetime.utcnow().isoformat())
            update_time = datetime.utcnow()
            filtered_data["update_time"] = update_time.isoformat()
        else:
            action = "insert"
            create_time = datetime.utcnow()
            update_time = create_time
            filtered_data.update({
                "create_time": create_time.isoformat(),
                "update_time": update_time.isoformat()
            })

        # Insert or update the document
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

# New API to delete a document by ID
@app.delete("/data/{doc_id}")
async def delete_data(doc_id: str):
    try:
        # Check if document exists
        existing_doc = repository.get_data(DATA_INDEX, doc_id)
        if not existing_doc.get("found"):
            raise HTTPException(status_code=404, detail="Document not found")

        # Delete the document by ID
        repository.client.delete(index=DATA_INDEX, id=doc_id)

        # Log the deletion action
        log_entry = LogModel(
            user="system",  # You can use a default system user or pass a user parameter if needed
            action="delete",
            create_time=datetime.utcnow(),
            update_time=datetime.utcnow()
        )
        repository.insert_data(LOGS_INDEX, None, log_entry.dict())

        return {"status": "success", "action": "delete", "id": doc_id}

    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

# New API to delete an entire index
@app.delete("/index/{index_name}")
async def delete_index(index_name: str):
    try:
        # Check if the index exists
        if not repository.client.indices.exists(index=index_name):
            raise HTTPException(status_code=404, detail="Index not found")

        # Delete the index
        repository.client.indices.delete(index=index_name)

        return {"status": "success", "action": "delete index", "index": index_name}

    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

# New API to get all indices (useful for checking)
@app.get("/indices")
async def get_indices():
    try:
        indices = repository.client.cat.indices(format="json")
        return {"indices": indices}

    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))



=====================

Delete Document by ID

DELETE /<index_name>/_doc/<doc_id>

DELETE /opensearch-create-data-index/_doc/123


Delete Entire Index

DELETE /<index_name>

DELETE /opensearch-create-data-index

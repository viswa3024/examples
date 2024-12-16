# Required Imports
from fastapi import FastAPI, HTTPException, Query
from opensearchpy import OpenSearch, RequestsHttpConnection
from datetime import datetime
import uuid
import os
from pydantic import BaseModel
from typing import Optional

# FastAPI App
app = FastAPI()

# OpenSearch Client Setup
OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST", "localhost")
OPENSEARCH_PORT = int(os.getenv("OPENSEARCH_PORT", 9200))
client = OpenSearch(
    hosts=[{"host": OPENSEARCH_HOST, "port": OPENSEARCH_PORT}],
    http_auth=(os.getenv("OPENSEARCH_USER", "admin"), os.getenv("OPENSEARCH_PASSWORD", "admin")),
    use_ssl=False,
    verify_certs=False,
    connection_class=RequestsHttpConnection,
)

# Index Names
DATA_INDEX = "opensearch-data-index"
LOGS_INDEX = "opensearch-logs-index"

# Data Model
class DataModel(BaseModel):
    name: str
    username: str
    address: Optional[str] = None
    language: Optional[str] = None
    region: Optional[str] = None
    gender: Optional[str] = None

# Log Model
class LogModel(BaseModel):
    user: str
    action: str
    create_time: str
    update_time: str

# Repository Layer
class OpenSearchRepository:
    def __init__(self, client):
        self.client = client

    def get_document(self, index: str, doc_id: str):
        try:
            return self.client.get(index=index, id=doc_id, ignore=[404])
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching document: {str(e)}")

    def insert_or_update_document(self, index: str, doc_id: str, data: dict):
        try:
            existing_doc = self.get_document(index, doc_id)

            if existing_doc.get("found"):
                # Update existing document
                self.client.update(
                    index=index, id=doc_id, body={"doc": data}
                )
            else:
                # Insert new document
                self.client.index(index=index, id=doc_id, body=data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error inserting/updating document: {str(e)}")

    def insert_log(self, index: str, log_data: dict):
        try:
            self.client.index(index=index, body=log_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error inserting log: {str(e)}")

# Initialize Repository
repository = OpenSearchRepository(client)

# API Endpoints
@app.post("/data")
async def handle_data(data: DataModel, user: str = Query(...)):
    """
    API to insert or update data in OpenSearch and log the action.
    """
    try:
        # Generate a unique ID for deduplication
        doc_id = str(
            uuid.uuid5(
                uuid.NAMESPACE_DNS, f"{data.name}-{data.username}-{data.address}-{data.language}"
            )
        )

        # Prepare timestamps
        create_time = datetime.utcnow().isoformat()
        update_time = datetime.utcnow().isoformat()

        # Check if document exists and preserve create_time
        existing_doc = repository.get_document(DATA_INDEX, doc_id)

        if existing_doc.get("found"):
            action = "update"
            create_time = existing_doc["_source"].get("create_time", create_time)
            repository.insert_or_update_document(
                DATA_INDEX, doc_id, {**data.dict(), "create_time": create_time, "update_time": update_time}
            )
        else:
            action = "insert"
            repository.insert_or_update_document(
                DATA_INDEX, doc_id, {**data.dict(), "create_time": create_time, "update_time": update_time}
            )

        # Log the action
        log_entry = LogModel(
            user=user, action=action, create_time=create_time, update_time=update_time
        )
        repository.insert_log(LOGS_INDEX, log_entry.dict())

        return {"status": "success", "action": action, "id": doc_id}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/logs")
async def get_logs(query: dict):
    """
    Generic API to search logs based on a given query.
    """
    try:
        response = client.search(index=LOGS_INDEX, body=query)
        return [hit["_source"] for hit in response["hits"]["hits"]]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching logs: {str(e)}")

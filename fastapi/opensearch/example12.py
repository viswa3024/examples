# client.py
from opensearchpy import OpenSearch, RequestsHttpConnection
import os

class OpenSearchClient:
    def __init__(self):
        self.client = OpenSearch(
            hosts=[
                {"host": os.getenv("OPENSEARCH_HOST", "localhost"), "port": int(os.getenv("OPENSEARCH_PORT", 9200))}
            ],
            http_auth=(
                os.getenv("OPENSEARCH_USER", "admin"), 
                os.getenv("OPENSEARCH_PASSWORD", "admin")
            ),
            use_ssl=False,
            verify_certs=False,
            connection_class=RequestsHttpConnection,
        )

    def get_client(self):
        return self.client


# repository.py
from datetime import datetime
from typing import Optional

class Repository:
    def __init__(self, client):
        self.client = client

    def insert_data(self, index: str, doc_id: Optional[str], data: dict) -> None:
        """
        Inserts a new document into the specified OpenSearch index.
        """
        self.client.index(
            index=index,
            id=doc_id,
            body=data
        )

    def update_data(self, index: str, doc_id: str, data: dict) -> None:
        """
        Updates an existing document in the specified OpenSearch index.
        """
        self.client.update(
            index=index,
            id=doc_id,
            body={"doc": data}
        )

    def insert_log(self, index: str, log_entry: dict) -> None:
        """
        Inserts a log entry into the logs index.
        """
        self.insert_data(index=index, doc_id=None, data=log_entry)


# main.py
from fastapi import FastAPI, HTTPException
from uuid import uuid5, NAMESPACE_DNS
from datetime import datetime
from pydantic import BaseModel
from client import OpenSearchClient
from repository import Repository

# Pydantic models
class DataModel(BaseModel):
    name: str
    username: str
    address: str
    language: str
    region: str

class LogModel(BaseModel):
    user: str
    action: str
    create_time: datetime
    update_time: datetime

# FastAPI app
app = FastAPI()

# OpenSearch and repository initialization
client = OpenSearchClient().get_client()
repository = Repository(client=client)

# Index names
DATA_INDEX = "opensearch-create-data-index"
LOGS_INDEX = "opensearch-create-logs-index"

@app.post("/data")
async def handle_data(data: DataModel, user: str):
    """
    API to insert or update data in OpenSearch. Logs all actions.
    """
    try:
        # Generate a unique ID based on content for deduplication
        doc_id = str(uuid5(NAMESPACE_DNS, f"{data.name}-{data.username}-{data.address}-{data.language}"))

        # Check if the document exists
        existing_doc = client.get(index=DATA_INDEX, id=doc_id, ignore=[404])

        if existing_doc.get("found"):
            # Update the existing document
            action = "update"
            repository.update_data(index=DATA_INDEX, doc_id=doc_id, data=data.dict())
            create_time = existing_doc["_source"].get("create_time", datetime.utcnow().isoformat())
            update_time = datetime.utcnow()
        else:
            # Insert a new document
            action = "insert"
            create_time = datetime.utcnow()
            update_time = create_time
            repository.insert_data(
                index=DATA_INDEX,
                doc_id=doc_id,
                data={**data.dict(), "create_time": create_time.isoformat(), "update_time": update_time.isoformat()}
            )

        # Log the action
        log_entry = LogModel(
            user=user,
            action=action,
            create_time=create_time,
            update_time=update_time
        )
        repository.insert_log(index=LOGS_INDEX, log_entry=log_entry.dict())

        return {"status": "success", "action": action, "id": doc_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/data/{doc_id}")
async def get_data(doc_id: str):
    """
    API to fetch data by document ID from OpenSearch.
    """
    try:
        doc = client.get(index=DATA_INDEX, id=doc_id, ignore=[404])
        if not doc.get("found"):
            raise HTTPException(status_code=404, detail="Document not found")
        return doc["_source"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/logs")
async def get_logs():
    """
    API to fetch all logs from OpenSearch.
    """
    try:
        logs = client.search(index=LOGS_INDEX, body={"query": {"match_all": {}}})
        return [log["_source"] for log in logs["hits"]["hits"]]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

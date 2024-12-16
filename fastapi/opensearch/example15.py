# client.py
from opensearchpy import OpenSearch, RequestsHttpConnection
import os

OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST", "localhost")
OPENSEARCH_PORT = int(os.getenv("OPENSEARCH_PORT", 9200))

client = OpenSearch(
    hosts=[{"host": OPENSEARCH_HOST, "port": OPENSEARCH_PORT}],
    http_auth=(os.getenv("OPENSEARCH_USER", "admin"), os.getenv("OPENSEARCH_PASSWORD", "admin")),
    use_ssl=False,
    verify_certs=False,
    connection_class=RequestsHttpConnection,
)

# repository.py
from opensearchpy import OpenSearch, OpenSearchException

class OpenSearchRepository:
    def __init__(self, client: OpenSearch):
        self.client = client

    def insert_data(self, index: str, doc_id: str, data: dict):
        try:
            self.client.index(index=index, id=doc_id, body=data)
        except OpenSearchException as e:
            raise RuntimeError(f"Failed to insert data into index {index}: {e}")

    def update_data(self, index: str, doc_id: str, data: dict):
        try:
            self.client.update(index=index, id=doc_id, body={"doc": data})
        except OpenSearchException as e:
            raise RuntimeError(f"Failed to update data in index {index}: {e}")

    def get_data(self, index: str, doc_id: str):
        try:
            return self.client.get(index=index, id=doc_id, ignore=[404])
        except OpenSearchException as e:
            raise RuntimeError(f"Failed to retrieve data from index {index}: {e}")

    def execute_query(self, index: str, query: dict) -> list:
        try:
            response = self.client.search(index=index, body=query)
            return [hit["_source"] for hit in response["hits"]["hits"]]
        except OpenSearchException as e:
            raise RuntimeError(f"Failed to execute query on index {index}: {e}")

# data_model.py
from pydantic import BaseModel

class DataModel(BaseModel):
    name: str
    username: str
    address: str
    language: str
    region: str  # New field added for region

# log_model.py
from pydantic import BaseModel
from datetime import datetime

class LogModel(BaseModel):
    user: str
    action: str
    create_time: datetime = None
    update_time: datetime = None

# main.py
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

@app.post("/data")
async def handle_data(data: DataModel, user: str):
    try:
        doc_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{data.name}-{data.username}-{data.address}-{data.language}"))
        existing_doc = repository.get_data(DATA_INDEX, doc_id)

        if existing_doc.get("found"):
            action = "update"
            repository.update_data(DATA_INDEX, doc_id, data.dict())
            create_time = existing_doc["_source"].get("create_time", datetime.utcnow().isoformat())
            update_time = datetime.utcnow()
        else:
            action = "insert"
            create_time = datetime.utcnow()
            update_time = create_time
            repository.insert_data(
                DATA_INDEX, 
                doc_id, 
                {**data.dict(), "create_time": create_time.isoformat(), "update_time": update_time.isoformat()}
            )

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

@app.get("/logs")
async def get_logs(query: dict):
    try:
        logs = repository.execute_query(LOGS_INDEX, query)
        return {"logs": logs}
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))









======================================

if existing_doc.get("found"):
    action = "update"
    repository.update_data(DATA_INDEX, doc_id, data.dict())
    
    # Preserve the existing create_time, set a new update_time
    create_time = existing_doc["_source"].get("create_time", datetime.utcnow().isoformat())
    update_time = datetime.utcnow()  # Update this for the latest change
else:
    action = "insert"
    create_time = datetime.utcnow()  # Set creation time for new records
    update_time = create_time        # Same as creation time for a new record
    repository.insert_data(
        DATA_INDEX, 
        doc_id, 
        {**data.dict(), "create_time": create_time.isoformat(), "update_time": update_time.isoformat()}
    )


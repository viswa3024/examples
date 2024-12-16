from fastapi import FastAPI, HTTPException
from opensearchpy import OpenSearch, RequestsHttpConnection
from pydantic import BaseModel
from datetime import datetime
import os
import uuid

app = FastAPI()

# Configuration for OpenSearch
OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST", "localhost")
OPENSEARCH_PORT = int(os.getenv("OPENSEARCH_PORT", 9200))
client = OpenSearch(
    hosts=[{"host": OPENSEARCH_HOST, "port": OPENSEARCH_PORT}],
    http_auth=(os.getenv("OPENSEARCH_USER", "admin"), os.getenv("OPENSEARCH_PASSWORD", "admin")),
    use_ssl=False,
    verify_certs=False,
    connection_class=RequestsHttpConnection,
)

# Index names
DATA_INDEX = "opensearch-create-data-index"
LOGS_INDEX = "opensearch-create-logs-index"

class DataModel(BaseModel):
    name: str
    username: str
    address: str
    language: str

class LogModel(BaseModel):
    user: str
    action: str
    timestamp: datetime

# Helper function to create an index if it doesn't exist
def create_index_if_not_exists(index_name: str, mapping: dict = None):
    if not client.indices.exists(index=index_name):
        client.indices.create(index=index_name, body={"mappings": mapping} if mapping else None)

@app.on_event("startup")
async def setup_indices():
    # Ensure both indices exist at startup
    create_index_if_not_exists(DATA_INDEX)
    create_index_if_not_exists(LOGS_INDEX)

@app.post("/data")
async def handle_data(data: DataModel, user: str):
    # Create or update the data index
    try:
        create_index_if_not_exists(DATA_INDEX)
        create_index_if_not_exists(LOGS_INDEX)

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

from fastapi import FastAPI, HTTPException
from opensearchpy import OpenSearch, RequestsHttpConnection
from datetime import datetime
import uuid
import os
from data_model import DataModel
from log_model import LogModel

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

@app.post("/data")
async def handle_data(data: DataModel, user: str):
    """
    API to insert or update data in OpenSearch. Logs all actions.
    """
    try:
        # Generate a unique ID based on content for deduplication
        doc_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{data.name}-{data.username}-{data.address}-{data.language}"))

        # Check if the document exists
        existing_doc = client.get(index=DATA_INDEX, id=doc_id, ignore=[404])

        if existing_doc.get("found"):
            # Update the existing document
            action = "update"
            client.update(
                index=DATA_INDEX,
                id=doc_id,
                body={"doc": data.dict()}
            )
            create_time = existing_doc["_source"].get("create_time", datetime.utcnow().isoformat())
            update_time = datetime.utcnow()
        else:
            # Insert a new document
            action = "insert"
            create_time = datetime.utcnow()
            update_time = create_time
            client.index(
                index=DATA_INDEX,
                id=doc_id,
                body={**data.dict(), "create_time": create_time.isoformat(), "update_time": update_time.isoformat()}
            )

        # Log the action
        log_entry = LogModel(
            user=user,
            action=action,
            create_time=create_time,
            update_time=update_time
        )
        client.index(
            index=LOGS_INDEX,
            body=log_entry.dict()
        )

        return {"status": "success", "action": action, "id": doc_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

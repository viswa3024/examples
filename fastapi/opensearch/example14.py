# repository.py
from opensearchpy import OpenSearch

class OpenSearchRepository:
    def __init__(self, client: OpenSearch):
        self.client = client

    def insert_data(self, index: str, doc_id: str, data: dict):
        self.client.index(index=index, id=doc_id, body=data)

    def update_data(self, index: str, doc_id: str, data: dict):
        self.client.update(index=index, id=doc_id, body={"doc": data})

    def get_data(self, index: str, doc_id: str):
        return self.client.get(index=index, id=doc_id, ignore=[404])

    def execute_query(self, index: str, query: dict) -> list:
        """
        Executes a given query on the specified OpenSearch index.
        """
        response = self.client.search(index=index, body=query)
        return [hit["_source"] for hit in response["hits"]["hits"]]

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

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/logs")
async def get_logs(query: dict):
    try:
        logs = repository.execute_query(LOGS_INDEX, query)
        return {"logs": logs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

repository.py

from datetime import datetime
from opensearchpy import OpenSearch
from typing import Optional


class OpenSearchRepository:
    def __init__(self, client: OpenSearch, data_index: str, logs_index: str):
        self.client = client
        self.data_index = data_index
        self.logs_index = logs_index

    def update_data(self, index: str, doc_id: str, data: dict) -> None:
        """
        Updates an existing document in the OpenSearch index.
        """
        self.client.update(
            index=index,
            id=doc_id,
            body={"doc": data}
        )

    def insert_data(self, index: str, doc_id: str, data: dict) -> None:
        """
        Inserts a new document into the OpenSearch index.
        """
        self.client.index(
            index=index,
            id=doc_id,
            body=data
        )

    def insert_log(self, log_entry: dict) -> None:
        """
        Inserts a log entry into the logs index.
        """
        self.client.index(
            index=self.logs_index,
            body=log_entry
        )

    def get_document(self, index: str, doc_id: str) -> Optional[dict]:
        """
        Retrieves a document from OpenSearch by its ID.
        """
        response = self.client.get(index=index, id=doc_id, ignore=[404])
        if response.get("found"):
            return response["_source"]
        return None

    def search_logs(self, query: dict) -> list:
        """
        Searches logs in OpenSearch using a provided query.
        """
        response = self.client.search(index=self.logs_index, body=query)
        return [hit["_source"] for hit in response["hits"]["hits"]]


========================


main.py


from fastapi import FastAPI, HTTPException
from datetime import datetime
import uuid
from data_model import DataModel
from log_model import LogModel
from client import client  # Import the OpenSearch client
from repository import OpenSearchRepository  # Import the repository

app = FastAPI()

# Index names
DATA_INDEX = "opensearch-create-data-index"
LOGS_INDEX = "opensearch-create-logs-index"

# Initialize the repository
repository = OpenSearchRepository(client=client, data_index=DATA_INDEX, logs_index=LOGS_INDEX)


@app.post("/data")
async def handle_data(data: DataModel, user: str):
    """
    API to insert or update data in OpenSearch. Logs all actions.
    """
    try:
        # Generate a unique ID based on content for deduplication
        doc_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{data.name}-{data.username}-{data.address}-{data.language}"))

        # Check if the document exists
        existing_doc = repository.get_document(index=DATA_INDEX, doc_id=doc_id)

        if existing_doc:
            # Update the existing document
            action = "update"
            repository.update_data(
                index=DATA_INDEX,
                doc_id=doc_id,
                data=data.dict()
            )
            create_time = existing_doc.get("create_time", datetime.utcnow().isoformat())
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
        repository.insert_log(log_entry.dict())

        return {"status": "success", "action": action, "id": doc_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/data/{doc_id}")
async def get_data(doc_id: str):
    """
    API to get data from OpenSearch by document ID.
    """
    try:
        # Fetch the document by its ID
        data = repository.get_document(index=DATA_INDEX, doc_id=doc_id)

        if data:
            return {"status": "success", "data": data}
        else:
            raise HTTPException(status_code=404, detail="Data not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/logs")
async def get_logs(user: str = None, action: str = None):
    """
    API to get logs from OpenSearch. Optionally filter by user or action.
    """
    try:
        # Define the query
        query = {
            "query": {
                "bool": {
                    "must": [],
                    "filter": []
                }
            }
        }

        # Add user filter if provided
        if user:
            query["query"]["bool"]["filter"].append({"term": {"user.keyword": user}})

        # Add action filter if provided
        if action:
            query["query"]["bool"]["filter"].append({"term": {"action.keyword": action}})

        # Search for logs
        logs = repository.search_logs(query=query)
        return {"status": "success", "logs": logs}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


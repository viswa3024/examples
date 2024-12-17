from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

class DataModel(BaseModel):
    name: str
    username: str
    address: str
    language: str
    image_name: str  # This will be updated with the file name


@app.post("/submit-data/")
async def submit_data(
    data: str = Form(...),  # Receive JSON as string
    file: UploadFile = File(...)
):
    try:
        # Parse JSON string into DataModel
        data_obj = DataModel(**json.loads(data))
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON object")

    # Update the image_name field with the filename from the uploaded file
    data_obj.image_name = file.filename

    file_content = await file.read()
    return {
        "message": "Data and file received successfully",
        "submitted_data": data_obj.dict(),
        "file_info": {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(file_content),
        },
    }

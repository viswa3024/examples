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

# Allowed image types (including SVG), now in a list
ALLOWED_IMAGE_TYPES = ["image/png", "image/jpeg", "image/jpg", "image/svg+xml"]

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

    # Check if the file exists and is not empty
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    # Check if the uploaded file type is allowed using the list
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type. Only image files and SVG are allowed.")

    # Optionally, check file size (example: max 5MB)
    max_size = 5 * 1024 * 1024  # 5MB
    if len(await file.read()) > max_size:
        raise HTTPException(status_code=400, detail="File size exceeds the maximum limit of 5MB")

    # Re-read the file content after checking size (because it was consumed in size check)
    await file.seek(0)

    # Set the image_name from the uploaded file's filename
    data_obj.image_name = file.filename

    file_content = await file.read()
    return {
        "message": "Data and file received successfully",
        "submitted_data": data_obj.dict(),  # Convert data model to dictionary
        "file_info": {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(file_content),
        },
    }

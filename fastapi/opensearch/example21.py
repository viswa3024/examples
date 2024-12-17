from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Define the Pydantic model
class DataModel(BaseModel):
    name: str
    username: str
    address: str
    language: str

# Create FastAPI app instance
app = FastAPI()

# POST endpoint
@app.post("/submit-data/")
async def submit_data(data: DataModel):
    # Example logic (e.g., validation or processing)
    if not data.language.isalpha():
        raise HTTPException(status_code=400, detail="Language must only contain alphabetic characters.")
    
    # Return the received data as a response
    return {
        "message": "Data received successfully",
        "submitted_data": data.dict()  # Convert the model to a dictionary for the response
    }
=============================================================

from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from pydantic import BaseModel

# Define the Pydantic model
class DataModel(BaseModel):
    name: str
    username: str
    address: str
    language: str

# Create FastAPI app instance
app = FastAPI()

# POST endpoint with file upload
@app.post("/submit-data/")
async def submit_data(
    name: str = Form(...),
    username: str = Form(...),
    address: str = Form(...),
    language: str = Form(...),
    file: UploadFile = File(...)
):
    # Process the file (example: save it or read its content)
    file_content = await file.read()
    
    # Example logic: Check file size (optional)
    if len(file_content) > 5 * 1024 * 1024:  # 5 MB limit
        raise HTTPException(status_code=400, detail="File size exceeds 5 MB limit.")

    # Return a response
    return {
        "message": "Data and file received successfully",
        "submitted_data": {
            "name": name,
            "username": username,
            "address": address,
            "language": language,
        },
        "file_info": {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(file_content),
        },
    }

Request Body (multipart/form-data):

name: John Doe
username: johndoe123
address: 123 Elm Street
language: English
file: [Upload a file]

Example Response:
{
    "message": "Data and file received successfully",
    "submitted_data": {
        "name": "John Doe",
        "username": "johndoe123",
        "address": "123 Elm Street",
        "language": "English"
    },
    "file_info": {
        "filename": "example.txt",
        "content_type": "text/plain",
        "size": 128
    }
}
===============================================================


from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from pydantic import BaseModel

# Define the Pydantic model
class DataModel(BaseModel):
    name: str
    username: str
    address: str
    language: str

# Create FastAPI app instance
app = FastAPI()

# POST endpoint
@app.post("/submit-data/")
async def submit_data(
    name: str = Form(...),
    username: str = Form(...),
    address: str = Form(...),
    language: str = Form(...),
    file: UploadFile = File(...)
):
    # Construct the DataModel object
    data = DataModel(name=name, username=username, address=address, language=language)
    
    # Process the file (example: read its content or save it)
    file_content = await file.read()
    
    # Example validation: Check file type (optional)
    if file.content_type not in ["image/png", "image/jpeg", "application/pdf"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PNG, JPEG, and PDF are allowed.")
    
    # Return the combined response
    return {
        "message": "Data and file received successfully",
        "submitted_data": data.dict(),  # Convert DataModel to dict
        "file_info": {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(file_content),
        },
    }

# To include both the DataModel and file upload in a FastAPI POST endpoint, you'll need to handle the structured fields from DataModel while also accepting the file. This can be done by combining Form and File inputs. Unfortunately, you cannot directly pass a Pydantic model (DataModel) as-is with File uploads because multipart form data does not directly map to JSON. Instead, you can extract individual fields for the DataModel using Form and construct the model manually.



==========================================================================


To handle the fields collectively as an object (DataModel), you can use Depends in FastAPI. This allows you to extract and validate the fields from a multipart form request while leveraging Pydantic's validation for the DataModel.

Here’s how you can achieve that:

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from pydantic import BaseModel
from fastapi.params import Depends
from typing import Optional

# Define the Pydantic model
class DataModel(BaseModel):
    name: str
    username: str
    address: str
    language: str

# Dependency to parse form data into a Pydantic model
def parse_form_data(
    name: str = Form(...),
    username: str = Form(...),
    address: str = Form(...),
    language: str = Form(...)
) -> DataModel:
    return DataModel(name=name, username=username, address=address, language=language)

# Create FastAPI app instance
app = FastAPI()

# POST endpoint
@app.post("/submit-data/")
async def submit_data(
    data: DataModel = Depends(parse_form_data),
    file: UploadFile = File(...)
):
    # Process the file
    file_content = await file.read()
    
    # Example validation: Check file type
    if file.content_type not in ["image/png", "image/jpeg", "application/pdf"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PNG, JPEG, and PDF are allowed.")
    
    # Return the combined response
    return {
        "message": "Data and file received successfully",
        "submitted_data": data.dict(),  # Convert DataModel to dict
        "file_info": {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(file_content),
        },
    }

======================================================

If you want to handle the entire DataModel as an object without reading each field individually (i.e., no name: str = Form(...)), you can use Form with Depends while still constructing the DataModel from the incoming multipart form data. Here's how:

Solution: Using DataModel Directly
In this approach, we parse the entire multipart form data into a Pydantic model in one step.

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

# Define the Pydantic model
class DataModel(BaseModel):
    name: str
    username: str
    address: str
    language: str

# Create FastAPI app instance
app = FastAPI()

# Helper to parse form data into DataModel
async def as_form(
    name: str = Form(...),
    username: str = Form(...),
    address: str = Form(...),
    language: str = Form(...)
) -> DataModel:
    return DataModel(name=name, username=username, address=address, language=language)

# POST endpoint
@app.post("/submit-data/")
async def submit_data(
    data: DataModel = Depends(as_form),
    file: UploadFile = File(...)
):
    # Process file
    file_content = await file.read()

    # Example: File size validation
    if len(file_content) > 5 * 1024 * 1024:  # 5 MB limit
        raise HTTPException(status_code=400, detail="File size exceeds 5 MB.")
    
    # Return combined response
    return {
        "message": "Data and file received successfully",
        "submitted_data": jsonable_encoder(data),
        "file_info": {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(file_content),
        },
    }
  
======================================================

If you don’t want to write the as_form function repeatedly, you can make a reusable decorator for Pydantic models to handle form parsing automatically:

from typing import Type
from fastapi import Form
from pydantic import BaseModel

def as_form(cls: Type[BaseModel]):
    def _as_form(**data):
        return cls(**data)
    cls.as_form = _as_form
    return cls

@as_form
class DataModel(BaseModel):
    name: str
    username: str
    address: str
    language: str


@app.post("/submit-data/")
async def submit_data(
    data: DataModel = Depends(DataModel.as_form),
    file: UploadFile = File(...)
):
    # Process data and file
    ...
========================================================


If you're receiving the form data as strings and not as a DataModel object when using the as_form function, it's likely because the form data is not being properly parsed into the DataModel object. Let’s address this issue step by step to ensure that the form fields are correctly transformed into a DataModel instance.

Correct Approach to Parse Form Data into a Pydantic Object
Here’s how to ensure the transformation is done properly:

Create a Custom as_form Method for DataModel: Instead of writing a separate function, we can define a method on the Pydantic model itself to parse form data directly.

Updated Code Example:

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from pydantic import BaseModel

# Helper decorator for form parsing
def as_form(cls):
    def _as_form(**data):
        return cls(**data)
    cls.as_form = _as_form
    return cls

# Define the Pydantic model
@as_form
class DataModel(BaseModel):
    name: str
    username: str
    address: str
    language: str

# Create FastAPI app instance
app = FastAPI()

@app.post("/submit-data/")
async def submit_data(
    data: DataModel = Depends(DataModel.as_form),
    file: UploadFile = File(...)
):
    # Validate file content
    file_content = await file.read()
    if len(file_content) > 5 * 1024 * 1024:  # Limit: 5 MB
        raise HTTPException(status_code=400, detail="File size exceeds 5 MB.")
    
    # Return combined response
    return {
        "message": "Data and file received successfully",
        "submitted_data": data.dict(),  # Convert DataModel to dict
        "file_info": {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(file_content),
        },
    }


Explanation:
Custom as_form Decorator:

The as_form decorator automatically maps the form fields to a Pydantic model (DataModel) without requiring individual fields to be declared in the endpoint.
It creates an as_form method dynamically for any Pydantic model, making it reusable.
FastAPI Dependency Injection:

The Depends(DataModel.as_form) ensures the parsed data is provided as a DataModel object.
File Handling:

The file field is handled separately, and its content is processed independently.


Benefits of This Approach:
Clean Code: Avoids writing separate parsing logic for each model.
Reusable: The as_form decorator can be applied to any Pydantic model.
Proper Object Mapping: The form data is directly mapped to a DataModel object with full Pydantic validation.

Here's a curl example to test the FastAPI endpoint with multipart/form-data, including form fields and a file upload.

Example curl Request:

curl -X POST "http://127.0.0.1:8000/submit-data/" \
-H "Content-Type: multipart/form-data" \
-F "name=John Doe" \
-F "username=johndoe123" \
-F "address=123 Elm Street" \
-F "language=English" \
-F "file=@example.txt"
Explanation of the curl Command:
-X POST: Specifies the HTTP method (POST).
URL: Replace http://127.0.0.1:8000/submit-data/ with your API endpoint.
-H "Content-Type: multipart/form-data": Sets the request header for multipart/form-data.
-F "key=value":
Sends form data fields (name, username, address, language) as key-value pairs.
-F "file=@example.txt":
Uploads a file named example.txt from your local machine.
Replace example.txt with the path to your test file.

================================================

FastAPI processes form data as multipart/form-data, and the Form() method only supports string-like values because form fields in HTTP are transmitted as strings. If you want to send complex objects like JSON in the request body instead of form data, you can use application/json and pass a BaseModel object.

However, if you must stick with multipart/form-data and send complex objects, you'll need to encode the object as a string (e.g., JSON string) and parse it back into the desired structure on the server.


Approaches to Handle Objects:
1. Use application/json (Preferred for Objects)
If the data can be sent as JSON instead of multipart/form-data, the API design becomes simpler:

Endpoint Code:

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

app = FastAPI()

class DataModel(BaseModel):
    name: str
    username: str
    address: str
    language: str

@app.post("/submit-data/")
async def submit_data(data: DataModel, file: UploadFile = File(...)):
    file_content = await file.read()
    return {
        "message": "Data and file received successfully",
        "submitted_data": data.dict(),
        "file_info": {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(file_content),
        },
    }

Request curl:

curl -X POST "http://127.0.0.1:8000/submit-data/" \
-H "Content-Type: application/json" \
-H "accept: application/json" \
-F "file=@example.txt" \
-d '{"name": "test", "username": "user123", "address": "123 Elm Street", "language": "English"}'


2. Stick to multipart/form-data and Encode Object as JSON
If you must use multipart/form-data, you can send the object as a JSON string in one of the form fields.

Updated Endpoint Code:

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

class DataModel(BaseModel):
    name: str
    username: str
    address: str
    language: str

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

Request curl:

curl -X POST "http://127.0.0.1:8000/submit-data/" \
-H "Content-Type: multipart/form-data" \
-F "data={\"name\":\"test\",\"username\":\"user123\",\"address\":\"123 Elm Street\",\"language\":\"English\"}" \
-F "file=@example.txt"

Why Strings in Form?
HTTP form fields (multipart/form-data) inherently represent data as strings. If you send non-string data (like objects), encoding/decoding is required because browsers and HTTP libraries transmit form fields as key-value pairs, where the values are always strings.

Using JSON (application/json) avoids this limitation by transmitting structured data natively. If file upload is required alongside structured data, combining the two approaches is necessary.


====================================================

To handle multiple file uploads as an array in FastAPI, you can use a list of UploadFile objects. Here's how to update your endpoint to support multiple files:

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from pydantic import BaseModel
import json

# Helper decorator for form parsing
def as_form(cls):
    def _as_form(**data):
        return cls(**data)
    cls.as_form = _as_form
    return cls

# Define the Pydantic model
@as_form
class DataModel(BaseModel):
    name: str
    username: str
    address: str
    language: str

app = FastAPI()

@app.post("/submit-data/")
async def submit_data(
    data: DataModel = Depends(DataModel.as_form),  # Parse form data into DataModel
    files: list[UploadFile] = File(...)           # Accept multiple files
):
    # Validate file count and process files
    file_infos = []
    for file in files:
        content = await file.read()
        if len(content) > 5 * 1024 * 1024:  # Limit: 5 MB
            raise HTTPException(status_code=400, detail=f"File {file.filename} exceeds size limit.")
        file_infos.append({
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(content),
        })

    return {
        "message": "Data and files received successfully",
        "submitted_data": data.dict(),
        "files_info": file_infos,
    }

Key Changes:
Multiple Files:

Changed file: UploadFile to files: list[UploadFile] to accept multiple files.
Each file in the list is processed individually.
Form Data:

The DataModel still uses the as_form approach to parse form fields into a Pydantic model.

Request Example with curl:

curl -X POST "http://127.0.0.1:8000/submit-data/" \
-H "Content-Type: multipart/form-data" \
-F "name=John Doe" \
-F "username=johndoe123" \
-F "address=123 Elm Street" \
-F "language=English" \
-F "files=@example1.txt" \
-F "files=@example2.txt"

Explanation:
-F "files=@example1.txt": Specifies the first file to upload.
-F "files=@example2.txt": Specifies the second file.
Add more -F "files=@<file>" entries for additional files.

Example Response:

{
    "message": "Data and files received successfully",
    "submitted_data": {
        "name": "John Doe",
        "username": "johndoe123",
        "address": "123 Elm Street",
        "language": "English"
    },
    "files_info": [
        {
            "filename": "example1.txt",
            "content_type": "text/plain",
            "size": 2048
        },
        {
            "filename": "example2.txt",
            "content_type": "text/plain",
            "size": 4096
        }
    ]
}


To handle multiple file uploads as an array in FastAPI, you can use a list of UploadFile objects. Here's how to update your endpoint to support multiple files:

Updated Endpoint Code
python
Copy code
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from pydantic import BaseModel
import json

# Helper decorator for form parsing
def as_form(cls):
    def _as_form(**data):
        return cls(**data)
    cls.as_form = _as_form
    return cls

# Define the Pydantic model
@as_form
class DataModel(BaseModel):
    name: str
    username: str
    address: str
    language: str

app = FastAPI()

@app.post("/submit-data/")
async def submit_data(
    data: DataModel = Depends(DataModel.as_form),  # Parse form data into DataModel
    files: list[UploadFile] = File(...)           # Accept multiple files
):
    # Validate file count and process files
    file_infos = []
    for file in files:
        content = await file.read()
        if len(content) > 5 * 1024 * 1024:  # Limit: 5 MB
            raise HTTPException(status_code=400, detail=f"File {file.filename} exceeds size limit.")
        file_infos.append({
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(content),
        })

    return {
        "message": "Data and files received successfully",
        "submitted_data": data.dict(),
        "files_info": file_infos,
    }
Key Changes:
Multiple Files:

Changed file: UploadFile to files: list[UploadFile] to accept multiple files.
Each file in the list is processed individually.
Form Data:

The DataModel still uses the as_form approach to parse form fields into a Pydantic model.
Request Example with curl:
bash
Copy code
curl -X POST "http://127.0.0.1:8000/submit-data/" \
-H "Content-Type: multipart/form-data" \
-F "name=John Doe" \
-F "username=johndoe123" \
-F "address=123 Elm Street" \
-F "language=English" \
-F "files=@example1.txt" \
-F "files=@example2.txt"
Explanation:
-F "files=@example1.txt": Specifies the first file to upload.
-F "files=@example2.txt": Specifies the second file.
Add more -F "files=@<file>" entries for additional files.
Example Response:
json
Copy code
{
    "message": "Data and files received successfully",
    "submitted_data": {
        "name": "John Doe",
        "username": "johndoe123",
        "address": "123 Elm Street",
        "language": "English"
    },
    "files_info": [
        {
            "filename": "example1.txt",
            "content_type": "text/plain",
            "size": 2048
        },
        {
            "filename": "example2.txt",
            "content_type": "text/plain",
            "size": 4096
        }
    ]
}
Notes:
File Size Validation:

Each file's size is validated individually to ensure no single file exceeds the limit.
Handling Large Files:

FastAPI streams file uploads, so you can handle large files efficiently without loading them into memory all at once.
Maximum Number of Files:

If needed, you can add additional validation to limit the number of files uploaded. For example:

if len(files) > 10:
    raise HTTPException(status_code=400, detail="Too many files uploaded. Maximum is 10.")

=============================================

This code snippet demonstrates a way to add a custom method (as_form) to a Pydantic model dynamically, which allows the model to easily parse form data provided via FastAPI's Form fields.

Detailed Explanation:
1. as_form Function

def as_form(cls):
    def _as_form(**data):
        return cls(**data)
    cls.as_form = _as_form
    return cls

Purpose:
This function takes a class (cls, typically a Pydantic model) and dynamically adds an as_form method to it. This as_form method allows you to instantiate the Pydantic model from Form data.

How it Works:

cls is the class to which you want to add the method (e.g., DataModel).
_as_form(**data) is a nested function that takes form field data as keyword arguments (**data) and instantiates the class (cls) using cls(**data).
cls.as_form = _as_form dynamically attaches the _as_form method to the class.
return cls ensures that the modified class is returned.

2. Applying the Decorator to DataModel

@as_form
class DataModel(BaseModel):
    name: str
    username: str
    address: str
    language: str

Decorator Use:
The @as_form decorator is applied to the DataModel class, which is a subclass of Pydantic's BaseModel.

Effect: After applying the decorator:

The DataModel class now has an as_form method that can be used to create an instance of DataModel from form fields.

3. Usage with FastAPI
In FastAPI, you often need to parse data submitted in a form (multipart/form-data) rather than a JSON payload (application/json). Pydantic models, by default, work well with JSON but don't natively support form parsing. This snippet bridges that gap.

Example Endpoint:

from fastapi import FastAPI, Form, Depends

app = FastAPI()

@app.post("/submit/")
async def submit(data: DataModel = Depends(DataModel.as_form)):
    return {"submitted_data": data.dict()}

Depends(DataModel.as_form):
This tells FastAPI to use the as_form method to create a DataModel instance from form data.
FastAPI automatically extracts the form fields (e.g., name, username, address, language) and passes them as keyword arguments to the as_form method.



This code snippet demonstrates a way to add a custom method (as_form) to a Pydantic model dynamically, which allows the model to easily parse form data provided via FastAPI's Form fields.

Detailed Explanation:
1. as_form Function
python
Copy code
def as_form(cls):
    def _as_form(**data):
        return cls(**data)
    cls.as_form = _as_form
    return cls
Purpose:
This function takes a class (cls, typically a Pydantic model) and dynamically adds an as_form method to it. This as_form method allows you to instantiate the Pydantic model from Form data.

How it Works:

cls is the class to which you want to add the method (e.g., DataModel).
_as_form(**data) is a nested function that takes form field data as keyword arguments (**data) and instantiates the class (cls) using cls(**data).
cls.as_form = _as_form dynamically attaches the _as_form method to the class.
return cls ensures that the modified class is returned.
2. Applying the Decorator to DataModel
python
Copy code
@as_form
class DataModel(BaseModel):
    name: str
    username: str
    address: str
    language: str
Decorator Use:
The @as_form decorator is applied to the DataModel class, which is a subclass of Pydantic's BaseModel.

Effect: After applying the decorator:

The DataModel class now has an as_form method that can be used to create an instance of DataModel from form fields.
3. Usage with FastAPI
In FastAPI, you often need to parse data submitted in a form (multipart/form-data) rather than a JSON payload (application/json). Pydantic models, by default, work well with JSON but don't natively support form parsing. This snippet bridges that gap.

Example Endpoint:

python
Copy code
from fastapi import FastAPI, Form, Depends

app = FastAPI()

@app.post("/submit/")
async def submit(data: DataModel = Depends(DataModel.as_form)):
    return {"submitted_data": data.dict()}
Depends(DataModel.as_form):
This tells FastAPI to use the as_form method to create a DataModel instance from form data.
FastAPI automatically extracts the form fields (e.g., name, username, address, language) and passes them as keyword arguments to the as_form method.
4. Key Benefits
Cleaner Code:
Instead of listing each form field explicitly in the endpoint, you can define them once in the Pydantic model and reuse that definition.

Consistency:
All the validation rules defined in the DataModel are automatically applied to the form data.

Reusability:
The same Pydantic model can be used for both JSON requests and form submissions, making the code more DRY (Don't Repeat Yourself).


Example Request
Here’s how you would send a request to the /submit/ endpoint:

curl Command:

curl -X POST "http://127.0.0.1:8000/submit/" \
-H "Content-Type: multipart/form-data" \
-F "name=John Doe" \
-F "username=johndoe123" \
-F "address=123 Elm Street" \
-F "language=English"

Response:

{
    "submitted_data": {
        "name": "John Doe",
        "username": "johndoe123",
        "address": "123 Elm Street",
        "language": "English"
    }
}

Summary
The as_form function is a clever utility that enhances Pydantic models to work seamlessly with form data in FastAPI. It dynamically adds an as_form method, which simplifies the creation of model instances from Form fields, ensuring clean, reusable, and validation-ready code.


=================================


import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private apiUrl = 'http://127.0.0.1:8000/submit-data/';

  constructor(private http: HttpClient) {}

  submitData(data: any, file: File): Observable<any> {
    const formData = new FormData();
    formData.append('data', JSON.stringify(data)); // Append JSON data
    formData.append('file', file, file.name); // Append the file

    return this.http.post(this.apiUrl, formData);
  }
}


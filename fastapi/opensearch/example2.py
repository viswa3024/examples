{
    "id": "1",
    "content": {
        "name": "test",
        "username": "user1",
        "address": "user_address",
        "language": "english"
    }
}

curl -X POST "http://localhost:8000/data?user=user1" \\
-H "Content-Type: application/json" \\
-d '{
    "id": "1",
    "content": {
        "name": "test",
        "username": "user1",
        "address": "user_address",
        "language": "english"
    }
}'


import requests

url = "http://localhost:8000/data"
headers = {"Content-Type": "application/json"}
payload = {
    "id": "1",
    "content": {
        "name": "test",
        "username": "user1",
        "address": "user_address",
        "language": "english"
    }
}
params = {"user": "user1"}

response = requests.post(url, json=payload, params=params, headers=headers)

print(response.json())

import json
from tests.test_additional_properties_bool import app
from fastapi.testclient import TestClient

client = TestClient(app)
response = client.get("/openapi.json")
print(json.dumps(response.json(), indent=2))

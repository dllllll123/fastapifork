from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel, ConfigDict


class FooBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Foo(FooBaseModel):
    pass


app = FastAPI()


@app.post("/")
async def post(
    foo: Foo | None = None,
):
    return foo


client = TestClient(app)


def test_call_invalid():
    response = client.post("/", json={"foo": {"bar": "baz"}})
    assert response.status_code == 422


def test_call_valid():
    response = client.post("/", json={})
    assert response.status_code == 200
    assert response.json() == {}


class PartialFoo(FooBaseModel):
    model_config = ConfigDict(extra="allow")


@app.post("/partial")
async def partial(
    foo: PartialFoo,
):
    return foo


def test_partial_update():
    response = client.post("/partial", json={"extra_field": "value"})
    assert response.status_code == 200
    assert response.json() == {"extra_field": "value"}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/": {
                    "post": {
                        "summary": "Post",
                        "operationId": "post__post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "anyOf": [
                                            {"$ref": "#/components/schemas/Foo"},
                                            {"type": "null"},
                                        ],
                                        "title": "Foo",
                                    }
                                }
                            }
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {"application/json": {"schema": {}}},
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HTTPValidationError"
                                        }
                                    }
                                },
                            },
                        },
                    }
                }
            },
            "components": {
                "schemas": {
                    "Foo": {
                        "properties": {},
                        "additionalProperties": False,
                        "type": "object",
                        "title": "Foo",
                    },
                    "HTTPValidationError": {
                        "properties": {
                            "detail": {
                                "items": {
                                    "$ref": "#/components/schemas/ValidationError"
                                },
                                "type": "array",
                                "title": "Detail",
                            }
                        },
                        "type": "object",
                        "title": "HTTPValidationError",
                    },
                    "ValidationError": {
                        "properties": {
                            "ctx": {"title": "Context", "type": "object"},
                            "input": {"title": "Input"},
                            "loc": {
                                "items": {
                                    "anyOf": [{"type": "string"}, {"type": "integer"}]
                                },
                                "type": "array",
                                "title": "Location",
                            },
                            "msg": {"type": "string", "title": "Message"},
                            "type": {"type": "string", "title": "Error Type"},
                        },
                        "type": "object",
                        "required": ["loc", "msg", "type"],
                        "title": "ValidationError",
                    },
                }
            },
        }
    )

import importlib
import sys
from typing import Any

import pytest

needs_py310 = pytest.mark.skipif(
    sys.version_info < (3, 10), reason="requires python3.10+"
)
needs_py314 = pytest.mark.skipif(
    sys.version_info < (3, 14), reason="requires python3.14+"
)

needs_orjson = pytest.mark.skipif(
    importlib.util.find_spec("orjson") is None,
    reason="requires orjson",
)

needs_ujson = pytest.mark.skipif(
    importlib.util.find_spec("ujson") is None,
    reason="requires ujson",
)

workdir_lock = pytest.mark.xdist_group("workdir_lock")


def skip_module_if_py_gte_314():
    """Skip entire module on Python 3.14+ at import time."""
    if sys.version_info >= (3, 14):
        pytest.skip("requires python3.13-", allow_module_level=True)


def get_body_model_name(
    openapi: dict[str, Any], path: str, content_type: str = "application/json"
) -> str:
    body = openapi["paths"][path]["post"]["requestBody"]
    body_schema = body["content"][content_type]["schema"]
    return body_schema.get("$ref", "").split("/")[-1]


def get_request_body_schema(
    openapi: dict[str, Any], path: str, content_type: str = "application/json"
) -> dict[str, Any]:
    body_model_name = get_body_model_name(openapi, path, content_type)
    return openapi["components"]["schemas"][body_model_name]

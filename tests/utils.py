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


def get_request_body_schema(
    openapi: dict[str, Any],
    path: str,
    content_type: str = "application/json",
    method: str = "post",
) -> dict[str, Any]:
    body = openapi["paths"][path][method]["requestBody"]
    return body["content"][content_type]["schema"]


def get_body_model_name(
    openapi: dict[str, Any],
    path: str,
    content_type: str = "application/json",
    method: str = "post",
) -> str:
    body_schema = get_request_body_schema(openapi, path, content_type, method)
    return body_schema.get("$ref", "").split("/")[-1]

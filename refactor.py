import os

def process_file(file_path, content_type):
    with open(file_path, "r") as f:
        content = f.read()
        
    if "get_body_model_name" not in content:
        return

    content = content.replace("from .utils import get_body_model_name", "from tests.utils import get_request_body_schema")
    content = content.replace("get_body_model_name(openapi, path)", f'get_request_body_schema(openapi, path, "{content_type}")')

    with open(file_path, "w") as f:
        f.write(content)

base_dir = "tests/test_request_params"
for dirpath, dirnames, filenames in os.walk(base_dir):
    for filename in filenames:
        if filename.endswith(".py") and filename != "utils.py":
            file_path = os.path.join(dirpath, filename)
            
            content_type = ""
            if "test_file" in dirpath:
                content_type = "multipart/form-data"
            elif "test_form" in dirpath:
                content_type = "application/x-www-form-urlencoded"
            elif "test_body" in dirpath:
                content_type = "application/json"
            else:
                continue
                
            process_file(file_path, content_type)

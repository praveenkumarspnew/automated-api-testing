import os
import requests
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Get BASE_URL from environment
BASE_URL = os.getenv("BASE_URL", None)

if not BASE_URL:
    print("BASE_URL is not set. Please add it to your .env file.")
    exit(1)

# Fetch Swagger (OpenAPI) JSON specification
swagger_url = f"{BASE_URL}/swagger.json"
response = requests.get(swagger_url)

if response.status_code != 200:
    print(f"Failed to fetch Swagger JSON from {swagger_url}")
    exit(1)

swagger_spec = response.json()

# Parse the Swagger spec to generate tests
paths = swagger_spec.get("paths", {})

# Directory to store generated tests
test_dir = "./tests"
os.makedirs(test_dir, exist_ok=True)

def create_test_function(path, method, details):
    """Generate a test function for the given API path and method."""
    function_name = f"test_{method}_{path.replace('/', '_').strip('_')}"
    url = f"{BASE_URL}{path}"

    test_code = f"""
def {function_name}():
    \"\"\"Auto-generated test for {method.upper()} {url}\"\"\"
    response = requests.{method}(f"{{url}}")
    assert response.status_code == 200, f"Failed {method.upper()} {url}"
    assert response.json() is not None, f"No JSON response for {method.upper()} {url}"
"""
    return test_code

# Generate a test file
with open(os.path.join(test_dir, "test_auto_generated.py"), "w") as test_file:
    test_file.write("import requests\n\n")
    for path, methods in paths.items():
        for method, details in methods.items():
            test_func = create_test_function(path, method, details)
            test_file.write(test_func + "\n\n")

print(f"API tests generated in {test_dir}/test_auto_generated.py")


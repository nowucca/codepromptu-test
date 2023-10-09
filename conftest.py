import pytest
import requests
from dotenv import load_dotenv
import os
import base64

load_dotenv()

BASE_URL="http://aitools.cs.vt.edu:8000"
TEST_USERNAME = os.getenv('TEST_USERNAME')
TEST_PASSWORD = os.getenv('TEST_PASSWORD')


def get_auth_basic_credentials():
    # Ensure the variables are set
    if not TEST_USERNAME or not TEST_PASSWORD:
        raise ValueError("Both TEST_USERNAME and TEST_PASSWORD must be set!")

    # Encode the credentials
    credentials = f"{TEST_USERNAME}:{TEST_PASSWORD}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    return encoded_credentials


@pytest.fixture(autouse=True)
def teardown_database():
    yield  # This marks the separation between setup and teardown. Since we only need teardown, nothing is before yield.

    # After test completion, perform the teardown:
    # Assuming you have a function/API to fetch prompts by tags
    response = requests.get(f"{BASE_URL}/private/prompt/tags?tags=pytest", auth=(f"{TEST_USERNAME}", f"{TEST_PASSWORD}"))
    if response.status_code == 200:
        for prompt in response.json():
            guid = prompt["guid"]
            # Delete the prompt with "pytest" tag
            requests.delete(f"{BASE_URL}/private/prompt/{guid}", auth=(f"{TEST_USERNAME}", f"{TEST_PASSWORD}"))

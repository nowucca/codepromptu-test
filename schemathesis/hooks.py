import os

from schemathesis.hooks import HookContext, register
import schemathesis
import dotenv

dotenv.load_dotenv()

TEST_USERNAME = os.getenv('TEST_USERNAME')
DISCRIMINATOR_TAG = "pytest-" + TEST_USERNAME


@register("before_generate_body")
def add_pytest_tag(context: HookContext, case: schemathesis.Case) -> schemathesis.Case:
    # Check if the current endpoint is `POST /private/prompt/`
    if ((context.endpoint.method == "POST" or context.endpoint.method == "PUT") and
            (context.endpoint.path == "/private/prompt/" or context.endpoint.path == "/public/prompt")):
        # Ensure that the 'tags' attribute is present and modify its value
        if "tags" in case.body:
            case.body["tags"].append(DISCRIMINATOR_TAG)
        else:
            # If the 'tags' attribute doesn't exist, create it
            case.body["tags"] = [DISCRIMINATOR_TAG]
    return case

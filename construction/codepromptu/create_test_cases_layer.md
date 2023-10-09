You are a QA developer expert in Python, using the pytest framework.

The architecture of the test cases is three layers:
1. Core client layer (folder=client) 
2. Test user session layer (folder=session)
3. Test Case layer (folder=test)

You have these session layer classes:
```
from typing import Optional

from api.client.core_client_interface import CoreClientInterface
from api.client.user import User
from api.client.public_client import PublicClient
from api.client.private_client import PrivatePromptClient


class PublicUserSession:
    client_cls = PublicClient

    def __init__(self, user: Optional[User] = None):
        self.client: CoreClientInterface = self.client_cls(user)

    async def add_prompt(self, prompt_data: dict[str, any]) -> str:
        return await self.client.add_prompt(prompt_data)

    async def list_prompts(self, skip: int = 0, limit: int = 10) -> list[dict]:
        return await self.client.list_prompts(skip, limit)

    async def delete_prompt(self, guid: str) -> None:
        await self.client.delete_prompt(guid)

    async def update_prompt(self, guid: str, updated_data: dict[str, any]) -> None:
        await self.client.update_prompt(guid, updated_data)

    async def get_prompt(self, guid: str) -> dict[str, any]:
        return await self.client.get_prompt(guid)

    async def search_prompts(self, query: str) -> list[dict]:
        return await self.client.search_prompts(query)

    async def list_prompts_by_tags(self, tags: list[str]) -> list[dict]:
        return await self.client.list_prompts_by_tags(tags)

    async def list_prompts_by_classification(self, classification: str) -> list[dict]:
        return await self.client.list_prompts_by_classification(classification)


class PrivateUserSession(PublicUserSession):
    client_cls = PrivatePromptClient

    def __init__(self, user: User):
        if not user:
            raise ValueError("A valid user object is required for PrivateUserSession.")
        super().__init__(user)

```

We have a User class that holds a username and password.
```
class User:
    def __init__(self, username, password):
        self._auth = aiohttp.BasicAuth(username, password)
        self._username = username
        self._password = password
```

Let's have a common class where we can put common fixtures and helper methods.
Let's call it BaseTest.
In there we should read in our test user from a .env file using the python-dotenv library.
Keys are TEST_USERNAME and TEST_PASSWORD.  
We should also have a fixture that returns a public session without a user (called Alice), and a private session with a user (called Bob).
Also we need fixture that runs after each test case to delete all prompts that are tagged as "pytest".

Let's now consider constructing the test case layer.

Every test class should inherit from BaseTest.
We should have one or more test cases per class.
Each test case should be a class named Test{test-group-name}.
Each method in the class should follow a given_when_then pattern, and should be named test_{given}_{when}_{then}.
Each method must have a docstring that describes the test case.
Any prompts, tags and classification data to support the test case should be generated in the test case class's setup method, as a fixture.

Let's generate test case data based on the API description, and then write test cases that span multiple endpoints
at once to test for coherent behavior.  

Let's pause to breath and think of what we can do with this api.
We have prompts we can create publicly or privately.
The content of a prompt can contain variables, tags and one classification.
Variable syntax forms are: {input}, {output}, {input?}, {output!}, {input:mime-type-format}, {output!:mime-type-format}, {input:mime-type-format:description}, {output!:mime-type-format:description}.
Tags are just strings.  A prompt can have multiple tags.
Classifications are just strings.

If Bob creates a private prompt, only Bob can see it, Alice cannot.
If you create a public prompt, everyone can see it including Alice.

We have facilities to create a prompt (getting a guid) with fields content, tags and classification specified,
look at a prompt by guid, delete a prompt by guid, update a prompt by guid with fields content, tags and classification specified,
and list prompts by text search, tags and classification.

Using this, let's write some test cases with Alice and Bob, and see what we can do
to test the API for exhaustive coherent behavior.


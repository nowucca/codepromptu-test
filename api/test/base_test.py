import pytest
from dotenv import load_dotenv
import os

from api.client.user import User
from api.session.session import PublicUserSession, PrivateUserSession


class BaseTest:

    @pytest.fixture(autouse=True)  # autouse=True makes it automatically applied to tests
    async def clear_prompts(self, alice: PublicUserSession, bob: PrivateUserSession):
        """Fixture to delete prompts tagged as 'pytest' after every test."""
        yield
        # code to delete prompts tagged as 'pytest' here
        alice_tags = await alice.list_prompts_by_tags(["pytest"])
        bob_tags = await bob.list_prompts_by_tags(["pytest"])
        for prompt in alice_tags:
            await alice.delete_prompt(prompt['guid'])
        for prompt in bob_tags:
            await bob.delete_prompt(prompt['guid'])

    @pytest.fixture(scope='function')
    async def alice(self) -> PublicUserSession:
        """Fixture to provide a public session without a user."""
        return PublicUserSession()

    @pytest.fixture(scope='function')
    async def adrianna(self) -> PublicUserSession:
        """Fixture to provide a public session with an admin user."""
        load_dotenv()
        username = os.getenv("TEST_USERNAME")
        password = os.getenv("TEST_PASSWORD")
        user = User(username, password)
        return PublicUserSession(user)

    @pytest.fixture(scope='function')
    async def bob(self) -> PrivateUserSession:
        """Fixture to provide a private session with a user."""
        load_dotenv()
        username = os.getenv("TEST_USERNAME")
        password = os.getenv("TEST_PASSWORD")
        user = User(username, password)
        return PrivateUserSession(user)

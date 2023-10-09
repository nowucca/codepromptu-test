import pytest
from api.session.session import PublicUserSession, PrivateUserSession

from api.test.base_test import BaseTest


@pytest.mark.asyncio
class TestPromptCreation(BaseTest):

    def setup_method(self, method) -> None:
        """Setup method for test case data generation."""
        self.sample_prompt_data = {
            "content": "This is a sample {input} for testing.",
            "tags": ["sample"],
            "classification": "testing"
        }

    async def test_adrianna_creates_public_prompt(self, adrianna: PublicUserSession):
        """
        Given: Adrianna wants to create a public prompt.
        When: Adrianna provides valid prompt data.
        Then: The prompt should be created successfully and be retrievable by anyone.
        """
        prompt_id = await adrianna.add_prompt(self.sample_prompt_data)
        retrieved_prompt = await adrianna.get_prompt(prompt_id)
        assert retrieved_prompt['content'] == self.sample_prompt_data['content']

    async def test_bob_creates_private_prompt(self, bob: PrivateUserSession):
        """
        Given: Bob wants to create a private prompt.
        When: Bob provides valid prompt data.
        Then: The prompt should be created successfully and only be retrievable by Bob.
        """
        prompt_id = await bob.add_prompt(self.sample_prompt_data)
        retrieved_prompt = await bob.get_prompt(prompt_id)
        assert retrieved_prompt['content'] == self.sample_prompt_data['content']


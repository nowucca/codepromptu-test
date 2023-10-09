import pytest

from api.session.session import PublicUserSession, PrivateUserSession
from api.test.base_test import BaseTest


@pytest.mark.asyncio
class TestPromptVisibility(BaseTest):

    def setup_method(self, method) -> None:
        """Setup method for test case data generation."""
        self.public_prompt_data = {
            "content": "This is a public {input}.",
            "tags": ["public"],
            "classification": "public"
        }
        self.private_prompt_data = {
            "content": "This is a private {input}.",
            "tags": ["private"],
            "classification": "private"
        }

    async def test_public_prompt_visibility(self, adrianna: PublicUserSession, alice: PublicUserSession):
        """
        Given: Adrianna creates a public prompt.
        When: Alice retrieves the list of public prompts.
        Then: ALice should see Adrianna's public prompt.
        """
        public_prompt_guid = await adrianna.add_prompt(self.public_prompt_data)
        alice_prompts = await alice.list_prompts_by_tags(["public"])
        assert public_prompt_guid in [prompt['guid'] for prompt in alice_prompts], \
        f"Alice did not find Adrianna's public prompt. Expected prompt guid: {public_prompt_guid}"

    async def test_private_prompt_invisibility(self, alice: PublicUserSession, bob: PrivateUserSession):
        """
        Given: Bob creates a private prompt.
        When: Alice retrieves the list of prompts.
        Then: Alice should not see Bob's private prompt.
        """
        private_prompt_guid = await bob.add_prompt(self.private_prompt_data)
        alice_prompts = await alice.list_prompts_by_tags(["private"])
        assert private_prompt_guid not in [prompt['guid'] for prompt in alice_prompts]

import asyncio

import pytest

from api.session.session import PublicUserSession, PrivateUserSession
from api.test.base_test import BaseTest


@pytest.mark.asyncio
class TestPublicPromptUpdates(BaseTest):
    """Test scenarios related to the updating of public prompts."""

    @pytest.fixture(autouse=True)
    def setup_public_prompt(self, adrianna: PublicUserSession):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self._setup_public_prompt_async(adrianna))

    async def _setup_public_prompt_async(self, adrianna: PublicUserSession) -> str:
        prompt_data = {"content": "{input} translates to {output}", "tags": ["public", "translation"],
                       "classification": "public_data"}
        prompt_id = await adrianna.add_prompt(prompt_data)
        return prompt_id

    async def test_adrianna_updates_public_prompt_check_update(self, setup_public_prompt, adrianna: PublicUserSession):
        """Given a public prompt, when Adrianna updates its content,
        then the updated content and GUID should match upon retrieval."""
        prompt_id = setup_public_prompt
        new_content = "{input} is converted to {output}"
        await adrianna.update_prompt(prompt_id, {"content": new_content})
        updated_prompt = await adrianna.get_prompt(prompt_id)
        assert updated_prompt['content'] == new_content
        assert updated_prompt['guid'] == prompt_id

    async def test_bob_attempts_update_on_public_prompt(self, setup_public_prompt, adrianna: PublicUserSession,
                                                        bob: PrivateUserSession):
        """Given a public prompt, when Bob attempts to update its content,
        then he should get an error and the prompt GUID should remain unchanged."""
        with pytest.raises(Exception):  # Assuming the API throws an error for unauthorized update attempts
            await bob.update_prompt(setup_public_prompt, {"content": "New content by Bob"})

        unchanged_prompt = await adrianna.get_prompt(setup_public_prompt)
        assert unchanged_prompt['guid'] == setup_public_prompt

    async def test_update_non_existent_public_prompt(self, adrianna: PublicUserSession):
        """Given a non-existent public prompt GUID, when Adrianna tries to update it,
        then she should get an error."""
        non_existent_guid = "non-existent-guid"
        with pytest.raises(Exception):  # Assuming the API throws an error for invalid prompt GUID
            await adrianna.update_prompt(non_existent_guid, {"content": "Trying to update non-existent content"})

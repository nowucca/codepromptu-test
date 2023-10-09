import pytest

from api.session.session import PrivateUserSession, PublicUserSession


@pytest.mark.asyncio
class TestPrivatePromptCreationRetrieval:
    """Test scenarios related to the creation of private prompts and their retrieval."""

    @pytest.fixture
    async def setup_private_prompt(self, bob: PrivateUserSession) -> str:
        prompt_data = {"content": "{input} becomes {output}", "tags": ["private", "example"],
                       "classification": "personal"}
        prompt_id = await bob.add_prompt(prompt_data)
        yield prompt_id

    async def test_bob_creates_private_prompt_retrieved_by_him(self, setup_private_prompt, bob: PrivateUserSession):
        """Given a private prompt created by Bob, when he retrieves it, then the retrieved prompt
        should match the created prompt's GUID."""
        prompt_id = setup_private_prompt
        retrieved_prompt = await bob.get_prompt(prompt_id)
        assert retrieved_prompt['guid'] == prompt_id

    async def test_alice_fails_to_retrieve_bob_private_prompt(self, setup_private_prompt, alice: PublicUserSession):
        """Given a private prompt created by Bob, when Alice attempts to retrieve it, then she should get an error."""
        with pytest.raises(Exception):  # assuming the API throws an error for unauthorized access
            await alice.get_prompt(setup_private_prompt)

    async def test_retrieve_non_existent_private_prompt(self, bob: PrivateUserSession):
        """Given a non-existent private prompt GUID, when Bob tries to retrieve it, then he should get an error."""
        non_existent_guid = "non-existent-guid"
        with pytest.raises(Exception):  # assuming the API throws an error for invalid prompt GUID
            await bob.get_prompt(non_existent_guid)

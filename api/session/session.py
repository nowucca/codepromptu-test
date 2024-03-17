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

    async def add_tag_to_prompt(self, guid: str, tag: str) -> None:
        await self.client.add_tag_to_prompt(guid, tag)

    async def remove_tag_from_prompt(self, guid: str, tag: str) -> None:
        await self.client.remove_tag_from_prompt(guid, tag)

    async def list_prompts_by_tags(self, tags: list[str]) -> list[dict]:
        return await self.client.list_prompts_by_tags(tags)


class PrivateUserSession(PublicUserSession):
    client_cls = PrivatePromptClient

    def __init__(self, user: User):
        if not user:
            raise ValueError("A valid user object is required for PrivateUserSession.")
        super().__init__(user)

from typing import List, Optional

import aiohttp
from dotenv import load_dotenv
import os
load_dotenv()

from api.client.core_client_interface import CoreClientInterface
from api.client.user import User


class PublicClient(CoreClientInterface):
    BASE_URL = os.getenv("BASE_URL")
    TEST_USERNAME = os.getenv('TEST_USERNAME')

    def __init__(self, user: Optional[User] = None):
        self.auth = None
        if user:
            self.auth = user.get_basic_auth()
        self._discriminator_tag = "pytest-" + self.TEST_USERNAME

    async def _ensure_discriminator_tag(self, prompt_data):
        prompt_data["tags"] = list(set(prompt_data.get("tags", []) + [self._discriminator_tag]))  # Ensuring "pytest" tag

    async def add_prompt(self, prompt_data: dict[str, any]) -> str:
        async with aiohttp.ClientSession() as session:
            await self._ensure_discriminator_tag(prompt_data)
            resp = await session.post(f'{self.BASE_URL}/public/prompt/', json=prompt_data, auth=self.auth)
            return await resp.text()

    async def list_prompts(self, skip: int = 0, limit: int = 10) -> List[dict]:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(f'{self.BASE_URL}/public/prompt/?skip={skip}&limit={limit}')
            return await resp.json()

    async def delete_prompt(self, guid) -> None:
        async with aiohttp.ClientSession() as session:
            resp = await session.delete(f'{self.BASE_URL}/public/prompt/{guid}', auth=self.auth)
            if resp.status != 204:
                raise Exception(f"Failed to delete prompt with guid: {guid}")

    async def update_prompt(self, guid: str, updated_data: dict[str, any]) -> None:
        async with aiohttp.ClientSession() as session:
            await self._ensure_discriminator_tag(updated_data)
            resp = await session.put(f'{self.BASE_URL}/public/prompt/{guid}', json=updated_data, auth=self.auth)
            if resp.status != 204:
                raise Exception(f"Failed to update prompt with guid: {guid}")

    async def get_prompt(self, guid: str) -> dict[str, any]:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(f'{self.BASE_URL}/public/prompt/{guid}')
            return await resp.json()

    async def search_prompts(self, query: str) -> List[dict]:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(f'{self.BASE_URL}/public/prompt/search/?query={query}')
            return await resp.json()

    async def list_prompts_by_tags(self, tags: List[str]) -> List[dict]:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(f'{self.BASE_URL}/public/prompt/tags/?tags={",".join(tags)}')
            return await resp.json()

    async def list_prompts_by_classification(self, classification: str) -> List[dict]:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(f'{self.BASE_URL}/public/prompt/classification/{classification}')
            return await resp.json()

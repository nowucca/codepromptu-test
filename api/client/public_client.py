from typing import List, Optional

import aiohttp

from api.client.user import User


class PublicClient:
    BASE_URL = 'YOUR_API_ENDPOINT_HERE'  # replace with the actual base URL

    def __init__(self, user: Optional[User] = None):
        self.auth = None
        if user:
            self.auth = user.get_basic_auth()

    async def add_prompt(self, prompt_data: dict[str, any]):
        async with aiohttp.ClientSession() as session:
            prompt_data["tags"] = list(set(prompt_data.get("tags", []) + ["pytest"]))  # Ensuring "pytest" tag
            resp = await session.post(f'{self.BASE_URL}/public/prompt/', json=prompt_data, auth=self.auth)
            return await resp.json()

    async def list_prompts(self, skip: int = 0, limit: int = 10):
        async with aiohttp.ClientSession() as session:
            resp = await session.get(f'{self.BASE_URL}/public/prompt/?skip={skip}&limit={limit}')
            return await resp.json()

    async def delete_prompt(self, guid):
        async with aiohttp.ClientSession() as session:
            resp = await session.delete(f'{self.BASE_URL}/public/prompt/{guid}', auth=self.auth)
            return resp.status

    async def update_prompt(self, guid, updated_data):
        async with aiohttp.ClientSession() as session:
            updated_data["tags"] = list(set(updated_data.get("tags", []) + ["pytest"]))  # Ensuring "pytest" tag
            resp = await session.put(f'{self.BASE_URL}/public/prompt/{guid}', json=updated_data, auth=self.auth)
            return await resp.json()

    async def get_prompt(self, guid):
        async with aiohttp.ClientSession() as session:
            resp = await session.get(f'{self.BASE_URL}/public/prompt/{guid}')
            return await resp.json()

    async def search_prompts(self, query: str):
        async with aiohttp.ClientSession() as session:
            resp = await session.get(f'{self.BASE_URL}/public/prompt/search/?query={query}')
            return await resp.json()

    async def list_prompts_by_tags(self, tags: List[str]):
        async with aiohttp.ClientSession() as session:
            resp = await session.get(f'{self.BASE_URL}/public/prompt/tags/?tags={",".join(tags)}')
            return await resp.json()

    async def list_prompts_by_classification(self, classification: str) -> str:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(f'{self.BASE_URL}/public/prompt/classification/{classification}')
            return await resp.json()

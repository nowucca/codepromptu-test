from typing import List

import aiohttp

from api.client.user import User


class PrivatePromptClient:
    BASE_URL = 'YOUR_API_ENDPOINT_HERE'  # replace with the actual base URL

    def __init__(self, user: User):
        if not user:
            raise ValueError("A valid user object is required for PrivatePromptClient.")
        self._auth = user.get_basic_auth()

    async def add_prompt(self, prompt_data: dict[str, any]):
        async with aiohttp.ClientSession() as session:
            prompt_data["tags"] = list(set(prompt_data.get("tags", []) + ["pytest"]))  # Ensuring "pytest" tag
            resp = await session.post(f'{self.BASE_URL}/private/prompt/', json=prompt_data, auth=self._auth)
            return await resp.json()

    async def list_prompts(self, skip: int = 0, limit: int = 10):
        async with aiohttp.ClientSession() as session:
            resp = await session.get(f'{self.BASE_URL}/private/prompt/?skip={skip}&limit={limit}', auth=self._auth)
            return await resp.json()

    async def delete_prompt(self, guid: str):
        async with aiohttp.ClientSession() as session:
            resp = await session.delete(f'{self.BASE_URL}/private/prompt/{guid}', auth=self._auth)
            return resp.status

    async def update_prompt(self, guid, updated_data: dict[str, any]):
        async with aiohttp.ClientSession() as session:
            updated_data["tags"] = list(set(updated_data.get("tags", []) + ["pytest"]))  # Ensuring "pytest" tag
            resp = await session.put(f'{self.BASE_URL}/private/prompt/{guid}', json=updated_data, auth=self._auth)
            return await resp.json()

    async def search_prompts(self, query: str):
        async with aiohttp.ClientSession() as session:
            resp = await session.get(f'{self.BASE_URL}/private/prompt/search?query={query}', auth=self._auth)
            return await resp.json()

    async def list_prompts_by_tag(self, tags: List[str]):
        async with aiohttp.ClientSession() as session:
            resp = await session.get(f'{self.BASE_URL}/private/prompt/tags/?tags={",".join(tags)}')
            return await resp.json()

    async def list_prompts_by_classification(self, classification):
        async with aiohttp.ClientSession() as session:
            resp = await session.get(f'{self.BASE_URL}/private/prompt/classification/{classification}/',
                                     auth=self._auth)
            return await resp.json()

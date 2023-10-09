from typing import List, Optional, Protocol


class CoreClientInterface(Protocol):

    async def add_prompt(self, prompt_data: dict[str, any]) -> str:
        ...

    async def list_prompts(self, skip: int = 0, limit: int = 10) -> List[dict]:
        ...

    async def delete_prompt(self, guid: str) -> None:
        ...

    async def update_prompt(self, guid: str, updated_data: dict[str, any]) -> None:
        ...

    async def get_prompt(self, guid: str) -> dict[str, any]:
        ...

    async def search_prompts(self, query: str) -> List[dict]:
        ...

    async def list_prompts_by_tags(self, tags: List[str]) -> List[dict]:
        ...

    # Additional methods as needed
    async def list_prompts_by_classification(self, classification: str) -> List[dict]:
        ...

from app.repositories.search_repository import SearchRepository


class SearchService:
    def __init__(self, repository: SearchRepository):
        self.repository = repository

    async def search_events(
        self,
        q: str,
        page: int = 1,
        page_size: int = 20,
    ) -> dict:
        q = q.strip()

        if not q:
            raise ValueError("q must not be empty.")

        if page < 1:
            raise ValueError("page must be greater than or equal to 1.")

        if page_size < 1 or page_size > 100:
            raise ValueError("page_size must be between 1 and 100.")

        total = await self.repository.count_events(q)

        items = await self.repository.search_events(
            q=q,
            page=page,
            page_size=page_size,
        )

        total_pages = (total + page_size - 1) // page_size

        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages,
        }
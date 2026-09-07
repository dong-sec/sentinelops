from pydantic import BaseModel, ConfigDict

from app.schemas.events import EventListItem


class EventSearchResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[EventListItem]
    page: int
    page_size: int
    total: int
    total_pages: int
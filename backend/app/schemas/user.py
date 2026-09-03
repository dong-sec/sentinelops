from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    email: str | None = None
    role: str
    status: str


class UserCreateRequest(BaseModel):
    username: str
    email: str | None = None
    password: str
    role: str


class UserUpdateRequest(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
    role: str | None = None
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional


class URLCreate(BaseModel):
    url: HttpUrl = Field(..., description="Полный URL, который нужно сократить")


class URLOut(BaseModel):
    id: int
    short_id: str
    full_url: str
    clicks: int
    created_at: str


class URLInfo(BaseModel):
    short_id: str
    full_url: str
    clicks: int
    created_at: str

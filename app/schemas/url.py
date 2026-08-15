from datetime import datetime
from pydantic import BaseModel, HttpUrl, Field, ConfigDict

class URLBase(BaseModel):
    target_url : HttpUrl 

class URLCreate(URLBase):
    custom_alias: str | None = Field(default=None, max_length=10)
    expires_in_days: int | None = Field(default=None, ge=1)

class URLResponse(URLBase):
    short_code: str
    short_url: str
    created_at: datetime
    expires_at: datetime | None
    is_active: bool
    model_config = ConfigDict(from_attributes=True)

class URLStats(URLResponse):
    clicks:int

from typing import Optional

from pydantic import BaseModel


class TweetDto(BaseModel):
    city: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "city": "Campinas",
            }
        }

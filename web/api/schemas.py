"""Request, response schemas for application endpoints
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from web import constants


class PairItemSchema(BaseModel):
    query: str
    location_id: int


class GetPairSchema(BaseModel):
    id: UUID
    next_run: datetime
    check_every: int
    pair: PairItemSchema


class CreatePairSchema(PairItemSchema):
    check_every: Optional[int] = constants.CHECK_EVERY


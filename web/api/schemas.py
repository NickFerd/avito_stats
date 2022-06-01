"""Request, response schemas for application endpoints
"""
from datetime import datetime
from typing import Optional, List, Union
from uuid import UUID

from pydantic import BaseModel, HttpUrl

from config import settings

__all__ = [
    'GetPairSchema',
    'CreatePairSchema',
    'ResultsRequestSchema',
    'StatsResponseSchema',
    'TopAdsResponseSchema',
]


class PairItemSchema(BaseModel):
    query: str
    location: str


class StatItemSchema(BaseModel):
    """Schema for counting statistics of pair at particular moment
    """
    moment: datetime
    count: int


class AdItemSchema(BaseModel):
    """Schema of one advertisement"""
    ad_id: int
    url: HttpUrl
    title: str
    price: Union[float, int]


class AdList(BaseModel):
    moment: datetime
    ads: List[AdItemSchema]


class CreatePairSchema(PairItemSchema):
    check_every_minute: Optional[int] = settings.default_check_every_minute


class GetPairSchema(CreatePairSchema):
    id: UUID


class ResultsRequestSchema(BaseModel):
    """Schema for getting stats of particular pair"""
    pair_id: UUID
    datetime_from: datetime
    datetime_to: datetime


class StatsResponseSchema(ResultsRequestSchema):
    stats: List[StatItemSchema]


class TopAdsResponseSchema(ResultsRequestSchema):
    top_ads: List[AdList]


"""Request, response schemas for application endpoints
"""
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, HttpUrl

from web import constants

__all__ = [
    'GetPairSchema',
    'CreatePairSchema',
    'ResultsRequestSchema',
    'StatsResponseSchema',
    'TopAdsResponseSchema',
    'LocationRequestSchema',
    'LocationResponseSchema'
]


class PairItemSchema(BaseModel):
    query: str
    location_id: int


class StatItemSchema(BaseModel):
    """Schema for counting statistics of pair at particular moment
    """
    moment: datetime
    count: int


class AdItemSchema(BaseModel):
    """Schema of one advertisement"""
    ad_id: int
    url: HttpUrl
    moment: datetime


class GetPairSchema(BaseModel):
    id: UUID
    last_run: datetime
    check_every: int
    pair: PairItemSchema


class CreatePairSchema(PairItemSchema):
    check_every_minute: Optional[int] = constants.CHECK_EVERY


class ResultsRequestSchema(BaseModel):
    """Schema for getting stats of particular pair"""
    pair_id: UUID
    datetime_from: datetime
    datetime_to: datetime


class StatsResponseSchema(ResultsRequestSchema):
    stats: List[StatItemSchema]


class TopAdsResponseSchema(ResultsRequestSchema):
    top_ads: List[AdItemSchema]


class LocationRequestSchema(BaseModel):
    location_name: str


class LocationResponseSchema(LocationRequestSchema):
    location_id: int

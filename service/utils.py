"""Utility functions and objects
"""

from dataclasses import dataclass
import uuid
from datetime import datetime
from typing import List


@dataclass
class AdItem:
    """Represent one advertisement"""
    ad_id: int
    url: str
    title: str
    price: float


@dataclass
class StatItem:
    """Represents one stat item in db"""
    pair_id: str
    moment: datetime
    count: int
    ads: List[AdItem]


@dataclass
class PairItem:
    """Represents one pair"""
    id: uuid.UUID
    query: str
    location: str
    check_every_minute: int


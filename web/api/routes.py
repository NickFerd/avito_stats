"""Application routes"""

from uuid import UUID, uuid4

from fastapi import APIRouter

from web.api import schemas

router = APIRouter()


@router.post('/add', response_model=schemas.GetPairSchema)
async def add_pair(payload: schemas.CreatePairSchema):
    """Add a new pair to tracking schedule
    """
    pass


@router.get('/stop/{pair_id}')
async def stop_tracking_pair(pair_id: UUID):
    pass


@router.post('/stat', response_model=schemas.StatsResponseSchema)
async def fetch_count_stats(payload: schemas.ResultsRequestSchema):
    pass


@router.post('/top', response_model=schemas.TopAdsResponseSchema)
async def fetch_top_ads(payload: schemas.ResultsRequestSchema):
    pass


@router.post('/location', response_model=schemas.LocationResponseSchema)
async def fetch_location_id(payload: schemas.LocationRequestSchema):
    pass

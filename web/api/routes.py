"""Application routes"""

from uuid import UUID, uuid4

from fastapi import APIRouter

from web.api.schemas import (
    CreatePairSchema,
    GetPairSchema
)
router = APIRouter()


@router.post('/add', response_model=GetPairSchema)
async def add_pair(payload: CreatePairSchema):
    """View function to add a new pair to tracking schedule
    If pair (query, location) already exists, TODO """
    print('adding pair')
    return {'status': 'OK'}


@router.get('/stop/{pair_id}')
async def stop_tracking_pair(pair_id: UUID):
    print(f'Stop tracking pair: {pair_id}')
    return {'status': 'OK'}


@router.post('/stat')  # todo add response schema
async def fetch_count_stats():
    pass


@router.post('/top')  # todo add response schema
async def fetch_top_ads():
    pass


@router.post('/location')  # todo add request/response schema
async def fetch_location_id():
    pass

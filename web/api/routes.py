"""Application routes"""

from uuid import UUID

from fastapi import APIRouter

router = APIRouter()


@router.get('/stop/{pair_id}')
async def stop_tracking_pair(pair_id: UUID):
    print(f'Stop tracking pair: {pair_id}')
    return {'status': 'OK'}


@router.post('/add')
async def add_pair():
    print('adding pair')
    return {'status': 'OK'}

"""Application routes"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import JSONResponse

from service import exceptions as exc
from service.stats_service import StatsService
from web.api import schemas, deps

router = APIRouter()


@router.post('/add', response_model=schemas.GetPairSchema)
def add_pair(payload: schemas.CreatePairSchema,
             service: StatsService = Depends(deps.init_service),
             valid_locations: dict = Depends(deps.valid_locations)):
    """Add a new pair to tracking schedule
    """
    location = payload.location.lower()
    query = payload.query.lower()

    # Validate location
    if location not in valid_locations:
        raise HTTPException(status_code=400, detail="Invalid location")

    pair_info = service.add_pair(query=query,
                                 location=location,
                                 check_every_minute=payload.check_every_minute)
    return pair_info


@router.get('/stop/{pair_id}')
def stop_tracking_pair(pair_id: UUID,
                       service: StatsService = Depends(deps.init_service)):
    """Remove pair from tracking schedule
    """
    try:
        service.stop_tracking_pair(pair_id=pair_id)
    except exc.PairNotFound:
        raise HTTPException(status_code=404, detail="Pair not found")

    return JSONResponse({"result": "success"})


@router.post('/stat', response_model=schemas.StatsResponseSchema)
def fetch_count_stats(payload: schemas.ResultsRequestSchema):
    pass


@router.post('/top', response_model=schemas.TopAdsResponseSchema)
def fetch_top_ads(payload: schemas.ResultsRequestSchema):
    pass




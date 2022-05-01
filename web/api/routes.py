"""Application routes"""
from random import randint
from uuid import UUID

from celery.schedules import schedule
from fastapi import APIRouter
from starlette.responses import JSONResponse
from redbeat import RedBeatSchedulerEntry

from web.api import schemas
from scheduler import celery

router = APIRouter()


@router.post('/add', response_model=schemas.GetPairSchema)
def add_pair(payload: schemas.CreatePairSchema):
    """Add a new pair to tracking schedule
    """
    print(payload)
    print(type(payload))


@router.get('/stop/{pair_id}')
def stop_tracking_pair(pair_id: UUID):
    """Remove pair from tracking schedule
    """
    pass


@router.post('/stat', response_model=schemas.StatsResponseSchema)
def fetch_count_stats(payload: schemas.ResultsRequestSchema):
    pass


@router.post('/top', response_model=schemas.TopAdsResponseSchema)
def fetch_top_ads(payload: schemas.ResultsRequestSchema):
    pass


@router.post('/location', response_model=schemas.LocationResponseSchema)
def fetch_location_id(payload: schemas.LocationRequestSchema):
    pass


@router.get('/task')
def trigger_task():
    task = celery.simple_task.delay()
    return JSONResponse({"task_id": task.id})


@router.get('/set_periodic')
def set_periodic_task():
    task_name = str(randint(1, 20))
    # celery.app.conf.beat_schedule[task_name] = {
    #     "task": 'scheduler.celery.simple_task',
    #     'schedule': 60,
    # }
    # key = celery.app.add_periodic_task(schedule=30,
    #                                    sig=celery.simple_task.s(),
    #                                    name=task_name)
    # print(celery.app.conf.beat_schedule)
    interval = schedule(run_every=60)
    entry = RedBeatSchedulerEntry(task_name,
                                  'scheduler.celery.simple_task',
                                  interval,
                                  app=celery.app)
    entry.save()
    print(entry.next)
    print(entry.name)
    print(entry.enabled)
    return JSONResponse({"task_name": task_name})

"""Web app initialization
"""
from fastapi import FastAPI

from web.api.routes import router
from database import init_db

app = FastAPI()

app.include_router(router)


@app.on_event('startup')
def startup_callback():
    """Execute on startup"""
    init_db()

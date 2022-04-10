"""Web app initialization
"""
from fastapi import FastAPI

from web.api.routes import router


app = FastAPI()

app.include_router(router)


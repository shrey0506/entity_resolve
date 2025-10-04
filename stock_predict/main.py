from fastapi import FastAPI
from app.view.view import router

app = FastAPI()

app.include_router(router)
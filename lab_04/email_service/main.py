from fastapi import FastAPI
from api.router import router
from core.init_db import init_db

app = FastAPI()
app.include_router(router)

@app.on_event("startup")
def on_startup():
    init_db()
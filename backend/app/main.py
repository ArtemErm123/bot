from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(title="Bot Backend")
app.include_router(router, prefix="/api")

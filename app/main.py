from fastapi import FastAPI
from authentication.api.router import router as auth_router
from files.api.router import router as files_router

app = FastAPI(title="Cloud API - Redis & S3")
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(files_router, prefix="/files", tags=["files"])

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.router import api_router
from backend.core.config import settings
from backend.core.scheduler import shutdown_scheduler, start_scheduler
from backend.data.layout import get_local_data_layout


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_local_data_layout().ensure_directories()
    start_scheduler()
    yield
    shutdown_scheduler()


app = FastAPI(
    title=settings.app.project_name,
    openapi_url=f"{settings.app.api_v1_prefix}/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.origins,
    allow_credentials=settings.cors.allow_credentials,
    allow_methods=settings.cors.allow_methods,
    allow_headers=settings.cors.allow_headers,
)


@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "System is running"}


app.include_router(api_router, prefix=settings.app.api_v1_prefix)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app=app,
        host=settings.app.host,
        port=settings.app.port,
        reload=settings.app.reload,
    )

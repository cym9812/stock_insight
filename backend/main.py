from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api import endpoints_data, endpoints_agent
from backend.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境建议限制为具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "System is running"}


# Include routers
app.include_router(
    endpoints_data.router,
    prefix=f"{settings.API_V1_STR}/data",
    tags=["data"]
)
app.include_router(
    endpoints_agent.router,
    prefix=f"{settings.API_V1_STR}/agent",
    tags=["agent"]
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="0.0.0.0", port=18000, reload=True)

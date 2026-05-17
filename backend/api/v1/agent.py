from fastapi import APIRouter

from backend.schemas.agent import ChatResponse
from backend.services.agent_service import AgentService

router = APIRouter()
agent_service = AgentService()


@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(message: str):
    return agent_service.chat(message)

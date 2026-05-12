from fastapi import APIRouter

router = APIRouter()


@router.post("/chat")
async def chat_with_agent(message: str):
    """
    与股票分析 Agent 对话接口
    """
    return {
        "agent_response": f"You said: {message}. This is a placeholder response from the Stock Agent."
    }

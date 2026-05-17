from pydantic import BaseModel


class ChatResponse(BaseModel):
    agent_response: str

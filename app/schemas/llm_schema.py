from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(..., examples=["system", "user", "assistant"])
    content: str


class LlmChatRequest(BaseModel):
    messages: list[ChatMessage]
    max_tokens: int | None = Field(default=None, ge=1, le=2048)
    temperature: float | None = Field(default=None, ge=0.0, le=2.0)
    model: str | None = None


class LlmChatResponse(BaseModel):
    model: str
    content: str
    finish_reason: str | None = None
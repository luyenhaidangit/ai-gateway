import httpx

from app.core.config import Settings
from app.core.exceptions import ServiceUnavailableError
from app.schemas.llm_schema import LlmChatRequest
from app.schemas.llm_schema import LlmChatResponse


class LlmService:
    def __init__(self, settings: Settings):
        self.settings = settings

    async def chat(self, request: LlmChatRequest) -> LlmChatResponse:
        payload = {
            "model": request.model or self.settings.VLLM_MODEL_NAME,
            "messages": [message.model_dump() for message in request.messages],
            "max_tokens": request.max_tokens or self.settings.VLLM_MAX_TOKENS,
            "temperature": (
                request.temperature
                if request.temperature is not None
                else self.settings.VLLM_TEMPERATURE
            ),
        }

        base_url = self.settings.VLLM_BASE_URL.rstrip("/")
        timeout = httpx.Timeout(self.settings.VLLM_TIMEOUT_SECONDS)

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(f"{base_url}/v1/chat/completions", json=payload)
                response.raise_for_status()
        except httpx.HTTPError as exc:
            raise ServiceUnavailableError("vLLM") from exc

        data = response.json()
        choice = data["choices"][0]
        message = choice.get("message", {})

        return LlmChatResponse(
            model=data.get("model", payload["model"]),
            content=message.get("content", ""),
            finish_reason=choice.get("finish_reason"),
        )

    async def is_healthy(self) -> bool:
        base_url = self.settings.VLLM_BASE_URL.rstrip("/")
        timeout = httpx.Timeout(10.0)

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(f"{base_url}/v1/models")
                response.raise_for_status()
            return True
        except httpx.HTTPError:
            return False
import httpx
from pydantic import BaseModel, ConfigDict, Field
from pydantic_core import to_jsonable_python
from fastapi import FastAPI, HTTPException
from pydantic_ai import Agent, ModelMessagesTypeAdapter, RunContext
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider

app = FastAPI(
    title="Users Agent",
    version="0.1.0",
    description="Testserver. Das Modell llama3.2 ruft die User-API auf. Nur lesen: Liste und ein User.",
)

USERS_API = "http://127.0.0.1:8000/api/v1"

model = OllamaModel(
    "llama3.2",
    provider=OllamaProvider(base_url="http://127.0.0.1:11434/v1", api_key="ollama"),
)

agent = Agent(
    model,
    system_prompt=(
        "Du beantwortest Fragen zu Usern. "
        "Die Daten kommen nur aus list_users und get_user. "
        "Erfinde keine User und ändere nichts."
    ),
)


async def read_users_api(path: str) -> str:
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{USERS_API}{path}", timeout=5.0)
    except httpx.HTTPError as e:
        return f"Users API unreachable: {e}"
    if res.status_code == 404:
        return "User not found"
    return res.text


@agent.tool
async def list_users(ctx: RunContext) -> str:
    """Liest alle User. GET /api/v1/users. Kein Filter."""
    return await read_users_api("/users")


@agent.tool
async def get_user(ctx: RunContext, user_id: int) -> str:
    """Liest einen User. Die Id steht im Pfad. GET /api/v1/users/{user_id}."""
    return await read_users_api(f"/users/{user_id}")


class ChatRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={"example": {"prompt": "Wer hat die Id 1?"}}
    )

    prompt: str = Field(description="Die Frage an das Modell.")
    message_history: list[dict] | None = Field(
        default=None,
        description="Verlauf aus der letzten Antwort. Beim ersten Aufruf weglassen.",
    )


class ChatResponse(BaseModel):
    response: str = Field(description="Antwort des Modells.")
    message_history: list[dict] = Field(
        description="Vollständiger Verlauf. Beim nächsten Aufruf wieder mitgeben.",
    )


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Schickt die Frage an llama3.2. Das Modell ruft nur die zwei Lese-Werkzeuge auf."""
    try:
        raw = request.message_history or []
        real = [item for item in raw if isinstance(item, dict) and "kind" in item]
        history = ModelMessagesTypeAdapter.validate_python(real) if real else []
        result = await agent.run(request.prompt, message_history=history)
        return ChatResponse(
            response=result.output,
            message_history=to_jsonable_python(result.all_messages()),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

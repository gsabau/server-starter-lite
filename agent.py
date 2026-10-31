import os

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider
from session_agent import SessionAgent
from tools import get_user, get_weather, list_users


def make_agent():
    load_dotenv()

    model = OllamaModel(
        os.environ.get("MODEL_NAME", "llama3.2"),
        provider=OllamaProvider(
            base_url=os.environ.get("MODEL_BASE_URL", "http://127.0.0.1:11434/v1"),
            api_key=os.environ.get("MODEL_API_KEY", "ollama"),
        ),
    )

    agent = Agent(
        model,
        system_prompt=(
            "Du beantwortest Fragen zu Usern und zum Wetter. "
            "User-Daten kommen nur aus list_users und get_user. "
            "Wetter kommt nur aus get_weather. "
            "Erfinde keine User und kein Wetter."
        ),
        tools=[list_users, get_user, get_weather],
    )

    return SessionAgent(agent)

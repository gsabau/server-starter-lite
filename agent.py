import os

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider
from session_agent import SessionAgent
from tools import get_user, get_weather, list_users

SYSTEM_PROMPT = """You answer questions about users and the weather. You know no data yourself.
Call a tool for every question. Answer only from the tool result.
- list_users: for several users, counts and groups. Its only argument is role, to filter by one role. It has no argument for a number of users.
- get_user: for one user by id.
- get_weather: for the weather in a city.
If a tool returns an error, report the error and stop.
Answer in the language of the question.
"""


def make_agent():
    load_dotenv()

    model = OllamaModel(
        os.environ.get("MODEL_NAME", "qwen2.5:1.5b"),
        provider=OllamaProvider(
            base_url=os.environ.get("MODEL_BASE_URL", "http://127.0.0.1:11434/v1"),
            api_key=os.environ.get("MODEL_API_KEY", "qwen2.5:1.5b"),
        ),
    )

    agent = Agent(
        model,
        system_prompt=SYSTEM_PROMPT,
        tools=[list_users, get_user, get_weather],
        model_settings={"temperature": 0.0},
    )

    return SessionAgent(agent)

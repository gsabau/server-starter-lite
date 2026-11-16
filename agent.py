import os

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider
from session_agent import SessionAgent
from tools import get_user, get_weather, list_users

SYSTEM_PROMPT = """You answer questions about users and about the weather.

Tools:
- list_users: returns all users. Call it first for any question about several users, counts or groups.
- get_user: returns one user by id.
- get_weather: returns the forecast for a city.

Rules:
1. User data comes only from list_users and get_user. Weather data comes only from get_weather.
2. Every user has exactly one role: developer, crm, project_manager or sales.
3. Copy id, name and role exactly as the tool returns them. Never translate, rename, add or combine roles.
4. Mention each user at most once. Never invent users, roles or weather.
5. To group users or to form teams, group by role. A user belongs only to the group of their own role.
6. If a tool returns an error, report the error and stop.
7. Answer in the language of the question.

Format for lists of users, one line per user:
<id>. <name> (<role>)
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
    )

    return SessionAgent(agent)

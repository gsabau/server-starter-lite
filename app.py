import os

import flet as ft
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider

from tools import get_user, get_weather, list_users

load_dotenv()

model = OllamaModel(
    os.environ.get("MODEL_NAME", "llama3.2"),
    provider=OllamaProvider(
        base_url=os.environ.get("MODEL_BASE_URL", "http://127.0.0.1:11434/v1"),
        api_key=os.environ.get("MODEL_API_KEY", "ollama"),
    )
)

agent = Agent(
    model,
    system_prompt=(
        "Du beantwortest Fragen zu Usern und zum Wetter. "
        "User-Daten kommen nur aus list_users und get_user. "
        "Wetter kommt nur aus get_weather. "
        "Erfinde keine User und kein Wetter."
    ),
    tools=[list_users, get_user, get_weather]
)

async def main(page: ft.Page):
    page.title = "Users"
    history = []
    chat = ft.ListView(expand=True, auto_scroll=True, spacing=16, padding=12)
    prompt = ft.TextField(hint_text="Frage", expand=True, autofocus=True)

    async def send(e):
        text = (prompt.value or "").strip()
        if not text:
            return
        prompt.value = ""
        prompt.disabled = True
        send_button.disabled = True
        loading = ft.Row([ft.ProgressRing(width=20, height=20), ft.Text("Suche…")])
        chat.controls.append(
            ft.Text(text, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.RIGHT)
        )
        chat.controls.append(loading)
        page.update()
        try:
            result = await agent.run(text, message_history=history)
            history[:] = result.all_messages()
            reply = result.output
        except Exception as err:
            reply = str(err)
        chat.controls.remove(loading)
        chat.controls.append(ft.Text(reply, text_align=ft.TextAlign.LEFT))
        prompt.disabled = False
        send_button.disabled = False
        page.update()

    prompt.on_submit = send
    send_button = ft.Button("Senden", on_click=send)
    page.add(chat, ft.Row([prompt, send_button]))


if __name__ == "__main__":
    ft.run(main, view=ft.AppView.WEB_BROWSER)

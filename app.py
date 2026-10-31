import flet as ft

from agent import make_agent


async def main(page: ft.Page):
    page.title = "Users"
    agent = make_agent()
    history = []
    token_count = ft.TextSpan(
        "0",
        style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN),
    )
    tokens = ft.Text(
        spans=[
            ft.TextSpan("Tokens "),
            token_count,
            ft.TextSpan(" it's free!"),
        ],
        text_align=ft.TextAlign.LEFT,
    )
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
            token_count.text = str(agent.total)
        except Exception as err:
            reply = str(err)
        chat.controls.remove(loading)
        chat.controls.append(ft.Text(reply, text_align=ft.TextAlign.LEFT))
        prompt.disabled = False
        send_button.disabled = False
        page.update()

    prompt.on_submit = send
    send_button = ft.Button("Senden", on_click=send)
    page.add(tokens, chat, ft.Row([prompt, send_button]))


if __name__ == "__main__":
    ft.run(main, view=ft.AppView.WEB_BROWSER)

import reflex as rx
from biodiagnostico_app.styles import BUTTON_PRIMARY_STYLE, Color

def premium_button(text: str, icon: str = None):
    return rx.button(
        rx.hstack(
            rx.icon(tag=icon) if icon else rx.spacer(),
            rx.text(text),
            spacing="2",
        ),
        on_click=lambda: rx.console_log(f"Clicked {text}"),
        style=BUTTON_PRIMARY_STYLE,
    )

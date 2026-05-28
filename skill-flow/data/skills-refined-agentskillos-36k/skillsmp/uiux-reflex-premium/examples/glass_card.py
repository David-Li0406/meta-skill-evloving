import reflex as rx
from biodiagnostico_app.styles import CARD_STYLE, GLASS_STYLE, Typography, Spacing

def glass_card_example(title: str, content: str):
    return rx.box(
        rx.vstack(
            rx.text(title, style=Typography.H4),
            rx.text(content, style=Typography.BODY_SECONDARY),
            align_items="start",
            spacing=Spacing.SM,
        ),
        style={
            **CARD_STYLE,
            **GLASS_STYLE,
            "padding": Spacing.LG,
            "width": "100%",
        }
    )

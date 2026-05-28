import reflex as rx
from typing import List, Any

# Supondo que você tenha seus estilos importados
# from ...styles import Color, Spacing

def status_badge(status: str):
    """Retorna um badge colorido baseado no status."""
    badges = {
        "concluido": ("green", "Concluído"),
        "pendente": ("yellow", "Pendente"),
        "erro": ("red", "Erro"),
    }
    color, label = badges.get(status.lower(), ("gray", status))
    return rx.badge(label, color_scheme=color, variant="soft")

def data_table_row(item: Any, index: int):
    """Renderiza uma linha da tabela com zebrado suave."""
    bg_color = rx.cond(
        index % 2 == 0,
        "transparent",
        rx.color("gray", 2)
    )
    
    return rx.table.row(
        rx.table.cell(item.nome, color=rx.color("slate", 11), font_weight="500"),
        rx.table.cell(item.data),
        rx.table.cell(status_badge(item.status)),
        rx.table.cell(
            rx.hstack(
                rx.icon_button("pencil", variant="ghost", size="1"),
                rx.icon_button("trash", variant="ghost", color_scheme="red", size="1"),
            )
        ),
        bg=bg_color,
        _hover={"bg": rx.color("gray", 3)},
    )

def advanced_data_table(data: List[Any]):
    """
    Tabela com cabeçalho fixo, scroll e design premium.
    Use dentro de um container com tamanho definido.
    """
    return rx.scroll_area(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Nome"),
                    rx.table.column_header_cell("Data"),
                    rx.table.column_header_cell("Status"),
                    rx.table.column_header_cell("Ações"),
                ),
            ),
            rx.table.body(
                rx.foreach(
                    data,
                    lambda item, i: data_table_row(item, i)
                )
            ),
            variant="surface",
            size="2",
        ),
        type="always",
        scrollbars="vertical",
        style={"max_height": "400px"},
    )

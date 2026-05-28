import reflex as rx

def metric_card_with_chart(
    label: str, 
    value: str, 
    delta: str, 
    chart_data: list, 
    is_positive: bool = True
):
    """
    Card de métrica que exibe um valor principal, delta percentual e um mini-grafico (sparkline).
    
    Args:
        label: Título da métrica (ex: "Receita Total")
        value: Valor principal (ex: "R$ 12.000")
        delta: Variação (ex: "+12%")
        chart_data: Lista de dicionários [{'x': 1, 'y': 10}, ...]
        is_positive: Se a variação é positiva (verde) ou negativa (vermelho)
    """
    
    delta_color = "grass" if is_positive else "tomato"
    delta_icon = "trending-up" if is_positive else "trending-down"
    
    return rx.card(
        rx.hstack(
            # Lado Esquerdo: Dados
            rx.vstack(
                rx.text(label, size="1", color=rx.color("slate", 9), weight="medium"),
                rx.heading(value, size="6", color=rx.color("slate", 12)),
                rx.hstack(
                    rx.badge(
                        rx.icon(delta_icon, size=12),
                        delta,
                        color_scheme=delta_color,
                        radius="full",
                        variant="soft"
                    ),
                    rx.text("vs. mês anterior", size="1", color=rx.color("slate", 8)),
                    align="center",
                    spacing="2"
                ),
                align="start",
                spacing="2"
            ),
            # Lado Direito: Gráfico (Simulado com AreaChart)
            rx.box(
                rx.recharts.area_chart(
                    rx.recharts.area(
                        data_key="y",
                        stroke=rx.color(delta_color, 9),
                        fill=rx.color(delta_color, 4),
                        type="monotone"
                    ),
                    data=chart_data,
                    width="100%",
                    height=60,
                ),
                width="120px",
                height="60px",
                display=["none", "none", "block"] # Esconde em mobile
            ),
            justify="between",
            align="center",
            width="100%"
        ),
        size="2",
        variant="classic",
        style={
            "backdrop_filter": "blur(10px)",
            "background": rx.color("slate", 1, alpha=0.5),
        }
    )

import reflex as rx

# Este snippet demonstra como estruturar o layout para exportação PDF
# Normalmente usado em conjunto com libs como reportlab ou weasyprint no backend,
# mas aqui focamos na UI que dispara ou pre-visualiza.

def pdf_export_modal(is_open: rx.Var[bool], on_close: rx.EventHandler, on_export: rx.EventHandler):
    """
    Modal para configuração e exportação de relatórios PDF.
    """
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Exportar Relatório"),
            rx.dialog.description(
                "Configure as opções abaixo antes de gerar o PDF."
            ),
            
            rx.vstack(
                rx.text("Selecione o período", size="2", weight="bold"),
                rx.select(
                    ["Últimos 7 dias", "Últimos 30 dias", "Mês Atual", "Ano Atual"],
                    default_value="Mês Atual",
                    width="100%"
                ),
                
                rx.text("Opções de Inclusão", size="2", weight="bold"),
                rx.checkbox("Incluir gráficos"),
                rx.checkbox("Incluir dados brutos (anexo CSV)"),
                rx.checkbox("Adicionar marca d'água 'Confidencial'"),
                
                spacing="4",
                margin_y="4"
            ),
            
            rx.flex(
                rx.dialog.close(
                    rx.button("Cancelar", variant="soft", color_scheme="gray", on_click=on_close),
                ),
                rx.button(
                    rx.icon("file-down", size=18),
                    "Baixar PDF", 
                    on_click=on_export,
                    variant="solid"
                ),
                spacing="3",
                justify="end",
            ),
            style={"max_width": "450px"},
        ),
        open=is_open,
        on_open_change=on_close,
    )

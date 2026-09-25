"""
Neste arquivo ficam funções para configurar controles mais rapidamente, de maneira a não precisar definir propriedades 
várias vezes.
"""
import flet as ft

def botao_principal(label: str, on_click= None, bgcolor: ft.Colors | None = None) -> ft.FilledButton:
    """
    Retorna um botão grande, apropriado para tela inicial.
    """
    return ft.FilledButton(
            content=ft.Text(label, weight=ft.FontWeight.BOLD, size=20), 
            on_click=on_click, 
            elevation=True, 
            width=150, 
            height=50,
            bgcolor=bgcolor)

def texto_explicativo(conteudo: str, color: ft.Colors = ft.Colors.GREY_700):
    return ft.Text(conteudo, size=16, italic=True, color=color)

def card_brinquedo(nome:str, preco:str, quantidade: str, text_align=ft.TextAlign.LEFT):
    """
    Cria um card para apresentar um brinquedo, com nome e preço.
    """

    return ft.Container(
            content= ft.Text(
                value=f"{nome} ({quantidade}): {preco} reais", 
                size=16, 
                weight=ft.FontWeight.BOLD, 
                text_align=text_align),
            bgcolor=ft.Colors.GREY_500
            
            )




"""
Este aplicativo é um gerenciador de estoque desenvolvido para uma pequena loja de brinquedos, com o qual é possível
armazenar, editar, remover e exibir brinquedos ainda em estoque. Um sistema é necessário para isso porque brinquedos há
muito tempo em estoque são um problema financeiro muito grave.

A página é desenhada na função "main", que é a última e mais baixa neste arquivo. Por isso, desça a tela direto para ela, 
por favor.

Funções responsáveis por interagir com os dados (armazenados em JSON) e funções para eventos também estão neste arquivo.
Elas correpondem às demais funções além de main. Aliás, todas as funções disparadas por botões ou formulários estão com
o prefixo "event", para serem mais facilmente indentificáveis.

Pra controles parecidos que se repetem, há funções no arquivo "controles_personalizados.py", que os definem. Eles foram
usados neste arquivo para desenhar a tela.

Por fim, os dados seguem esta estrutura json: {"nome_brinquedo": {"quantidade": 0, "preco": 000.00}}, isto é, um 
dicionário onde cada chave é o nome de um briquedo, e seu valor é outro dicionário com "quantidade" e "preco".

"""
import flet as ft
import json
import os
import asyncio
from typing import Any, Literal

from flet.utils.platform_utils import is_linux

from controles_personalizados import botao_principal, texto_explicativo, card_brinquedo

def adicionar_brinquedo(nome: str, preco: str):
    """
    Registra um novo brinquedo ou então atualiza a quantidade de um já registrado, se tiver o mesmo nome. A inicialização
    do app garante que o arquivo onde os brinquedos ficam salvos existe, então não é necessário verificar agora. 

    nome (str): o nome do brinquedo.
    preco (str): preço em reais do brinquedo. Deve seguir este formato: 000,00.
    """

    # Se "preco" ou "nome" for uma string vazia, retornar erro.
    if not preco or not nome:
        raise ValueError("O argumento de função *preco* ou *nome* não pode ser uma string vazia.")

    # Converter preço para o tipo float, que é mais apropriado, e deixar maiúsculas as primeiras letras do nome.
    nome = nome.title()
    preco = preco.replace(",", ".")
    preco_float = float(preco)

    nome_arquivo = "estoque_brinquedos.json"
    novo_brinquedo = {"quantidade": 1, "preço": preco_float}

    # Se já foi registrado, atualizar o campo "quantidade" do brinquedo, se ainda não, adicionar um novo brinquedo.
    # Ler a estrutura atual, modificá-la e então sobrescrever a antiga pela nova.
    with open(nome_arquivo, "r+", encoding="utf-8") as f:
        estoque = json.load(f)
        f.seek(0, 0)
        f.truncate()

        if nome in estoque:
            estoque[nome]["quantidade"] += 1
            json.dump(estoque, f, ensure_ascii=True, indent=4)
        else:
            estoque[nome] = novo_brinquedo
            json.dump(estoque, f, ensure_ascii=True, indent=4)

def remover_brinquedo(nome: str):
    """
    Remove um brinquedo a partir do nome fornecido. No caso de não existir correspondentes, retorna ValueError.
    """

    # Obter a estrutura atual, remover um brinquedo (se existente) e então sobrescrever a estrutura antiga pela nova.
    # Se não há brinquedos registrados em estoque, cancelar a operação.
    # Se não encontrar brinquedo correspondente, retornar erro.
    with open("estoque_brinquedos.json", "r+", encoding="utf-8") as f:
       estoque: dict[str, dict[str, Any]] = json.load(f)

       if not (nome in estoque):
           raise ValueError("Não há brinquedo indexado com este nome.")

       f.seek(0, 0)
       f.truncate()

       del estoque[nome.title()]
       json.dump(estoque, f, ensure_ascii=True, indent=4)



def editar_brinquedo(nome: str, novo_preco: str, nova_quantidade: str):
    """
    Altera os valores (quantidade, preço) de um brinquedo atualmente registrado que corresponde ao nome fornecido. Se não
    há um brinquedo correspondente em estoque, retorna erro, que é capturado através de "KeyError". Se os novos valores
    fornecidos são strings vazias, retorna erro também.

    novo_preco (str): valor que vai substituir o preço atual, e precisa seguir este formato: "000,00". É uma string, em 
    vez de um float, porque facilita receber o valor de formulários Flet.

    nova_quantidade (str): valor inteiro que vai substituir a quantidade atual do brinquedo editado. Precisa seguir esse
    valor: "0" (sem casas decimais).
    """
    # Buscar o brinquedo editado pelo nome e retornar erro se não encontrado.
    # Através do modo "r+", ler a atual estrutura json, manipulá-la e então sobrescrevê-la pela nova.
    # Ao selecionar o brinquedo pelo nome (o que corresponde às chaves do dicionário json), é necessário deixar as 
    # iniciais maiúsculas, pois todos os nomes são salvos assim (str.title()).


    if not novo_preco or not nova_quantidade:
        raise ValueError("Os campos fornecidos estão vazios.")

    with open("estoque_brinquedos.json", "r+", encoding="utf-8") as f:
        estoque: dict[str, dict[str, Any]] = json.load(f)
        if not (nome in estoque):
            raise ValueError("Não há brinquedos com estes nome.")

        f.seek(0, 0)
        f.truncate()

        preco_float = float(novo_preco.replace(",", "."))
        quantidade_int = int(nova_quantidade)

        estoque[nome.title()]["preço"] = preco_float
        estoque[nome.title()]["quantidade"] = quantidade_int

        json.dump(estoque, f, ensure_ascii=True, indent=4)
            



def obter_brinquedos(campo: Literal["nome", "preço", "quantidade"] | None = None):
    """
    Retorna um objeto Python baseado no json onde os brinquedos foram registrados ou uma parte disso. A estrutura json
    pode ser obtida na descrição deste arquivo, que está no topo dele.

    campo (str): o nome do campo de onde as informações serão obtidas e que deve ser uma chave de dicionário existente.
    Por exemplo, para se obter os nomes de cada brinquedo, *campo* deve ser igual a "nome". Deixar este argumento vazio
    faz a função retornar a estrutura json inteira. Estes são os valores possíveis, quando fornecidos: "nome", 
    "quantidade" e "preço"
    """
    with open("estoque_brinquedos.json", "r", encoding="utf-8") as f:
        estoque:dict[str, dict[str, str]] = json.load(f)

    if campo is None:
        return estoque
    elif campo == "nome":
        return estoque.keys() # As chaves são os nomes dos brinquedos.
    else:
        return [brinquedo[campo] for brinquedo in estoque.values()]

async def event_corrigir_campo_preco(e: ft.Event[ft.TextField]):
    formulario_preco = e.control
    conteudo:str = formulario_preco.value

    # Inserir uma vírgula antes dos dois últimos números: 000,00, se houver mais que 3 números, e remover vírgulas velhas.
    # Impedir qualquer tentativa do usuário de inserir não números.
    # Os 2 últimos números, que devem ser centavos, possuem estes índices: [-2:]
    conteudo_corrigido = ""
    for digito in conteudo:
        if digito.isdigit():
            conteudo_corrigido += digito


    if len(conteudo_corrigido) >= 3:
        centavos = conteudo_corrigido[-2:]
        reais = conteudo_corrigido.removesuffix(centavos)

        conteudo_corrigido = reais + "," + centavos

    formulario_preco.value = conteudo_corrigido


def main(page: ft.Page):
    # Configurar a janela.
    page.window.maximized = False
    page.window.maximizable = False
    page.window.width = 900
    page.window.height = 400
    page.title = "Gerenciador de Estoque de Brinquedos."

    # ROW principal que porá as colunas lado a lado no aplicativo.
    row_principal = ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, expand=True)

    # Adicionar um botões.
    # Também criar funções de evento para um.
    async def event_btn_adicionar(e):
        try:
            adicionar_brinquedo(form_nome_brinquedo.value, form_preco_brinquedo.value)
            mensagem_erro.value = ""
        except ValueError:
            mensagem_erro.value = "Nenhum campo pode ficar vazio!"

    def event_btn_editar(e: ft.Event[ft.Button]):
        """
        Função de evento para o botão "editar", logo abaixo. Ele executa este processo: tornar o campo "quantidade" 
        visível, mudar seu nome para "salvar", muda a cor de fundo para verde e se preparar para editar um brinquedo, se
        clicado novamente. Após as mudanças visuais, se clicado de novo, restaura tudo para como era inicialmente, o que
        controla verificando se o campo "quantidade" está visível ou não.

        Além disso, a função "editar_brinquedo" é usada para alterar os dados de um brinquedo de fato. Esta função 
        retorna "ValueError" caso o nome fornecido não corresponda a nenhum brinquedo. Neste caso, uma mensagem de erro
        é retornada ao usuário.
        """

        botao_editar = e.control

        if form_quantidade_brinquedo.visible:
            try:
                # Coletar informações.
                nome_brinquedo = form_nome_brinquedo.value
                novo_preco = form_preco_brinquedo.value
                nova_quantidade = form_quantidade_brinquedo.value

                # Editar, de fato.
                editar_brinquedo(nome=nome_brinquedo, novo_preco=novo_preco, nova_quantidade=nova_quantidade)
                mensagem_erro.value = "O brinquedo foi editado com sucesso."
                
            except ValueError as error:
                mensagem_erro.value = str(error)

            finally:
                # Reverter mudanças visuais.
                form_quantidade_brinquedo.value = ""
                form_quantidade_brinquedo.visible = False
                botao_editar.content = ft.Text("Editar", size=20, weight=ft.FontWeight.BOLD)
                botao_editar.bgcolor = None
                
        else:
            form_quantidade_brinquedo.visible = True
            botao_editar.content = ft.Text("Salvar", weight=ft.FontWeight.BOLD, size=20)
            botao_editar.bgcolor = ft.Colors.GREEN_800
            mensagem_erro.value = "Após definir os novos valores para o brinquedo de mesmo nome, aperte em *salvar*"

    def event_btn_remover(e):
        nome = form_nome_brinquedo.value
        if not nome:
            mensagem_erro.value = "Para remover brinquedo, preencha o campo *nome*"
            return

        try:
            remover_brinquedo(nome)
            mensagem_erro.value = "Brinquedo {} removido com sucesso".format(nome)
        except ValueError as e:
            mensagem_erro.value = "Não há brinquedo com este nome"


    area_botoes = ft.Column(
        controls=[
            botao_principal("Adicionar", on_click=event_btn_adicionar),
            botao_principal("Remover", on_click=event_btn_remover),
            botao_principal("Editar", on_click=event_btn_editar),
        ],
    alignment=ft.MainAxisAlignment.SPACE_AROUND,
    expand=1
    )

    # Adicionar área para entrada de dados (Terá campos de formulário.)
    area_entrada_dados = ft.Container(
        expand=2,
        bgcolor=ft.Colors.BLUE_100,
        border=ft.Border.all(1),
        padding=10,
        content=ft.Column(
            controls=[
                texto_explicativo("Não preocupe-se com maiúsculas ou minúsculas, pois o sistema cuida disso."),

                form_nome_brinquedo:= ft.TextField(label="Nome do brinquedo."),
                form_preco_brinquedo:= ft.TextField(label="Preço do brinquedo.", hint_text="Digite o preço em reais.",
                                                    on_change=event_corrigir_campo_preco),
                form_quantidade_brinquedo:= ft.TextField(
                    visible=False,
                    hint_text="Para editar quantidade, altere este campo.",
                    label="Quantidade",
                    input_filter=ft.NumbersOnlyInputFilter()
                    ),
                mensagem_erro:= texto_explicativo("", color=ft.Colors.RED_900)
                ],
            spacing=20
            ),
        alignment=ft.Alignment.CENTER
        )

    # Adicionar área onde serão exibidos os brinquedos em estoque, se solicitado.
    brinquedos_exibidos = ft.Column(scroll= ft.ScrollMode.ADAPTIVE, height=290, width=400)

    def event_atualizar_exibidos(e):
        nomes = obter_brinquedos("nome")
        precos = obter_brinquedos("preço")
        quantidades = obter_brinquedos("quantidade")

        brinquedos_exibidos.controls = \
                [card_brinquedo(nome, preco, quantidade) for nome, preco, quantidade in zip(nomes, precos, quantidades)]

    area_exibicao = ft.Container(
            expand=2,
            alignment=ft.Alignment.TOP_LEFT,
            bgcolor=ft.Colors.BLUE_100,
            border=ft.Border.all(1),
            padding=ft.Padding.all(4),
            content= ft.Column(
                controls=[
                    ft.Container(
                        content= brinquedos_exibidos,
                        border=ft.Border.all(1)
                        ),
                    ft.FilledButton("Atualizar", 
                                    on_click= event_atualizar_exibidos)
                    ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                horizontal_alignment=ft.MainAxisAlignment.START,
                expand=True
                )
            )


    # Organizar tudo.
    row_principal.controls.append(area_botoes)
    row_principal.controls.append(area_entrada_dados)
    row_principal.controls.append(area_exibicao)
    page.add(row_principal)


if __name__ == "__main__":
    nome_arquivo = "estoque_brinquedos.json"
    if not os.path.isfile(nome_arquivo):
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=True, indent=4)

    ft.run(main)

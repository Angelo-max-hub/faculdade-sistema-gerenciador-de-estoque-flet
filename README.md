# O que é este trabalho?
Este sistema foi desenvolvido para realização de um trabalho avaliativo do curso Tecnólogo em Análise e Desenvolvimento de
sistemas.

# Introdução rápida.
Este sistema tem o objetivo de facilitar o gerenciamento de estoque em uma loja de brinquedos fictícia. Ele é justificável 
porque a permanência prolongada de brinquedos em estoque se torna um problema financeiro e administrativo grave, e é 
inviável os gestores memorizarem todos os brinquedos em estoque, sua quantidade e seu valores. O sistema permite registrar
essas coisas.

# Como fazer funcionar?
## Crie um ambiente virtual.
Crie e ative um ambiente virtual antes das outras etapas com os comandos a seguir (se estiver no Windows)
```sh
mkdir .venv
python -m venv .venv
.venv/Scripts/Activate.ps1
```

## Instale o Flet.
Instale o Flet com o comando e versão a seguir:
```sh
pip install "flet==1.0.0"
```
Executar o sistema com **versões mais recentes desta biblioteca**, quando forem lançadas, pode afetar ou impossibilitar o 
funcionamento do sistema. Por isso, atente-se para instalar a versão **1.0.0**, se não utilizar o ambiente virtual já 
criado.

## Execute o aplicativo.
Então, execute o arquivo *main.py* com o comando a seguir:
```sh
flet run main.py
```

# Informações importantes sobre a organização de código e o programa.
- Para alguns controles cujas configurações se repetiam, criei funções para evitar a duplicação de código. Estas funções
estão no arquivo *controles_personalizados.py*.
- O sistema utiliza um arquivo JSON para armazenar as informações dos brinquedos, e sua estrutura é esta:
```json
{
    "nome do brinquedo": {
        "preço": 00.0,
        "quantidade": 0
    },
    "outro nome de brinquedo": {
        "preco": 00.0,
        "quantidade": 0
    }
}
```
- Há várias funções dedicadas a interagir com os dados, e elas estão no arquivo *main.py*, onde a interface gráfica é 
  desenhada. Elas incluem **adicionar_brinquedo()** e **remover_brinquedo**.
- Funções de evento invocadas por controles também estão no arquivo *main.py*

# Prova de autoria.
Este é o link para o drive onde estão os vídeos de mim programando o sistema: [ir para o drive](https://drive.google.com/drive/folders/1qXMz_Too0sSyomOS7yG4x2ceW-HhD_kP?usp=sharing).

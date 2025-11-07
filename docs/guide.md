# Guias

Algumas instruções para utilizar o ptrojeto

## Rodar o projeto 

### Instalação e configuração do uv

O projeto foi desenvolvido com python usando o gerenciador de dependências 'UV'.

O uv é uma ferramenta de linha de comando que facilita a execução do python usando o `enviroments` o venv. O que poermite separa as dependencias instaladas no projeto das instaladas globalmente do sistema.

para usar o uv basta ter o python instalado, e instalar o uv a seguindo as orientações da documentação [uv.com](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer).

Ele também pode ser instalado usando o `pip` (gerenciador de dependências padrão do python), basta rodar o seguinte comando no perminal:

```shell
pip install uv
```
para testar a instalação, rode o seguinte comando:

```shell
uv --version
```

ele deve retornar algo assim:

```shell
uv 0.6.3 (a0b9f22a2 2025-02-24)
```
---

### Instalando as dependências do projeto

Para configurar o projeto é necessario instalar as dependencias.

Primeiro acesse a pasta do projeto no terminal, depois rode o seguinte comando:

```shell
uv sync
```

O uv irá configurar o `enviroment` do projeto e instalar as dependências.

---

### Rodando o código para coletar os dados

Para baixar os dados da fonte rode o seguinte comando:

```shell
uv run main.py
```

O sistema irá gerar um arquivo `comexstat.xlsx` com os dados na pasta `data`.

E também vai gerar um banco sqlite no arquivo `database.db` com todos os dados estruturados.

## Gerenciar repositório

Faça a configuração do git e github na sua máquina.

### Clonar o repositório do github

```shell
git clone https://github.com/geofmoura/analisededados.git
```

```shell
cd analisededados
```

### Criar um nova branch

Quando você clona o repositorio ele vem na brach padrão nesse caso a `main`, crie a sua branch para fazer as suas alterações sem afetar o código principal.

```shell
git branch -b <nome-da-branch>
```

### Atualizar branch

Para atualizar a sua branch com as alterações da branch main rode o seguinte comando:

```shell
git pull origin main
```














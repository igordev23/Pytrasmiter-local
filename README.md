# Screen Streamer com Flask, OpenCV e MSS

Este projeto transmite a tela do computador em tempo real via navegador, utilizando `Flask`, `OpenCV`, `mss` e `pyautogui`. Um círculo preto é desenhado sobre a posição atual do cursor do mouse, facilitando a visualização em apresentações ou demonstrações remotas.

## Funcionalidades

- Captura da tela inteira com sobreposição do cursor.
- Transmissão em tempo real via browser.
- Interface com botões para iniciar e parar a transmissão.
- Suporte à visualização remota via IP local.

## Ambiente Virtual (Recomendado)

Para evitar conflitos de dependências com outros projetos Python, recomenda-se o uso de um ambiente virtual.

### ▶️ Criando o ambiente virtual

Abra o terminal ou prompt de comando, acesse a pasta do projeto e execute:

```bash
python -m venv venv
```
Isso criará uma pasta chamada venv com o ambiente isolado do Python.

### ▶️ Ativando o ambiente virtual

Windows (CMD ou PowerShell):

```bash
venv\Scripts\activate
```
macOS ou Linux:

```bash
source venv/bin/activate
```
Você saberá que o ambiente está ativo quando aparecer (venv) no início da linha do terminal.

### ▶️ Instalando as dependências

Com o ambiente ativado, instale os pacotes necessários com:

```bash
pip install -r requirements.txt
```
### ⏹️ Desativando o ambiente virtual

Após terminar, você pode desativar o ambiente com:

```bash
deactivate
```
### Executando o Projeto

Com o ambiente virtual ativado, execute o arquivo principal:

```bash
python app.py
```

(Substitua app.py pelo nome do seu script principal, se for diferente.)
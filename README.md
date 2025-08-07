# Screen Streamer com Flask, OpenCV e MSS

Este projeto transmite a tela do computador em tempo real via navegador, utilizando `Flask`, `OpenCV`, `mss`, `tkinter` e `pyautogui`. Um círculo preto é desenhado sobre a posição atual do cursor do mouse, facilitando a visualização em apresentações ou demonstrações remotas.

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

#### ⚠️ Atenção:
Em alguns sistemas (Linux/macOS), mesmo após instalar o requirements.txt, podem ocorrer erros relacionados a bibliotecas nativas como tkinter, Xlib, ou drivers de tela usados por pyautogui e opencv-python.

Se isso acontecer:

##### No Linux (Ubuntu/Debian), você pode precisar instalar:

```bash
sudo apt-get install python3-tk python3-dev libx11-dev
```

##### No macOS, use o Homebrew para garantir dependências nativas:

```bash
brew install python-tk
```

No Windows, certifique-se de que o Python foi instalado com o instalador oficial do python.org e que a opção “Add Python to PATH” foi marcada.

✅ Recomenda-se o uso da versão Python 3.10.x, que oferece melhor compatibilidade com todas as bibliotecas utilizadas no projeto.

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
### ⚠️ Atenção – Porta 80 pode exigir permissão de administrador

Por padrão, o servidor Flask roda na porta 80, o que pode causar erro em sistemas Linux/macOS por falta de permissão.

Se ocorrer erro ao iniciar o servidor, você pode:

Executar com sudo:

```bash
sudo python app.py
```

Ou alterar a porta para uma acima de 1024 no arquivo app.py:

```bash
app.run(host='0.0.0.0', port=8080)
```



(Substitua app.py pelo nome do seu script principal, se for diferente.)


## 🔧 Gerando Executável com PyInstaller

Este projeto pode ser empacotado como um executável para **Windows, Linux e macOS** usando o [PyInstaller](https://pyinstaller.org/).

---

### ✅ Pré-requisitos

Instale o PyInstaller:

```bash
pip install pyinstaller
```
### ⚠️ Requisitos Específicos por Sistema

#### 🪟 Windows
Nenhum requisito adicional além do Python instalado corretamente no PATH.

Use ; como separador no parâmetro --add-data.

#### 🐧 Linux
É recomendado instalar os seguintes pacotes:

```bash
sudo apt install build-essential python3-dev
```

#### 🍎 macOS
Necessário instalar as ferramentas de linha de comando do Xcode, se ainda não estiverem instaladas:

```bash
xcode-select --install
```

Isso é necessário para compilar alguns binários e permitir que o PyInstaller funcione corretamente.

### 🚀 Gerar Executável
Use o comando abaixo para empacotar o projeto com interface gráfica (--windowed) e incluir a pasta templates/:

```bash
pyinstaller --onefile --windowed --add-data "templates:templates" app.py

```
🔄 No Windows, troque : por ;:

```bash
pyinstaller --onefile --windowed --add-data "templates;templates" app.py

```
### 📦 Arquivo gerado
Após a execução, o executável será gerado na pasta dist/:

```bash
dist/
└── app.exe  (Windows)
└── app      (Linux/macOS)
```

## 📝 Observações
Mesmo com --onefile, o PyInstaller extrai arquivos temporários no tempo de execução, então o uso de caminhos relativos (como templates/) ainda funciona.

Se seu programa estiver travando no macOS por segurança, vá em:
Preferências do Sistema > Segurança e Privacidade > Aba Geral
e clique em “Permitir” para o app bloqueado.
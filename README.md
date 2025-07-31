# Screen Streamer com Flask, OpenCV e MSS

Este projeto transmite a tela do computador em tempo real via navegador, utilizando `Flask`, `OpenCV`, `mss` e `pyautogui`. Um círculo vermelho é desenhado sobre a posição atual do cursor do mouse, facilitando a visualização em apresentações ou demonstrações remotas.

## Funcionalidades

- Captura da tela inteira com sobreposição do cursor.
- Transmissão em tempo real via browser.
- Interface com botões para iniciar e parar a transmissão.
- Suporte à visualização remota via IP local.

## Requisitos

Instale as bibliotecas necessárias com:

```bash
pip install -r requirements.txt

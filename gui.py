# gui.py
import tkinter as tk
from tkinter import ttk
import requests

def iniciar_interface(ip_local):
    def iniciar_transmissao():
        try:
            requests.get(f"http://{ip_local}:80/start")
            atualizar_status()
        except Exception as e:
            status_var.set(f"Erro: {e}")
            status_label.config(fg="orange")

    def parar_transmissao():
        try:
            requests.get(f"http://{ip_local}:80/stop")
            atualizar_status()
        except Exception as e:
            status_var.set(f"Erro: {e}")
            status_label.config(fg="orange")

    def atualizar_status():
        try:
            r = requests.get(f"http://{ip_local}:80/status").json()
            if r['capturing']:
                status_var.set(f"🟢 Transmissão Ativa ({r['fps']} FPS)")
                status_label.config(fg="green")
                start_btn.config(state="disabled")
                stop_btn.config(state="normal")
            else:
                status_var.set("🔴 Transmissão Inativa")
                status_label.config(fg="red")
                start_btn.config(state="normal")
                stop_btn.config(state="disabled")
        except:
            status_var.set("⚠️ Servidor offline")
            status_label.config(fg="orange")
            start_btn.config(state="disabled")
            stop_btn.config(state="disabled")

    def alterar_fps(event):
        novo_fps = int(fps_var.get())
        try:
            requests.get(f"http://{ip_local}:80/set_fps?value={novo_fps}")
            atualizar_status()
        except:
            status_var.set("Erro ao mudar FPS")
            status_label.config(fg="orange")

    # Interface
    janela = tk.Tk()
    janela.title("Controle de Transmissão")
    janela.geometry("320x260")
    janela.resizable(False, False)

    ttk.Label(janela, text="Controle de Transmissão", font=("Segoe UI", 14)).pack(pady=10)

    status_var = tk.StringVar(value="Carregando...")
    status_label = tk.Label(janela, textvariable=status_var, font=("Segoe UI", 12))
    status_label.pack(pady=10)

    start_btn = ttk.Button(janela, text="Iniciar", command=iniciar_transmissao)
    start_btn.pack(pady=5)

    stop_btn = ttk.Button(janela, text="Parar", command=parar_transmissao)
    stop_btn.pack(pady=5)

    ttk.Label(janela, text="FPS:").pack(pady=(15, 0))
    fps_var = tk.StringVar(value="60")
    fps_box = ttk.Combobox(janela, textvariable=fps_var, state="readonly", values=["30", "40", "50", "60"])
    fps_box.pack(pady=5)
    fps_box.bind("<<ComboboxSelected>>", alterar_fps)

    atualizar_status()
    janela.mainloop()

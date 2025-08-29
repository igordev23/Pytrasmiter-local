# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
import requests
import socket
import pyperclip  # pip install pyperclip

def obter_ip_local():
    """Obtém o IP local da rede"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "IP não encontrado"

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
                status_var.set(f"🟢 Transmissão Ativa ({r['fps']} FPS) - 👥 {r['viewers']} conectados")
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
        
        
        janela.after(2000, atualizar_status)


    def alterar_fps(event):
        novo_fps = int(fps_var.get())
        try:
            requests.get(f"http://{ip_local}:80/set_fps?value={novo_fps}")
            atualizar_status()
        except:
            status_var.set("Erro ao mudar FPS")
            status_label.config(fg="orange")

    def copiar_ip():
        pyperclip.copy(ip_local)
        messagebox.showinfo("Copiado", f"IP {ip_local} copiado para a área de transferência.")

    # Interface
    janela = tk.Tk()
    janela.title("Controle de Transmissão")
    janela.geometry("500x420")
    janela.resizable(False, False)

    ttk.Label(janela, text="Controle de Transmissão", font=("Segoe UI", 14)).pack(pady=10)

    # Exibição do IP
    # Frame do IP/Link de visualização
    frame_link = ttk.Frame(janela)
    frame_link.pack(pady=10, padx=10, fill="x")

    # Label com o IP ou link
    label_link = ttk.Label(frame_link, text=f"🔗 Link de visualização: http://{ip_local}:80", font=("Segoe UI", 10))
    label_link.pack(side="left", expand=True)

    # Botão para copiar
    btn_copiar = ttk.Button(frame_link, text="Copiar", command=copiar_ip)
    btn_copiar.pack(side="right", padx=5)


    # Status
    status_var = tk.StringVar(value="Carregando...")
    status_label = tk.Label(janela, textvariable=status_var, font=("Segoe UI", 12))
    status_label.pack(pady=10)

    # Botões
    start_btn = ttk.Button(janela, text="Iniciar", command=iniciar_transmissao)
    start_btn.pack(pady=5)

    stop_btn = ttk.Button(janela, text="Parar", command=parar_transmissao)
    stop_btn.pack(pady=5)

    # FPS
    ttk.Label(janela, text="FPS:").pack(pady=(15, 0))
    fps_var = tk.StringVar(value="60")
    fps_box = ttk.Combobox(janela, textvariable=fps_var, state="readonly", values=["30", "40", "50", "60"])
    fps_box.pack(pady=5)
    fps_box.bind("<<ComboboxSelected>>", alterar_fps)

    atualizar_status()
    janela.mainloop()


if __name__ == "__main__":
    ip = obter_ip_local()
    iniciar_interface(ip)

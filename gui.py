import tkinter as tk
from tkinter import ttk, messagebox
import requests
import socket
import threading
import pyperclip


# ---------------------------------------------------------
# Função que obtém o IP local
# ---------------------------------------------------------
def obter_ip_local():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return None


# ---------------------------------------------------------
# Interface principal
# ---------------------------------------------------------
def iniciar_interface(ip_inicial):

    # IP que muda dinamicamente
    ip_atual = {"ip": ip_inicial}

    # Requisição com timeout e sem travar GUI
    def request_async(url, callback=None):
        def run():
            try:
                r = requests.get(url, timeout=1)
                if callback:
                    callback(r)
            except:
                if callback:
                    callback(None)
        threading.Thread(target=run, daemon=True).start()

    # Atualiza IP real automaticamente
    def atualizar_ip_automatico():
        novo_ip = obter_ip_local()
        if novo_ip and novo_ip != ip_atual["ip"]:
            ip_atual["ip"] = novo_ip
            label_ip.config(text=f"IP atual: {novo_ip}")
            label_link.config(text=f"🔗 Link de visualização: http://{novo_ip}:80")
        janela.after(2000, atualizar_ip_automatico)

    # ---------------------- AÇÕES -------------------------

    def iniciar_transmissao():
        request_async(f"http://{ip_atual['ip']}:80/start", lambda r: atualizar_status())

    def parar_transmissao():
        request_async(f"http://{ip_atual['ip']}:80/stop", lambda r: atualizar_status())

    def atualizar_status():
        def callback(resp):
            if resp is None:
                status_var.set("⚠️ Servidor offline")
                status_label.config(fg="orange")
                start_btn.config(state="disabled")
                stop_btn.config(state="disabled")
                return

            try:
                r = resp.json()
                if r["capturing"]:
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
                status_var.set("⚠️ Erro no servidor")
                status_label.config(fg="orange")

        request_async(f"http://{ip_atual['ip']}:80/status", callback)
        janela.after(2000, atualizar_status)

    def alterar_fps(event):
        fps = int(fps_var.get())
        request_async(f"http://{ip_atual['ip']}:80/set_fps?value={fps}")

    def copiar_ip():
        pyperclip.copy(ip_atual["ip"])
        messagebox.showinfo("Copiado", "IP copiado para a área de transferência.")

    # ---------------------------------------------------------
    # Construção da GUI
    # ---------------------------------------------------------

    janela = tk.Tk()
    janela.title("Controle de Transmissão")
    janela.geometry("520x440")
    janela.resizable(False, False)

    ttk.Label(janela, text="🎥 Controle de Transmissão", font=("Segoe UI", 14)).pack(pady=10)

    label_ip = ttk.Label(janela, text=f"IP atual: {ip_atual['ip']}", font=("Segoe UI", 10))
    label_ip.pack(pady=5)

    # Link e botão copiar
    frame_link = ttk.Frame(janela)
    frame_link.pack(pady=10, padx=10, fill="x")

    label_link = ttk.Label(frame_link, text=f"🔗 Link de visualização: http://{ip_atual['ip']}:80", font=("Segoe UI", 10))
    label_link.pack(side="left", expand=True)

    ttk.Button(frame_link, text="Copiar", command=copiar_ip).pack(side="right", padx=5)

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
    fps_box = ttk.Combobox(janela, textvariable=fps_var, state="readonly",
                           values=["30", "40", "50", "60"])
    fps_box.pack(pady=5)
    fps_box.bind("<<ComboboxSelected>>", alterar_fps)

    # Inicia primeiro status
    atualizar_status()

    # Inicia detecção automática de IP
    atualizar_ip_automatico()

    janela.mainloop()


# ---------------------------------------------------------
# Execução principal
# ---------------------------------------------------------
if __name__ == "__main__":
    ip = obter_ip_local()
    iniciar_interface(ip)

import socket
import threading
import requests
import pyperclip
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox


def obter_ip_local():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return None


def iniciar_interface(ip_inicial):

    ip_atual = {"ip": ip_inicial}

    def request_async(url, callback=None):
        def run():
            try:
                r = requests.get(url, timeout=1)
                callback(r) if callback else None
            except:
                callback(None) if callback else None
        threading.Thread(target=run, daemon=True).start()

    def atualizar_ip_auto():
        novo_ip = obter_ip_local()
        if novo_ip and novo_ip != ip_atual["ip"]:
            ip_atual["ip"] = novo_ip
            label_ip.configure(text=f"IP atual: {novo_ip}")
            label_link.configure(text=f"http://{novo_ip}:80")
        janela.after(2000, atualizar_ip_auto)

    # --------------------- AÇÕES ----------------------
    def iniciar_transmissao():
        request_async(f"http://{ip_atual['ip']}:80/start", lambda r: atualizar_status())

    def parar_transmissao():
        request_async(f"http://{ip_atual['ip']}:80/stop", lambda r: atualizar_status())

    def atualizar_status():
        def callback(resp):
            if resp is None:
                status_var.set("⚠ Servidor offline")
                status_label.configure(bootstyle="warning")
                start_btn.configure(state=DISABLED)
                stop_btn.configure(state=DISABLED)
                return

            try:
                data = resp.json()
                if data.get("capturing"):
                    status_var.set(
                        f"🟢 Transmitindo ({data.get('fps')} FPS) — 👥 {data.get('viewers')} espectadores"
                    )
                    status_label.configure(bootstyle="success")
                    start_btn.configure(state=DISABLED)
                    stop_btn.configure(state=NORMAL)
                else:
                    status_var.set("🔴 Transmissão parada")
                    status_label.configure(bootstyle="danger")
                    start_btn.configure(state=NORMAL)
                    stop_btn.configure(state=DISABLED)

            except:
                status_var.set("⚠ Erro no servidor")
                status_label.configure(bootstyle="warning")

        request_async(f"http://{ip_atual['ip']}:80/status", callback)
        janela.after(2000, atualizar_status)

    def alterar_fps(event):
        fps = int(fps_var.get())
        request_async(f"http://{ip_atual['ip']}:80/set_fps?value={fps}")

    def copiar_link():
        pyperclip.copy(f"http://{ip_atual['ip']}:80")
        messagebox.showinfo("Copiado", "Link copiado para a área de transferência.")

    # ---------------------------------------------------------
    # GUI — Material 3
    # ---------------------------------------------------------
    janela = tb.Window(themename="flatly")
    janela.title("Controle de Transmissão")
    janela.geometry("540x800")
    janela.resizable(False, False)

    tb.Label(
        janela,
        text="🎥 Controle de Transmissão",
        font=("Segoe UI", 18, "bold")
    ).pack(pady=15)

    # CARD IP
    card_ip = tb.Labelframe(janela, text="Endereço IP", padding=15)
    card_ip.pack(padx=20, pady=10, fill="x")

    label_ip = tb.Label(card_ip, text=f"IP atual: {ip_atual['ip']}", font=("Segoe UI", 11))
    label_ip.pack(anchor="w")

    # CARD LINK
    card_link = tb.Labelframe(janela, text="Visualização", padding=15)
    card_link.pack(padx=20, pady=10, fill="x")

    tb.Label(card_link, text="Link:", font=("Segoe UI", 11)).pack(anchor="w")

    link_row = tb.Frame(card_link)
    link_row.pack(fill="x", pady=5)

    label_link = tb.Label(link_row, text=f"http://{ip_atual['ip']}:80", font=("Segoe UI", 10))
    label_link.pack(side="left", expand=True)

    tb.Button(link_row, text="Copiar", bootstyle="primary", command=copiar_link).pack(side="right")

    # CARD STATUS
    card_status = tb.Labelframe(janela, text="Status", padding=15)
    card_status.pack(padx=20, pady=10, fill="x")

    status_var = tb.StringVar(value="Carregando...")
    status_label = tb.Label(card_status, textvariable=status_var, font=("Segoe UI", 12, "bold"))
    status_label.pack()

    # CONTROLES
    card_ctrl = tb.Labelframe(janela, text="Controles", padding=15)
    card_ctrl.pack(padx=20, pady=10, fill="x")

    start_btn = tb.Button(card_ctrl, text="▶ Iniciar Transmissão", bootstyle="success", command=iniciar_transmissao)
    start_btn.pack(fill="x", pady=5)

    stop_btn = tb.Button(card_ctrl, text="⏹ Parar Transmissão", bootstyle="danger", command=parar_transmissao)
    stop_btn.pack(fill="x", pady=5)

   # --- FPS CARD (ESSA PARTE FICA VISÍVEL AQUI) ---
    card_fps = tb.Labelframe(janela, text="Configurações de FPS", padding=15)
    card_fps.pack(padx=20, pady=10, fill="x")   # <-- ESSENCIAL

    tb.Label(card_fps, text="Selecione o FPS:", font=("Segoe UI", 11)).pack(anchor="w")

    fps_var = tb.StringVar(value="60")

    fps_box = tb.Combobox(
        card_fps,
        textvariable=fps_var,
        values=["15", "24", "30", "40", "50", "60", "75", "90"],
        state="readonly",
        bootstyle="primary"
    )
    fps_box.pack(fill="x", pady=5)
    fps_box.bind("<<ComboboxSelected>>", alterar_fps)


    atualizar_status()
    atualizar_ip_auto()

    janela.mainloop()


if __name__ == "__main__":
    ip = obter_ip_local()
    iniciar_interface(ip)

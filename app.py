# app.py
import cv2
import numpy as np
import threading
import time
import socket
import mss
import pyautogui
from flask import Flask, Response, render_template, request
from gui import iniciar_interface

app = Flask(__name__)

frame_lock = threading.Lock()
ultimo_frame = None
capturando = False
thread_captura = None
encerrar_event = threading.Event()
fps_atual = 60  # Valor padrão de FPS

def capturar_tela():
    global ultimo_frame, fps_atual
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        while not encerrar_event.is_set():
            try:
                img = np.array(sct.grab(monitor))
                 # Adiciona borda branca de 10 pixels em todos os lados
               
                mouse_x, mouse_y = pyautogui.position()
                cv2.circle(img, (mouse_x, mouse_y), 5, (0, 0, 0), -1)
                _, buffer = cv2.imencode('.jpg', img)
                with frame_lock:
                    ultimo_frame = buffer.tobytes()
                time.sleep(1 / fps_atual)
            except Exception as e:
                print(f"Erro na captura: {e}")
                break

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start')
def start():
    global capturando, thread_captura
    if not capturando:
        encerrar_event.clear()
        capturando = True
        thread_captura = threading.Thread(target=capturar_tela)
        thread_captura.daemon = True
        thread_captura.start()
    return 'Transmissão iniciada.'

@app.route('/stop')
def stop():
    global capturando
    if capturando:
        encerrar_event.set()
        capturando = False
    return 'Transmissão parada.'

@app.route('/status')
def status():
    return {
        'capturing': capturando,
        'fps': fps_atual
    }

@app.route('/set_fps')
def set_fps():
    global fps_atual
    try:
        novo_fps = int(request.args.get('value'))
        if novo_fps in [30, 40, 50, 60]:
            fps_atual = novo_fps
            return f"FPS ajustado para {fps_atual}"
        else:
            return "FPS inválido", 400
    except:
        return "Erro ao ajustar FPS", 400

@app.route('/stream')
def stream():
    def gerar():
        while not encerrar_event.is_set():
            with frame_lock:
                frame = ultimo_frame
            if frame:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.033)  # Isso é fixo para envio da imagem, não precisa ser alterado
    return Response(gerar(), mimetype='multipart/x-mixed-replace; boundary=frame')

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
    except:
        ip = "127.0.0.1"
    return ip

if __name__ == '__main__':
    ip_local = get_local_ip()

    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=80, threaded=True, use_reloader=False))
    flask_thread.daemon = True
    flask_thread.start()

    print(f"\nServidor iniciado! Acesse pelo navegador:\n")
    print(f"Visualização: http://{ip_local}:80/\n")

    iniciar_interface(ip_local)

import cv2
import numpy as np
from flask import Flask, Response, render_template
import mss
import socket
import threading
import time
import pyautogui

app = Flask(__name__)

frame_lock = threading.Lock()
ultimo_frame = None
capturando = False
thread_captura = None

# Adiciona um controle para encerrar o loop com segurança
encerrar_event = threading.Event()

def capturar_tela():
    global ultimo_frame
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        while not encerrar_event.is_set():
            try:
                img = np.array(sct.grab(monitor))
                mouse_x, mouse_y = pyautogui.position()
                cv2.circle(img, (mouse_x, mouse_y), 10, (0, 0, 255), -1)
                _, buffer = cv2.imencode('.jpg', img)
                with frame_lock:
                    ultimo_frame = buffer.tobytes()
                time.sleep(0.033)
            except Exception as e:
                print(f"Erro na captura: {e}")
                break

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transmitter')
def transmitter():
    return render_template('transmitter.html')

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
    return {'capturing': capturando}

@app.route('/stream')
def stream():
    def gerar():
        while not encerrar_event.is_set():
            with frame_lock:
                frame = ultimo_frame
            if frame:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.033)
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
    print(f"\nServidor iniciado! Acesse pelo navegador:\n")
    print(f"Visualização: http://{ip_local}:5000/")
    print(f"Transmissor:  http://{ip_local}:5000/transmitter\n")

    app.run(host='0.0.0.0', port=5000, threaded=True)

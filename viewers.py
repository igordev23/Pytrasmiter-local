# viewers.py
from flask import Blueprint, request, jsonify

bp_viewers = Blueprint("bp_viewers", __name__)

# contador global
viewers_conectados = 0

@bp_viewers.route("/register_viewer", methods=["POST"])
def register_viewer():
    global viewers_conectados
    viewers_conectados += 1
    print(f"Viewer registrado. Total: {viewers_conectados}")
    return jsonify({"viewers": viewers_conectados})

@bp_viewers.route("/unregister_viewer", methods=["POST"])
def unregister_viewer():
    global viewers_conectados
    if viewers_conectados > 0:
        viewers_conectados -= 1
    print(f"Viewer saiu. Total: {viewers_conectados}")
    return jsonify({"viewers": viewers_conectados})

def get_viewers_count():
    """Função auxiliar para retornar o número atual de viewers"""
    return viewers_conectados

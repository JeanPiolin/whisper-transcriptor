from flask import Flask, request, jsonify
import whisper
import tempfile
import os

app = Flask(__name__)
modelo = whisper.load_model("base")  # También puedes usar "small"

@app.route('/')
def home():
    return 'Servidor Whisper activo'

@app.route('/transcribir', methods=['POST'])
def transcribir():
    if 'audio' not in request.files:
        return jsonify({"error": "No se encontró el archivo de audio"}), 400

    archivo = request.files['audio']

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        archivo.save(temp_audio.name)
        resultado = modelo.transcribe(temp_audio.name, language="es")
        texto = resultado["text"]
        os.remove(temp_audio.name)

    return jsonify({"transcripcion": texto})

# app.py

import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai.errors import APIError

# Carrega as variáveis de ambiente (do arquivo .env)
load_dotenv()

app = Flask(__name__)

# --- CONFIGURAÇÃO DA GEMINI API ---
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY não encontrada. Verifique seu arquivo .env.")

client = genai.Client(api_key=API_KEY)
MODEL_NAME = "gemini-2.5-flash"


SYSTEM_INSTRUCTION = (
    "Você é o 'Gênio do Futebol', um especialista entusiasmado e informativo. "
    "Suas respostas devem ser focadas em fatos, estatísticas, história, jogadores e campeonatos de futebol. "
    "**Mantenha o tom apaixonado, mas suas respostas devem ser breves, diretas e simples.** " # <<< CHAVE DO AJUSTE
    "Use no máximo 2 a 3 frases por resposta." # <<< NOVO LIMITE
)



# Inicializa o chat fora da rota para manter o histórico e a system instruction
# Nota: Em um ambiente de produção real, você usaria sessões para rastrear o histórico de cada usuário.
chat_session = client.chats.create(
    model=MODEL_NAME,
    config={"systemInstruction": SYSTEM_INSTRUCTION},
    history=[]
)
# --- FIM CONFIGURAÇÃO DA GEMINI API ---


@app.route("/")
def home():
    """Rota que serve o arquivo index.html (a interface do chatbot)."""
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def get_gemini_response():
    """Rota para o JavaScript enviar a mensagem do usuário e receber a resposta do Gemini."""
    
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "Mensagem não fornecida"}), 400

    try:
        # Envia a mensagem para a sessão de chat, mantendo a persona e o histórico
        response = chat_session.send_message(user_message)
        gemini_response = response.text
        
        return jsonify({"response": gemini_response})

    except APIError as e:
        print(f"Erro na API Gemini: {e}")
        return jsonify({"error": "Erro ao processar a resposta da IA."}), 500
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return jsonify({"error": "Erro interno do servidor."}), 500


if __name__ == "__main__":
    print("Iniciando o servidor Flask. Acesse: http://127.0.0.1:5000/")
    app.run(debug=True)
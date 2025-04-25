import requests
import logging
import os
from dotenv import load_dotenv
import asyncio
import json  # Import para log do JSON

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()
GEMINI_API_KEY: str | None = os.environ.get('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    logging.warning("A variável de ambiente GEMINI_API_KEY não está definida.")

GEMINI_TEXT_ENDPOINT: str = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

async def send_to_gemini(chat_history: list) -> str | None:
    """Envia o histórico da conversa para o Gemini e retorna a resposta."""
    if not GEMINI_API_KEY:
        logging.error("A API Key do Gemini não está configurada.")
        return None

    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "key": GEMINI_API_KEY
    }
    furia_context = "Você é um chatbot especializado na FURIA Esports com linguagem atrativa para o público jovem, uma organização brasileira de e-sports. Responda perguntas sobre a FURIA, seus times, jogadores, resultados, notícias e outras informações importantes. Se a pergunta não for sobre a FURIA Esports, diga que você não pode responder. Se a pergunta for relacionada a vazamentos ou detalhes financeiros da FURIA Esports, responda que não possui essa informação."

    logging.info(f"Histórico da conversa sendo enviado: {json.dumps(chat_history, indent=2, ensure_ascii=False)}")

    data = {
        "contents": [{"parts": [{"text": furia_context + "\nHistórico:\n" + "\n".join([f'{msg["role"]}: {msg["parts"][0]["text"]}' for msg in chat_history]) + f'\nPergunta: {chat_history[-1]["parts"][0]["text"]}' if chat_history else furia_context}]}]
    }

    try:
        response = await asyncio.to_thread(requests.post, GEMINI_TEXT_ENDPOINT, headers=headers, params=params, json=data)
        response.raise_for_status()
        return response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text")
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao se comunicar com o Gemini: {e}")
        return None
    except KeyError as e:
        logging.error(f"Erro ao processar resposta do Gemini: {e} - Response: {response.text}")
        return None
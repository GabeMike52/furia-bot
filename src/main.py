from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging
import os
from dotenv import load_dotenv
import sys
import json  # Import para log do JSON
sys.path.append('/home/gabecarneiro/Documents/Projetos/furia-bot/src')
from gemini_integration import send_to_gemini

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='logs/bot.log', filemode='w')
logging.getLogger().setLevel(logging.INFO)

load_dotenv()
TOKEN: Final[str | None] = os.environ.get('TELEGRAM_BOT_TOKEN')
BOT_USERNAME: Final[str | None] = os.environ.get('BOT_USERNAME')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Fala, Furioso(a), bem-vindo ao chatbot da FURIA!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Furioso(a), basta você digitar sua pergunta/dúvida que eu te respondo, beleza?')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('A FURIA Esports é uma organização brasileira que atua em modalidades diversas como CS2, Valorant, Rocket League, LOL, R6, entre outras.')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    chat_id = update.message.chat.id

    logging.info(f'User ({chat_id}) in {message_type}: "{text}"')

    if 'conversation_history' not in context.user_data:
        context.user_data['conversation_history'] = []

    context.user_data['conversation_history'].append({"role": "user", "parts": [{"text": text}]})

    response_gemini = await send_to_gemini(context.user_data['conversation_history'])

    if response_gemini:
        context.user_data['conversation_history'].append({"role": "model", "parts": [{"text": response_gemini}]})
        response: str = response_gemini
    else:
        response: str = "Desculpa, não consegui uma resposta por agora."

    logging.info(f'Bot response to {chat_id}: "{response}"')
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    logging.info('Starting Bot...')
    if not TOKEN:
        logging.critical("A variável de ambiente TELEGRAM_BOT_TOKEN não está definida. O bot não pode ser iniciado.")
    elif not BOT_USERNAME:
        logging.warning("A variável de ambiente BOT_USERNAME não está definida. Algumas funcionalidades podem não funcionar corretamente em grupos.")
    else:
        app = Application.builder().token(TOKEN).build()

        app.add_handler(CommandHandler('start', start_command))
        app.add_handler(CommandHandler('help', help_command))
        app.add_handler(CommandHandler('custom', custom_command))

        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        app.add_error_handler(error)

        logging.info('Checking for new messages...')
        app.run_polling(poll_interval=3)
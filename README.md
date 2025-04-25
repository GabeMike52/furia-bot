# FURIA Telegram Bot

Um bot do Telegram integrado ao Google Gemini para prover respostas relacionadas à FURIA Esports.

O bot foi feito com o BotFather e a integração com o Gemini foi escrita em Python, a integração foi realizada com o modelo gemini-2.0-flash de forma gratuita.

# Como usar?

1. Basta criar um bot simples no BotFather pelo Telegram e pegar o token para uso, assim como o username do bot, ex.: @bot

2. Usar sua conta do Google para gerar uma API Key do Gemini no link: https://aistudio.google.com/app/apikey 

3. Clonar o repositório na sua máquina:
```zsh
git clone https://github.com/GabeMike52/furia-bot
```

4. Instalar as dependências do projeto:
```zsh
pip install -r requirements.txt
```

5. Rodar o projeto:
```zsh
python src/main.py
```

Depois disso, basta falar com o bot que você criou pelo Telegram.
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
import telebot
import threading
from flask import Flask

# --- CONFIGURAÇÃO DO SERVIDOR FANTASMA PARA O KOYEB ---
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot Online!"

def run_flask():
    # Porta 8080 é o padrão do Koyeb
    app.run(host='0.0.0.0', port=8080)

# --- CONFIGURAÇÃO DO BOT ---
TOKEN = '8579259563:AAEYxm0ktGMDBev2R2svYQ4nyVl99CktzuA'
CHAT_ID = '@plugin_oferta'
bot = telebot.TeleBot(TOKEN)

# (Mantenha suas funções extrair_dados e rodar_bot aqui como estavam...)

@bot.message_handler(commands=['start'])
def testar(message):
    bot.reply_to(message, "Bot Online e acompanhando a planilha!")

if __name__ == "__main__":
    # 1. Inicia o Flask em uma thread separada para o Koyeb não matar o processo
    threading.Thread(target=run_flask).start()
    
    print("Bot iniciado...")
    
    # 2. Inicia o loop do seu bot
    # none_stop=True garante que ele não pare se houver erro de rede
    bot.polling(none_stop=True)


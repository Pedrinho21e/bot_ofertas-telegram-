import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
import telebot
import threading
from flask import Flask

# 1. CONFIGURAÇÃO DO SERVIDOR FANTASMA (PARA O KOYEB NÃO DESLIGAR)
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot Online!"

def run_flask():
    # O Koyeb usa a porta 8080 por padrão
    app.run(host='0.0.0.0', port=8080)

# 2. CONFIGURAÇÃO DO BOT (CRIAR A VARIÁVEL 'bot' PRIMEIRO)
TOKEN = '8579259563:AAEYxm0ktGMDBev2R2svYQ4nyVl99CktzuA'
CHAT_ID = '@plugin_oferta' 
# ADICIONE ESTA LINHA EXATAMENTE AQUI:
SHEET_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTtO4yCHk9jG121SV-EHxKWkXDB82kRbFHAWBDF2prrCF/pub?gid=0&single=true&output=csv'
bot = telebot.TeleBot(TOKEN)

# 3. FUNÇÕES DE EXTRAÇÃO (COLOQUE SUAS FUNÇÕES AQUI)
def extrair_dados(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        # ... resto da sua lógica de extração
        return "Dados extraídos"
    except:
        return None


    bot.polling(none_stop=True)
def rodar_bot():
    while True:
        try:
            print("Verificando planilha...")
            df = pd.read_csv(SHEET_URL)
            
            for index, row in df.iterrows():
                # Verifica se o Status na Coluna D está vazio
                if pd.isna(row['Status']) or row['Status'] == '':
                    link = row['Linkes']
                    print(f"Nova oferta encontrada: {link}")
                    
                    # Envia a mensagem para o seu canal @plugin_oferta
                    mensagem = f"🔥 **OFERTA NOVA!**\n\n🔗 {link}"
                    bot.send_message(CHAT_ID, mensagem, parse_mode='Markdown')
                    
                    # DICA: Como é CSV, você precisa marcar como 'Postado' 
                    # manualmente na planilha para ele não repetir.
            
        except Exception as e:
            print(f"Erro na planilha: {e}")
            
        time.sleep(60) # Espera 1 minuto
if __name__ == "__main__":
    # Inicia o servidor para o Koyeb não dar erro de health check
    threading.Thread(target=run_flask).start()
    
    # LIGA O MONITOR DE PLANILHA (O que você acabou de escrever)
    threading.Thread(target=rodar_bot).start()
    
    print("Bot ligado e monitorando a planilha...")
    bot.polling(none_stop=True)





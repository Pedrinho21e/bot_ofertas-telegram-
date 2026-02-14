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
CHAT_ID = '-1003233748780' # Certifique-se que o bot é ADM aqui
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

def rodar_bot():
    # Sua lógica para ler a planilha e enviar mensagens
    def  rodar_bot():
    while True:
        try:
            print("Verificando planilha...")
            # Lê a planilha usando o link que você configurou no SHEET_URL
            df = pd.read_csv(SHEET_URL)
            
            # Percorre cada linha da planilha
            for index, row in df.iterrows():
                # Verifica se a coluna Status está vazia (ou nan)
                if pd.isna(row['Status']) or row['Status'] == '':
                    link = row['Linkes']
                    print(f"Nova oferta encontrada: {link}")
                    
                    # Tenta enviar para o Telegram
                    mensagem = f"🔥 **OFERTA NOVA!**\n\n🔗 {link}"
                    bot.send_message(CHAT_ID, mensagem, parse_mode='Markdown')
                    
                    # Aqui você precisaria de uma lógica para marcar como "Postado"
                    # Como o link de CSV é apenas para leitura, o ideal é você 
                    # escrever manualmente "Postado" na planilha após o bot enviar.
            
        except Exception as e:
            print(f"Erro ao processar planilha: {e}")
            
        time.sleep(60) # Espera 1 minuto para checar de novo

# 4. COMANDOS DO TELEGRAM (APÓS DEFINIR O 'bot')
@bot.message_handler(commands=['start'])
def testar(message):
    bot.reply_to(message, "Bot Online e acompanhando a planilha!")

# 5. INICIALIZAÇÃO

if __name__ == "__main__":
    # Inicia o servidor para o Koyeb não desligar
    threading.Thread(target=run_flask).start()
    
    # INICIA A LEITURA DA PLANILHA EM SEGUNDO PLANO
    threading.Thread(target=rodar_bot).start()
    
    print("Bot iniciado e monitorando planilha...")
    bot.polling(none_stop=True)

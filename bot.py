import telebot
import pandas as pd
import threading
import time
from flask import Flask

# 1. CONFIGURAÇÕES INICIAIS
TOKEN = '8579259563:AAEYxm0ktGMDBev2R2svYQ4nyV199CktzuA'
# Use o ID numérico se o @plugin_oferta der erro de API
CHAT_ID = '@plugin_oferta' 

# AQUI ESTAVA O ERRO: Você precisa definir a variável SHEET_URL aqui em cima
SHEET_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTtO4yCHk9jG121SV-EHxKWkXDB82kRbFHAWBDF2prrCF/pub?gid=0&single=true&output=csv'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot Online!"

def run_flask():
    # O Koyeb usa a porta 8080 por padrão
    app.run(host='0.0.0.0', port=8080)

# 2. FUNÇÃO DE LEITURA DA PLANILHA
def rodar_bot():
    while True:
        try:
            print("Verificando planilha...")
            # Agora SHEET_URL está definida e o bot vai conseguir ler
            df = pd.read_csv(SHEET_URL)
            
            for index, row in df.iterrows():
                # Verifica se a coluna Status na planilha está vazia
                if pd.isna(row['Status']) or row['Status'] == '':
                    link = row['Linkes']
                    print(f"Nova oferta encontrada: {link}")
                    
                    # Envia a mensagem para o Telegram
                    mensagem = f"🔥 **OFERTA NOVA!**\n\n🔗 {link}"
                    bot.send_message(CHAT_ID, mensagem, parse_mode='Markdown')
                    
                    # Nota: Você deve escrever algo na coluna Status da planilha 
                    # manualmente para o bot não repetir a mesma postagem.
            
        except Exception as e:
            print(f"Erro na planilha: {e}")
            
        time.sleep(60) # Espera 1 minuto para checar de novo

# 3. INICIALIZAÇÃO (O CORAÇÃO DO BOT)
if __name__ == "__main__":
    # Inicia o servidor Flask em segundo plano
    threading.Thread(target=run_flask).start()
    
    # Inicia o monitor de planilha em segundo plano
    threading.Thread(target=rodar_bot).start()
    
    print("Bot ligado e monitorando a planilha...")
    bot.polling(none_stop=True)




import telebot
import pandas as pd
import threading
import time
from flask import Flask

# 1. CONFIGURAÇÕES INICIAIS
TOKEN = '8579259563:AAEYxm0ktGMDBev2R2svYQ4nyV199CktzuA'
# DICA: Se o erro de API persistir, use o ID numérico: -1003233748780
CHAT_ID = '@plugin_oferta' 

# DEFINA A VARIÁVEL SHEET_URL AQUI (O seu link CSV)
SHEET_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTtO4yCHk9jG121SV-EHxKWkXDB82kRbFHAWBDF2prrCF/pub?gid=0&single=true&output=csv'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot Online!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# 2. FUNÇÃO DE MONITORAMENTO DA PLANILHA
def rodar_bot():
    while True:
        try:
            print("Verificando planilha...")
            # Agora a variável SHEET_URL está definida corretamente
            df = pd.read_csv(SHEET_URL)
            
            for index, row in df.iterrows():
                # Verifica se a coluna Status está vazia
                if pd.isna(row['Status']) or row['Status'] == '':
                    link = row['Linkes']
                    print(f"Nova oferta encontrada: {link}")
                    
                    # Envia a mensagem para o Telegram
                    mensagem = f"🔥 **OFERTA NOVA!**\n\n🔗 {link}"
                    bot.send_message(CHAT_ID, mensagem, parse_mode='Markdown')
                    
                    # IMPORTANTE: Você precisa marcar como 'Postado' na planilha 
                    # para ele não repetir a mesma mensagem infinitamente.
            
        except Exception as e:
            print(f"Erro na planilha: {e}")
            
        time.sleep(60) # Espera 1 minuto para checar novamente

# 3. INICIALIZAÇÃO
if __name__ == "__main__":
    # Inicia o servidor para o Koyeb não dar erro de saúde
    threading.Thread(target=run_flask).start()
    
    # Inicia o motor de leitura da planilha
    threading.Thread(target=rodar_bot).start()
    
    print("Bot ligado e monitorando a planilha...")
    bot.polling(none_stop=True)

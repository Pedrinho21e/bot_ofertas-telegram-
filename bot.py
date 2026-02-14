import telebot
import pandas as pd
import threading
import time
from flask import Flask

# 1. CONFIGURAÇÕES INICIAIS
TOKEN = '8579259563:AAEYxm0ktGMDBev2R2svYQ4nyV199CktzuA'
# Usando o ID numérico para evitar erros de 'Bad Request' no Telegram
CHAT_ID = -1003233748780 

# AQUI ESTAVA O ERRO: Definindo o link CSV publico da sua planilha
SHEET_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTtO4yCHk9jG121SV-EHxKWkXDB82kRbFHAWBDF2prrCF/pub?gid=0&single=true&output=csv'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot Online!"

def run_flask():
    # Porta 8080 exigida pelo Koyeb
    app.run(host='0.0.0.0', port=8080)

# 2. MOTOR DE MONITORAMENTO DA PLANILHA
def rodar_bot():
    while True:
        try:
            print("Verificando planilha...")
            # Agora a variável SHEET_URL existe e o bot consegue ler os dados
            df = pd.read_csv(SHEET_URL)
            
            for index, row in df.iterrows():
                # Verifica se a coluna Status (Coluna D) está vazia (NaN ou '')
                if pd.isna(row['Status']) or str(row['Status']).strip() == '':
                    link = row['Linkes']
                    print(f"Nova oferta encontrada: {link}")
                    
                    # Monta e envia a mensagem para o Telegram
                    mensagem = f"🔥 **OFERTA NOVA!**\n\n🔗 {link}"
                    bot.send_message(CHAT_ID, mensagem, parse_mode='Markdown')
                    
                    # DICA: Você deve escrever 'Postado' na planilha manualmente 
                    # para que o bot não envie o mesmo link de novo no próximo minuto.
            
        except Exception as e:
            print(f"Erro na planilha: {e}")
            
        time.sleep(60) # Checa a planilha a cada 1 minuto

# 3. INICIALIZAÇÃO (Threading)
if __name__ == "__main__":
    # Inicia o Flask (Saúde da Instância no Koyeb)
    threading.Thread(target=run_flask).start()
    
    # Inicia o monitor de ofertas
    threading.Thread(target=rodar_bot).start()
    
    print("Bot ligado e monitorando a planilha...")
    bot.polling(none_stop=True)

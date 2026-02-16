import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import threading
import time
from flask import Flask
import os
import json
import requests
from bs4 import BeautifulSoup

# 1. CONFIGURAÇÕES
TOKEN = '8579259563:AAEYxm0ktGMDBev2R2svYQ4nyV199CktzuA'
CHAT_ID =@Plugln_Ofertas
NOME_DA_PLANILHA = "Linkes,Status"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def index(): return "Bot de Scraping Automático Online!"

# 2. FUNÇÃO PARA PEGAR DADOS DO SITE (SCRAPING)
def extrair_dados_do_link(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tenta pegar o título (funciona na maioria dos sites)
        titulo = soup.find('meta', property='og:title')
        titulo = titulo['content'] if titulo else "Oferta Incrível!"
        
        # Tenta pegar a imagem principal
        imagem = soup.find('meta', property='og:image')
        imagem_url = imagem['content'] if imagem else None
        
        return titulo, imagem_url
    except:
        return "Confira essa oferta!", None

def conectar_google():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_json = json.loads(os.environ.get('GOOGLE_CREDS'))
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
    return gspread.authorize(creds)

# 3. MONITORAMENTO AUTOMÁTICO
def rodar_bot():
    client = conectar_google()
    sheet = client.open(NOME_DA_PLANILHA).sheet1
    
    while True:
        try:
            dados = sheet.get_all_records()
            for i, linha in enumerate(dados, start=2):
                status = str(linha.get('Status', '')).strip()
                link = linha.get('Linkes', '')
                
                if status == '' and link != '':
                    # O BOT FAZ O TRABALHO SOZINHO AQUI:
                    titulo, foto_url = extrair_dados_do_link(link)
                    
                    legenda = f"🔥 **{titulo}**\n\n🔗 [CLIQUE AQUI PARA APROVEITAR]({link})"
                    
                    if foto_url:
                        bot.send_photo(CHAT_ID, foto_url, caption=legenda, parse_mode='Markdown')
                    else:
                        bot.send_message(CHAT_ID, legenda, parse_mode='Markdown')
                    
                    sheet.update_cell(i, 4, "Postado") # Marca na coluna D
                    print(f"Postado: {titulo}")
                    
        except Exception as e:
            print(f"Erro no monitor: {e}")
            
        time.sleep(60)

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()
    threading.Thread(target=rodar_bot).start()
    bot.polling(none_stop=True)





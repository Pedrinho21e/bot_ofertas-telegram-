import telebot
import feedparser
import time
import random
import os
from telebot import types

# Configurações via Variáveis de Ambiente (Padrão Railway)
TOKEN = os.getenv("8579259563:AAFE9yqbX4oT0Ek9e499JEPUcwkBEMak0Xs")
CHAT_ID = os.getenv("@plugin_oferta")
bot = telebot.TeleBot(TOKEN)

FONTES_RSS = [
    "https://www.pelando.com.br/rss",
    "https://www.promobit.com.br/feed/"
]

links_postados = set()
contador_lista = 0

def postar_minha_lista():
    try:
        with open("produto.txt", "r", encoding="utf-8") as f:
            linhas = [l.strip() for l in f.readlines() if ";" in l]
        if linhas:
            item = random.choice(linhas)
            nome, link = item.split(";")
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text="🛒 COMPRAR AGORA", url=link.strip()))
            bot.send_message(CHAT_ID, f"🌟 <b>OFERTA SELECIONADA</b>\n\n{nome}", reply_markup=markup, parse_mode="HTML")
    except Exception as e:
        print(f"Erro na lista: {e}")

def buscar_ofertas():
    global contador_lista
    for url in FONTES_RSS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:3]: 
                if entry.link not in links_postados:
                    markup = types.InlineKeyboardMarkup()
                    markup.add(types.InlineKeyboardButton(text="🔥 VER PROMOÇÃO", url=entry.link))
                    bot.send_message(CHAT_ID, f"📢 <b>NOVIDADE!</b>\n\n{entry.title}", reply_markup=markup, parse_mode="HTML")
                    links_postados.add(entry.link)
                    contador_lista += 1
                    if contador_lista >= 2:
                        time.sleep(5)
                        postar_minha_lista()
                        contador_lista = 0
                    time.sleep(10)
        except:
            pass

print("🚀 Bot Railway Iniciado!")
while True:
    buscar_ofertas()
    time.sleep(120)












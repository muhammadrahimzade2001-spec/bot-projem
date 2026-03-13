import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# 1. BOT AYARLARI
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 2. WEB (KEEP-ALIVE) SİSTEMİ - Botu 7/24 uyanık tutar
app = Flask('')
@app.route('/')
def home():
    return "Bot aktif!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

# 3. BOT OLAYLARI VE KOMUTLARI
@bot.event
async def on_ready():
    print(f'{bot.user} başarıyla bağlandı!')

@bot.command()
async def yardim(ctx):
    embed = discord.Embed(
        title="🤖 MesxeZe Bot Yardım Menüsü",
        description="Komutlar aşağıda listelenmiştir:",
        color=discord.Color.blue()
    )
    embed.add_field(name="🛠️ Destek", value="`!destek` - Yetkili ekibe ulaş.", inline=False)
    embed.add_field(name="ℹ️ Durum", value="`!bilgi` - Botun sürümünü göster.", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def destek(ctx):
    embed = discord.Embed(
        title="🎫 Destek Talebi",
        description="Yetkili ekibimize ulaşmak için şu kanalı kontrol et.",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

# 4. BAŞLATMA
if __name__ == "__main__":
    # Web sunucusunu başlat
    Thread(target=run_web).start()
    
    # Botu başlat
    token = os.environ['TOKEN']
    bot.run(token)

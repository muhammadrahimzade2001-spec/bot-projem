import discord
from discord.ext import commands
from discord import app_commands
import os
from flask import Flask
from threading import Thread

# --- WEB SUNUCUSU (Render Kapatmasın Diye) ---
app = Flask('')
@app.route('/')
def home(): return "Bot Aktif!"
def run(): app.run(host='0.0.0.0', port=8080)

# --- BOT AYARLARI ---
intents = discord.Intents.default()
intents.members = True
intents.message_content = True # Burayı portalda açmayı unutma kanka!
bot = commands.Bot(command_prefix="!", intents=intents)

user_points = {}

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'{bot.user} aktif ve ölümsüz!')

@bot.event
async def on_message(message):
    if message.author.bot: return
    user_points[message.author.id] = user_points.get(message.author.id, 0) + 1
    await bot.process_commands(message)

# --- TICKET SİSTEMİ ---
class DestekSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Klan Alımı", emoji="🛡️"),
            discord.SelectOption(label="Klan İçi Sorun", emoji="⚠️"),
            discord.SelectOption(label="Etkinlik Önerisi", emoji="💡"),
            discord.SelectOption(label="Diğer", emoji="📦")
        ]
        super().__init__(placeholder="Kategori seçiniz...", options=options)

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        channel = await guild.create_text_channel(name=f"ticket-{interaction.user.name.lower()}", overwrites=overwrites)
        await interaction.response.send_message(f"Kanal açıldı: {channel.mention}", ephemeral=True)
        await channel.send(f"🛡️ **MesxeZe Destek**\nHoş geldin {interaction.user.mention}! Yetkililer birazdan burada olacak.")

class DestekView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DestekSelect())

@bot.tree.command(name="destek", description="Destek talebi açar")
async def destek(interaction: discord.Interaction):
    await interaction.response.send_message("Kategori seçin:", view=DestekView())

# --- BOTU BAŞLAT ---
Thread(target=run).start() # Web sunucusunu başlat
bot.run(os.environ['TOKEN'])

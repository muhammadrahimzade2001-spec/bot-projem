import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View
import asyncio

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- 1. DESTEK SİSTEMİ (BUTONLU) ---
class CloseView(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Talebi Kapat", style=discord.ButtonStyle.danger, emoji="🔒")
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Kanal 5 saniye içinde siliniyor...", ephemeral=True)
        await asyncio.sleep(5)
        await interaction.channel.delete()

class DestekView(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Destek Aç", style=discord.ButtonStyle.success, emoji="📩")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        overwrites = {guild.default_role: discord.PermissionOverwrite(read_messages=False), 
                      interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True)}
        channel = await guild.create_text_channel(f'destek-{interaction.user.name}', overwrites=overwrites)
        await channel.send(f"{interaction.user.mention} hoş geldin! Yetkililer ilgilenecek.", view=CloseView())
        await interaction.response.send_message(f"✅ Kanal açıldı: {channel.mention}", ephemeral=True)

# --- 2. SLASH KOMUTLARI ---
@bot.event
async def on_ready():
    await bot.tree.sync() # Komutları Discord'a tanıt
    await bot.change_presence(activity=discord.Game(name="/yardım"))
    print(f'{bot.user} hazır ve slash komutları yüklendi!')

@bot.tree.command(name="yardım", description="Tüm komutları listeler")
async def yardım(interaction: discord.Interaction):
    embed = discord.Embed(title="🚀 MesxeZeBOT Menüsü", color=discord.Color.purple())
    embed.add_field(name="🛠️ Moderasyon", value="/sil, /ban, /kick, /mute", inline=False)
    embed.add_field(name="🎟️ Destek", value="/destek", inline=False)
    embed.add_field(name="👤 Kullanıcı", value="/avatar, /kullanıcıbilgi, /ping", inline=False)
    embed.add_field(name="🔗 Genel", value="/davet, /sunucubilgi", inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="sil", description="Mesaj siler")
async def sil(interaction: discord.Interaction, miktar: int):
    await interaction.channel.purge(limit=miktar)
    await interaction.response.send_message(f"✅ {miktar} mesaj silindi!", ephemeral=True)

@bot.tree.command(name="ban", description="Kullanıcıyı yasaklar")
async def ban(interaction: discord.Interaction, üye: discord.Member):
    await üye.ban()
    await interaction.response.send_message(f"🔨 {üye.name} yasaklandı.")

@bot.tree.command(name="kick", description="Kullanıcıyı atar")
async def kick(interaction: discord.Interaction, üye: discord.Member):
    await üye.kick()
    await interaction.response.send_message(f"👢 {üye.name} sunucudan atıldı.")

@bot.tree.command(name="avatar", description="Kullanıcının avatarını gösterir")
async def avatar(interaction: discord.Interaction, üye: discord.Member = None):
    üye = üye or interaction.user
    await interaction.response.send_message(üye.avatar.url)

@bot.tree.command(name="ping", description="Botun gecikmesini ölçer")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"🏓 Pong! {round(bot.latency * 1000)}ms")

@bot.tree.command(name="destek", description="Destek sistemi panelini açar")
async def destek(interaction: discord.Interaction):
    await interaction.response.send_message("📩 **Destek Paneli**", view=DestekView())

@bot.tree.command(name="davet", description="Sunucu davet linkini verir")
async def davet(interaction: discord.Interaction):
    await interaction.response.send_message("🔗 Davet: https://discord.gg/sunucun")

import os
# ... senin diğer kodların ...

# En altta sadece bu olsun:
token = os.environ.get('MTQ4MTkzODkwNjYwMDcwMjAwNA.GrRjuV.CAIEMWbX6t1YnJ2UtFQ36cyILL_1PSUD6oJHZU')
bot.run(token)

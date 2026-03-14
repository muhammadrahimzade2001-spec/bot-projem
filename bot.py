import discord
from discord.ext import commands
from discord import app_commands
import os
from flask import Flask
from threading import Thread
import random

# --- RENDER CANLI TUTMA ---
app = Flask('')
@app.route('/')
def home(): return "Klan Pro Bot Aktif!"
def run(): app.run(host='0.0.0.0', port=8080)

# --- BOT AYARLARI ---
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)

klan_puani = {} # Puan verileri

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'🔥 {bot.user} Gelişmiş Klan Botu Aktif!')

# --- EKONOMİ VE PUAN ---
@bot.tree.command(name="profil", description="Puanını gösterir")
async def profil(interaction: discord.Interaction, uye: discord.Member = None):
    target = uye or interaction.user
    puan = klan_puani.get(target.id, 0)
    embed = discord.Embed(title=f"🛡️ {target.name} Profili", description=f"💰 **Klan Puanı:** {puan} KP", color=discord.Color.gold())
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="gonder", description="Puan gönderir")
async def gonder(interaction: discord.Interaction, uye: discord.Member, miktar: int):
    sender_puan = klan_puani.get(interaction.user.id, 0)
    if sender_puan < miktar or miktar <= 0:
        return await interaction.response.send_message("Yetersiz bakiye veya geçersiz miktar!", ephemeral=True)
    klan_puani[interaction.user.id] -= miktar
    klan_puani[uye.id] = klan_puani.get(uye.id, 0) + miktar
    await interaction.response.send_message(f"✅ {uye.mention} kullanıcısına {miktar} KP gönderildi!")

@bot.tree.command(name="top", description="Zenginlik sıralaması")
async def top(interaction: discord.Interaction):
    sorted_list = sorted(klan_puani.items(), key=lambda x: x[1], reverse=True)[:10]
    embed = discord.Embed(title="🏆 MesxeZe En Zenginler", color=discord.Color.blue())
    for i, (uid, pts) in enumerate(sorted_list, 1):
        m = interaction.guild.get_member(uid)
        name = m.name if m else "Eski Üye"
        embed.add_field(name=f"{i}. {name}", value=f"{pts} KP", inline=False)
    await interaction.response.send_message(embed=embed)

# --- YÖNETİM ---
@bot.tree.command(name="klan-duyuru", description="Klan duyurusu atar")
@app_commands.checks.has_permissions(administrator=True)
async def klan_duyuru(interaction: discord.Interaction, mesaj: str):
    embed = discord.Embed(title="📢 DUYURU", description=mesaj, color=discord.Color.red())
    await interaction.channel.send(content="@everyone", embed=embed)
    await interaction.response.send_message("Duyuru atıldı.", ephemeral=True)

@bot.tree.command(name="rol-ver", description="Rol verir")
@app_commands.checks.has_permissions(manage_roles=True)
async def rol_ver(interaction: discord.Interaction, uye: discord.Member, rol: discord.Role):
    await uye.add_roles(rol)
    await interaction.response.send_message(f"✅ {rol.name} rolü verildi.")

@bot.tree.command(name="temizle", description="Mesajları siler")
@app_commands.checks.has_permissions(manage_messages=True)
async def temizle(interaction: discord.Interaction, miktar: int):
    await interaction.channel.purge(limit=miktar)
    await interaction.response.send_message(f"🧹 {miktar} mesaj temizlendi.", ephemeral=True)

# --- TICKET ---
class TicketKapat(discord.ui.View):
    @discord.ui.button(label="Kapat", style=discord.ButtonStyle.danger)
    async def kapat(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.channel.delete()

class DestekSelect(discord.ui.Select):
    def __init__(self):
        super().__init__(placeholder="Konu seç...", options=[discord.SelectOption(label="Alım"), discord.SelectOption(label="Şikayet")])
    async def callback(self, interaction: discord.Interaction):
        overwrites = {interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False), interaction.user: discord.PermissionOverwrite(read_messages=True), interaction.guild.me: discord.PermissionOverwrite(read_messages=True)}
        ch = await interaction.guild.create_text_channel(name=f"destek-{interaction.user.name}", overwrites=overwrites)
        await interaction.response.send_message(f"Kanal: {ch.mention}", ephemeral=True)
        await ch.send("Hoş geldin! İşin bitince kapat.", view=TicketKapat())

@bot.tree.command(name="destek", description="Ticket açar")
async def destek(interaction: discord.Interaction):
    v = discord.ui.View(); v.add_item(DestekSelect())
    await interaction.response.send_message("Kategori seç:", view=v)

# --- EĞLENCE ---
@bot.tree.command(name="yazi-tura", description="Yazı-Tura atar")
async def yazi_tura(interaction: discord.Interaction):
    await interaction.response.send_message(f"🪙 Sonuç: **{random.choice(['Yazı', 'Tura'])}**")

Thread(target=run).start()
bot.run(os.environ['TOKEN'])

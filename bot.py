import discord
from discord.ext import commands
from discord import app_commands
import os
from flask import Flask
from threading import Thread

# --- RENDER CANLI TUTMA ---
app = Flask('')
@app.route('/')
def home(): return "🛡️ MesxeZe Kayıt Sistemi Aktif!"
def run(): app.run(host='0.0.0.0', port=8081)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'✅ {bot.user} Kayıt Botu Başlatıldı!')

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="hoş-geldin")
    if channel:
        embed = discord.Embed(
            title="✨ Aramıza Yeni Bir Savaşçı Katıldı!",
            description=f"Selam {member.mention}, **MesxeZe** ailesine hoş geldin!\nLütfen kayıt için beklemede kal.",
            color=discord.Color.from_rgb(46, 204, 113)
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text="MesxeZe Guard Sistemi")
        await channel.send(embed=embed)

@bot.tree.command(name="kayit", description="Üyeyi klan düzenine göre isimlendirir")
@app_commands.checks.has_permissions(manage_nicknames=True)
async def kayit(interaction: discord.Interaction, uye: discord.Member, yeni_isim: str):
    old_name = uye.display_name
    await uye.edit(nick=yeni_isim)
    embed = discord.Embed(title="📝 Kayıt İşlemi Başarılı", color=discord.Color.blue())
    embed.add_field(name="Eski İsim", value=old_name, inline=True)
    embed.add_field(name="Yeni İsim", value=yeni_isim, inline=True)
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
    await interaction.response.send_message(embed=embed, ephemeral=True)

Thread(target=run).start()
bot.run(os.environ['TOKEN'])

import discord
from discord.ext import commands
from discord import app_commands
import os
from flask import Flask
from threading import Thread
import random
import datetime

# --- RENDER CANLI TUTMA ---
app = Flask('')
@app.route('/')
def home(): return "🛡️ KnavesDC Minecraft Botu Aktif!"
def run(): app.run(host='0.0.0.0', port=8080)

# --- BOT AYARLARI ---
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    activity = discord.Game(name="🛡️ KnavesDC Minecraft")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f'🚀 KnavesDC Botu "{bot.user}" olarak hazır!')

# --- MC SUNUCU KOMUTLARI ---

@bot.tree.command(name="ip", description="Minecraft sunucu adresini gösterir")
async def ip(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎮 KnavesDC Sunucu Bilgisi",
        description="Aşağıdaki IP adresini kullanarak sunucuya katılabilirsin!",
        color=discord.Color.green()
    )
    embed.add_field(name="📌 Sunucu IP", value="`tr-1.mangoohost.com.tr:26520`", inline=False)
    embed.set_footer(text="İyi oyunlar dileriz!")
    await interaction.response.send_message(embed=embed)

# --- YÖNETİM KOMUTLARI (MODERASYON) ---

@bot.tree.command(name="duyuru", description="Klan üyelerine duyuru yapar")
@app_commands.checks.has_permissions(administrator=True)
async def duyuru(interaction: discord.Interaction, mesaj: str):
    embed = discord.Embed(title="📢 KNAVESDC DUYURU", description=mesaj, color=discord.Color.red(), timestamp=datetime.datetime.now())
    embed.set_thumbnail(url=interaction.guild.icon.url if interaction.guild.icon else None)
    await interaction.channel.send(content="@everyone", embed=embed)
    await interaction.response.send_message("✅ Duyuru başarıyla gönderildi.", ephemeral=True)

@bot.tree.command(name="temizle", description="Sohbeti temizler")
@app_commands.checks.has_permissions(manage_messages=True)
async def temizle(interaction: discord.Interaction, miktar: int):
    await interaction.channel.purge(limit=miktar)
    await interaction.response.send_message(f"🧹 `{miktar}` mesaj silindi.", ephemeral=True)

@bot.tree.command(name="rol-ver", description="Üyeye rol verir")
@app_commands.checks.has_permissions(manage_roles=True)
async def rol_ver(interaction: discord.Interaction, uye: discord.Member, rol: discord.Role):
    await uye.add_roles(rol)
    await interaction.response.send_message(f"✅ {uye.mention} kullanıcısına **{rol.name}** rolü eklendi.")

@bot.tree.command(name="rol-al", description="Üyeden rol alır")
@app_commands.checks.has_permissions(manage_roles=True)
async def rol_al(interaction: discord.Interaction, uye: discord.Member, rol: discord.Role):
    await uye.remove_roles(rol)
    await interaction.response.send_message(f"❌ {uye.mention} kullanıcısından **{rol.name}** rolü alındı.")

@bot.tree.command(name="at", description="Üyeyi klandan atar")
@app_commands.checks.has_permissions(kick_members=True)
async def at(interaction: discord.Interaction, uye: discord.Member, sebep: str = "Yok"):
    await uye.kick(reason=sebep)
    await interaction.response.send_message(f"👞 {uye.name} klandan atıldı. Sebep: {sebep}")

@bot.tree.command(name="yasakla", description="Üyeyi klandan banlar")
@app_commands.checks.has_permissions(ban_members=True)
async def yasakla(interaction: discord.Interaction, uye: discord.Member, sebep: str = "Yok"):
    await uye.ban(reason=sebep)
    await interaction.response.send_message(f"🚫 {uye.name} klandan kalıcı olarak yasaklandı!")

# --- GELİŞMİŞ TICKET SİSTEMİ (BUTONLU) ---

class TicketKapat(discord.ui.View):
    @discord.ui.button(label="Talebi Kapat", style=discord.ButtonStyle.danger, emoji="🔒")
    async def kapat(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🔒 Bu kanal 5 saniye içinde silinecek...")
        await interaction.channel.delete()

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Destek Talebi Aç", style=discord.ButtonStyle.primary, emoji="🎫", custom_id="knaves_ticket")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        channel = await guild.create_text_channel(name=f"ticket-{interaction.user.name}", overwrites=overwrites)
        await interaction.response.send_message(f"✅ Destek kanalın açıldı: {channel.mention}", ephemeral=True)
        
        embed = discord.Embed(title="🎫 KnavesDC Destek", description=f"Hoş geldin {interaction.user.mention}, sorunun nedir?", color=discord.Color.blue())
        await channel.send(embed=embed, view=TicketKapat())

@bot.tree.command(name="ticket-kur", description="Butonlu ticket sistemini başlatır")
@app_commands.checks.has_permissions(administrator=True)
async def ticket_kur(interaction: discord.Interaction):
    embed = discord.Embed(title="🎫 Destek & Alım Merkezi", description="Bir sorun bildirmek veya klana katılmak için butona bas!", color=discord.Color.dark_gray())
    await interaction.channel.send(embed=embed, view=TicketView())
    await interaction.response.send_message("✅ Ticket sistemi aktif.", ephemeral=True)

# --- EĞLENCE & BİLGİ ---

@bot.tree.command(name="yazi-tura", description="Yazı-Tura atar")
async def yazi_tura(interaction: discord.Interaction):
    res = random.choice(["Yazı", "Tura"])
    await interaction.response.send_message(f"🪙 Sonuç: **{res}**")

@bot.tree.command(name="sunucu-bilgi", description="Sunucu durumunu gösterir")
async def sunucu_bilgi(interaction: discord.Interaction):
    g = interaction.guild
    embed = discord.Embed(title=f"📊 {g.name} İstatistikleri", color=discord.Color.blue())
    embed.add_field(name="Üye Sayısı", value=g.member_count)
    embed.add_field(name="Kanal Sayısı", value=len(g.channels))
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="kullanici-bilgi", description="Bir üyenin bilgilerini gösterir")
async def user_info(interaction: discord.Interaction, uye: discord.Member = None):
    target = uye or interaction.user
    embed = discord.Embed(title=f"👤 {target.name} Bilgileri", color=target.color)
    embed.add_field(name="ID", value=target.id)
    embed.add_field(name="Katılma Tarihi", value=target.joined_at.strftime("%d/%m/%Y"))
    embed.set_thumbnail(url=target.display_avatar.url)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="rastgele-sec", description="Klandan şanslı birini seçer")
async def rastgele(interaction: discord.Interaction):
    m = random.choice(interaction.guild.members)
    await interaction.response.send_message(f"🎲 Şanslı Savaşçı: {m.mention}")

@bot.tree.command(name="yardim", description="Tüm komutları listeler")
async def yardim(interaction: discord.Interaction):
    text = """
    **🎮 Oyun:** /ip
    **🎫 Destek:** /ticket-kur, /destek
    **⚙️ Yönetim:** /duyuru, /temizle, /rol-ver, /rol-al, /at, /yasakla
    **🎲 Eğlence:** /yazi-tura, /rastgele-sec, /sunucu-bilgi, /kullanici-bilgi
    """
    await interaction.response.send_message(text)

# --- BOTU BAŞLAT ---
Thread(target=run).start()
bot.run(os.environ['TOKEN'])

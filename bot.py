import discord
from discord.ext import commands
from discord import app_commands
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Ekonomi sistemi
user_points = {}

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'{bot.user} aktif ve komutlar senkronize edildi!')

@bot.event
async def on_message(message):
    if message.author.bot: return
    user_points[message.author.id] = user_points.get(message.author.id, 0) + 1
    await bot.process_commands(message)

# Destek Menüsü
async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        kategori_adi = self.values[0]
        
        # Yetkililerin görebileceği özel izinler
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        # Yeni kanal oluştur
        kanal_ismi = f"ticket-{interaction.user.name}"
        channel = await guild.create_text_channel(name=kanal_ismi, overwrites=overwrites)
        
        # Kanala ilk mesajı at
        embed = discord.Embed(title=f"🎫 {kategori_adi} Talebi", description=f"{interaction.user.mention}, yetkililerimiz seninle ilgilenecek.", color=discord.Color.green())
        await channel.send(embed=embed)
        
        # Kullanıcıya bilgi ver
        await interaction.response.send_message(f"Ticket kanalın açıldı: {channel.mention}", ephemeral=True)
        ]
        super().__init__(placeholder="Kategori seçiniz...", options=options)
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Seçimin: {self.values[0]}. Yetkililer ilgilenecek.", ephemeral=True)

class DestekView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DestekSelect())

# Slash Komutları
@bot.tree.command(name="destek", description="Destek açar")
async def destek(interaction: discord.Interaction):
    await interaction.response.send_message("Kategori seç:", view=DestekView())

@bot.tree.command(name="top", description="Sıralama")
async def top(interaction: discord.Interaction):
    sorted_users = sorted(user_points.items(), key=lambda x: x[1], reverse=True)[:5]
    embed = discord.Embed(title="🏆 Klan Aktiflik Sıralaması", color=discord.Color.gold())
    for i, (uid, pts) in enumerate(sorted_users, 1):
        member = interaction.guild.get_member(uid)
        name = member.name if member else "Bilinmeyen"
        embed.add_field(name=f"{i}. {name}", value=f"{pts} Puan", inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="yardim", description="Yardım menüsü")
async def yardim(interaction: discord.Interaction):
    await interaction.response.send_message("Komutlar: /destek, /top, /yardim")

bot.run(os.environ['TOKEN'])

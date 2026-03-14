import discord
from discord.ext import commands
from discord import app_commands
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

user_points = {}

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'{bot.user} aktif ve kanallar senkronize!')

@bot.event
async def on_message(message):
    if message.author.bot: return
    user_points[message.author.id] = user_points.get(message.author.id, 0) + 1
    await bot.process_commands(message)

# --- GERÇEK TICKET SİSTEMİ ---
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
        kategori_adi = self.values[0]
        
        # Kanal izinlerini ayarla
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        # Yeni kanal oluştur
        kanal_ismi = f"ticket-{interaction.user.name.lower()}"
        channel = await guild.create_text_channel(name=kanal_ismi, overwrites=overwrites)
        
        await interaction.response.send_message(f"Ticket kanalın oluşturuldu: {channel.mention}", ephemeral=True)
        await channel.send(f"🛡️ **MesxeZe Destek**\nHoş geldin {interaction.user.mention}! Konu: **{kategori_adi}**. Yetkililer birazdan burada olacak.")

class DestekView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DestekSelect())

@bot.tree.command(name="destek", description="Destek talebi açar")
async def destek(interaction: discord.Interaction):
    await interaction.response.send_message("Destek almak için kategori seçin:", view=DestekView())

@bot.tree.command(name="top", description="Sıralama")
async def top(interaction: discord.Interaction):
    sorted_users = sorted(user_points.items(), key=lambda x: x[1], reverse=True)[:5]
    embed = discord.Embed(title="🏆 Klan Aktiflik Sıralaması", color=discord.Color.gold())
    for i, (uid, pts) in enumerate(sorted_users, 1):
        member = interaction.guild.get_member(uid)
        name = member.name if member else "Bilinmeyen"
        embed.add_field(name=f"{i}. {name}", value=f"{pts} Puan", inline=False)
    await interaction.response.send_message(embed=embed)

bot.run(os.environ['TOKEN'])

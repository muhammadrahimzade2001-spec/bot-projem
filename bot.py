import discord
from discord.ext import commands
from discord import app_commands
import os

# İntents ayarları
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync() # Slash komutlarını senkronize et
    print(f'{bot.user} aktif!')

# --- DESTEK SİSTEMİ (Select Menu) ---
class DestekSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Klan Alımı", description="Klanımıza katılmak istiyorum", emoji="🛡️"),
            discord.SelectOption(label="Klan İçi Sorun", description="Bir üyeyle sorunum var", emoji="⚠️"),
            discord.SelectOption(label="Etkinlik Önerisi", description="Güzel bir fikrim var", emoji="💡"),
            discord.SelectOption(label="Diğer", description="Başka bir konu", emoji="📦")
        
        super().__init__(placeholder="Destek konusu seçiniz...", options=options)

    async def callback(self, interaction: discord.Interaction):
        # Yetkililere mesaj göndermek istersen burayı değiştirebiliriz
        await interaction.response.send_message(f"Destek talebin alındı: **{self.values[0]}**. Yetkililerimiz en kısa sürede dönüş yapacaktır!", ephemeral=True)
        ]
        super().__init__(placeholder="Kategori seçiniz...", options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Seçilen kategori: {self.values[0]}. Yetkililer ilgilenecek!", ephemeral=True)

class DestekView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DestekSelect())

# --- KOMUTLAR ---
@bot.tree.command(name="yardim", description="Yardım menüsü")
async def yardim(interaction: discord.Interaction):
    embed = discord.Embed(title="🤖 MesxeZe Yardım Menüsü", color=discord.Color.gold())
    embed.add_field(name="🛠️ Yönetim", value="/sil, /ban, /mute, /kick", inline=False)
    embed.add_field(name="ℹ️ Genel", value="/sunucubilgi, /avatar, /ping, /davet", inline=False)
    embed.add_field(name="🎫 Destek", value="/destek", inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="destek", description="Destek sistemi")
async def destek(interaction: discord.Interaction):
    embed = discord.Embed(title="🎫 MesxeZe - Destek", description="Desteğe ihtiyacınız varsa aşağıdaki kısımdan kategori seçin.", color=discord.Color.purple())
    await interaction.response.send_message(embed=embed, view=DestekView())

@bot.tree.command(name="sunucubilgi", description="Sunucu bilgisi")
async def sunucubilgi(interaction: discord.Interaction):
    guild = interaction.guild
    await interaction.response.send_message(f"Sunucu: {guild.name}\nÜye Sayısı: {guild.member_count}")

@bot.tree.command(name="avatar", description="Kullanıcı avatarı")
async def avatar(interaction: discord.Interaction, user: discord.Member = None):
    user = user or interaction.user
    await interaction.response.send_message(user.avatar.url)

@bot.tree.command(name="ping", description="Gecikme süresi")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {round(bot.latency * 1000)}ms")

# --- YÖNETİM KOMUTLARI ---
@bot.tree.command(name="sil", description="Mesaj silme")
@app_commands.checks.has_permissions(manage_messages=True)
async def sil(interaction: discord.Interaction, miktar: int):
    await interaction.channel.purge(limit=miktar)
    await interaction.response.send_message(f"{miktar} mesaj silindi.", ephemeral=True)

@bot.tree.command(name="ban", description="Ban atar")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, user: discord.Member):
    await user.ban()
    await interaction.response.send_message(f"{user.name} yasaklandı!")

# --- DAVET SİSTEMİ (Basit haliyle) ---
@bot.tree.command(name="davet", description="Kaç kişiyi davet ettiğini gösterir")
async def davet(interaction: discord.Interaction):
    invites = await interaction.guild.invites()
    user_invites = sum(invite.uses for invite in invites if invite.inviter == interaction.user)
    await interaction.response.send_message(f"Sunucuya şu ana kadar {user_invites} kişi davet ettin!")

# Başlat
bot.run(os.environ['TOKEN'])

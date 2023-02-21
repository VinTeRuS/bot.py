import discord
from discord.ext import commands
import random

TOKEN = "ваш токен"

client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
    print("Бот готов к работе")

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member} был кикнут с сервера")

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member} был забанен на сервере")

@client.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(muted_role, reason=reason)
    await ctx.send(f"{member} был замьючен на сервере")

@client.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member, *, reason=None):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(muted_role, reason=reason)
    await ctx.send(f"{member} был размьючен на сервере")

@client.command()
async def serverinfo(ctx):
    server = ctx.guild
    total_members = server.member_count
    online_members = len([m for m in server.members if m.status != discord.Status.offline])
    text_channels = len(server.text_channels)
    voice_channels = len(server.voice_channels)
    embed = discord.Embed(title=server.name, description=server.description)
    embed.add_field(name="Участники", value=f"Всего: {total_members}\nОнлайн: {online_members}")
    embed.add_field(name="Текстовые каналы", value=text_channels)
    embed.add_field(name="Голосовые каналы", value=voice_channels)
    await ctx.send(embed=embed)

@client.command()
async def userinfo(ctx, member: discord.Member):
    embed = discord.Embed(title=member.name, description=member.mention)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Присоединился", value=member.joined_at.strftime("%d.%m.%Y %H:%M:%S"), inline=True)
    embed.add_field(name="Аккаунт создан", value=member.created_at.strftime("%d.%m.%Y %H:%M:%S"), inline=True)
    embed.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed=embed)

@client.command()
async def cat(ctx):
    cat_urls = [
        "https://i.imgur.com/KYnMwWe.jpeg",
        "https://i.imgur.com/cyHNGkT.jpeg",
        "https://i.imgur.com/3Z3b7UJ.jpeg",
        "https://i.imgur.com/MCmV7LN.jpeg",
        "https://i.imgur.com/r4cB4M4.jpeg",
        "https://i.imgur.com/jZiVT10.jpeg",
        "https://i.imgur.com/3gElqxu.jpeg",
        "https://i.imgur.com/vaOZ6rK.jpeg",
        "https://i.imgur.com/HwTJ7Vd.jpeg"
    ]
    cat_url = random.choice(cat_urls)
    embed = discord.Embed(title="Random Cat", description="Random photo of a cat")
    embed.set_image(url=cat_url)
    await ctx.send(embed=embed)

@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} был разбанен")
            return

client.run(TOKEN)


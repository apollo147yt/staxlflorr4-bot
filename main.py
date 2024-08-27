import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

credits = {}
sacrifice_active = False
sacrifice_multiplier = 1.0

rarities = [
    {"name": "Common", "reward": 10, "color": 0xFFFFFF},
    {"name": "Uncommon", "reward": 25, "color": 0x1EFF00},
    {"name": "Rare", "reward": 50, "color": 0x0070DD},
    {"name": "Epic", "reward": 100, "color": 0xA335EE},
    {"name": "Legendary", "reward": 250, "color": 0xFF8000},
    {"name": "Mythic", "reward": 500, "color": 0xFF69B4},
    {"name": "Ultra", "reward": 1000, "color": 0xFF4500},
    {"name": "Super", "reward": 2500, "color": 0xFFD700},
    {"name": "Omega", "reward": 5000, "color": 0x555555},
    {"name": "Fabled", "reward": 10000, "color": 0xFFA500},
    {"name": "Divine", "reward": 25000, "color": 0x800080},
    {"name": "Supreme", "reward": 50000, "color": 0xFFB6C1},
    {"name": "Omnipotent", "reward": 100000, "color": 0x808080},
    {"name": "Astral", "reward": 250000, "color": 0x006400},
    {"name": "Celestial", "reward": 1000000, "color": 0x00FFFF},
]

def determine_rarity():
    rng = random.random()
    rarity = 0
    if rng < 0.55:
        rarity += 1
    if rng < 0.35:
        rarity += 1
    if rng < 0.2:
        rarity += 1
    if rng < 0.1:
        rarity += 1
    if rng < 0.05:
        rarity += 1
    if rng < 0.02:
        rarity += 1
    if rng < 0.01:
        rarity += 1
    if rng < 0.005:
        rarity += 1
    if rng < 0.0025:
        rarity += 1
    if rng < 0.001:
        rarity += 1
    if rng < 0.00044:
        rarity += 1
    if rng < 0.00014:
        rarity += 1
    if rng < 0.00004:
        rarity += 1
    if rng < 0.00001:
        rarity += 1
    if rng < 0.000004:
        rarity += 1
    if rng < 0.000001:
        rarity += 1
    if rng < 0.0000004:
        rarity += 1
    if rng < 0.0000001:
        rarity += 1
    if rng < 0.00000004:
        rarity += 1
    if rng < 0.00000001:
        rarity += 1
    if rng == 0:
        rarity += 1
    return rarity

@bot.event
async def on_ready():
        global credits
        credits = {}
        print(f'Logged in as {bot.user}')

@bot.command()
async def spin(ctx):
    global credits
    if not isinstance(credits, dict):
        credits = {}
    global sacrifice_multiplier
    rarity_index = determine_rarity()
    if rarity_index >= len(rarities):
        rarity_index = len(rarities) - 1
    rarity = rarities[rarity_index]
    reward = int(rarity["reward"] * sacrifice_multiplier)
    user_id = str(ctx.author.id)
    credits[user_id] = credits.get(user_id, 0) + reward
    embed = discord.Embed(title="Spin Result", color=rarity["color"])
    embed.add_field(name="Rarity", value=rarity["name"], inline=False)
    embed.add_field(name="Reward", value=f"{reward} credits", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def sac(ctx, amount: int):
    global sacrifice_active, sacrifice_multiplier
    user_id = str(ctx.author.id)
    if user_id not in credits or credits[user_id] < amount:
        await ctx.send("You don't have enough credits to sacrifice.")
        return
    if not isinstance(credits, dict):
        credits = {}
    credits[user_id] -= amount
    sacrifice_multiplier += amount / 10000
    sacrifice_active = True
    await ctx.send(f"Sacrifice accepted! Your current luck multiplier is now {sacrifice_multiplier}x.")

@bot.command()
async def setcredits(ctx, member: discord.Member, amount: int):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("You don't have permission to use this command.")
        return
    user_id = str(member.id)
    credits[user_id] = amount
    await ctx.send(f"{member.display_name}'s credits have been set to {amount}.")

@bot.command()
async def addcredits(ctx, member: discord.Member, amount: int):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("You don't have permission to use this command.")
        return
    user_id = str(member.id)
    credits[user_id] = credits.get(user_id, 0) + amount
    await ctx.send(f"{amount} credits have been added to {member.display_name}'s balance.")

@bot.command()
async def pay(ctx, member: discord.Member, amount: int):
    user_id = str(ctx.author.id)
    target_id = str(member.id)
    if user_id not in credits or credits[user_id] < amount:
        await ctx.send("You don't have enough credits to make this payment.")
        return
    credits[user_id] -= amount
    credits[target_id] = credits.get(target_id, 0) + amount
    await ctx.send(f"You have paid {amount} credits to {member.mention}.")

@bot.command()
async def credits(ctx, member: discord.Member = None):
    user_id = str(ctx.author.id) if member is None else str(member.id)
    credit_amount = credits.get(user_id, 0)
    await ctx.send(f"{ctx.author.display_name if member is None else member.display_name} has {credit_amount} credits.")

@bot.command()
async def assign_role(ctx, role: discord.Role):
    if not ctx.author.id == ctx.guild.owner_id:
        await ctx.send("You don't have permission to use this command.")
        return
    await ctx.author.add_roles(role)
    await ctx.send(f"The role {role.name} has been assigned to you.")

@bot.command()
async def remove_role(ctx, role: discord.Role):
    if not ctx.author.id == ctx.guild.owner_id:
        await ctx.send("You don't have permission to use this command.")
        return
    await ctx.author.remove_roles(role)
    await ctx.send(f"The role {role.name} has been removed from you.")

@bot.command()
async def endsac(ctx):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("You don't have permission to use this command.")
        return
    global sacrifice_active, sacrifice_multiplier
    sacrifice_active = False
    sacrifice_multiplier = 1.0
    await ctx.send("Sacrifice session has ended. Luck multiplier reset.")

@bot.command()
async def help1(ctx):
    embed = discord.Embed(title="Bot Commands", color=0x00ff00)
    embed.add_field(name="!spin", value="Spin to earn rewards based on rarity.", inline=False)
    embed.add_field(name="!sac", value="Sacrifice credits to increase your luck.", inline=False)
    embed.add_field(name="!setcredits [user] [amount]", value="Set a user's credits to a specific amount. (Admin only)", inline=False)
    embed.add_field(name="!addcredits [user] [amount]", value="Add a specific amount of credits to a user's balance. (Admin only)", inline=False)
    embed.add_field(name="!pay [user] [amount]", value="Pay another user a specific amount of credits.", inline=False)
    embed.add_field(name="!credits [user (optional)]", value="Check your or another user's credit balance.", inline=False)
    embed.add_field(name="!assign_role [role]", value="Assign a specific role to yourself. (Owner only)", inline=False)
    embed.add_field(name="!remove_role [role]", value="Remove a specific role from yourself. (Owner only)", inline=False)
    embed.add_field(name="!endsac", value="End the current sacrifice session. (Admin only)", inline=False)
    await ctx.send(embed=embed)

bot.run('MTI0MDQ2MDA2MzY2NDI0NjkxNQ.GqsJZA.-IwgY3lkI5QWcWhkcTvTBGESKuPLIQRCUZgFw8')

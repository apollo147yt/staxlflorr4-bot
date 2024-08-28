import discord
from discord.ext import commands
import random
import json
import os

# Default data structure
default_db = {
    "Social_credits": {},
    "luck_boost": {},
    "sac_active": False,
    "sac_amount": 0,
    "sac_spins": 0,
    "spins_count": {},
    "sac_spins_limit": 10,
    "custom_luck_multiplier": 1
}

# Check if the file exists
if not os.path.exists("db.json"):
    with open("db.json", "w") as f:
        json.dump(default_db, f, indent=4)

# Load the file
with open("db.json", "r") as f:
    db = json.load(f)

# Function to save the database
def save_db():
    with open("db.json", "w") as f:
        json.dump(db, f, indent=4)

# Ensure user data exists
def ensure_user_data(user_id):
    user_id_str = str(user_id)
    if user_id_str not in db["Social_credits"]:
        db["Social_credits"][user_id_str] = 0
    if user_id_str not in db["spins_count"]:
        db["spins_count"][user_id_str] = 0

# Get user credits
def get_user_credits(user_id):
    return db["Social_credits"].get(str(user_id), 0)

# Set user credits
def set_user_credits(user_id, credits):
    db["Social_credits"][str(user_id)] = credits

# Setting up bot with command prefix and intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Rarity names, credits, and colors
rarityNames = [
    'Common', 'Uncommon', 'Rare', 'Epic', 'Legendary', 'Mythic', 'Ultra', 'Super', 'Omega', 
    'Fabled', 'Divine', 'Supreme', 'Omnipotent', 'Astral', 'Celestial', 'Seraphic', 'Transcendent', 
    'Quantum', 'Galactic', 'Eternal', 'cHa0s', 'Quantum Shard'
]
rarityCredits = [
    -5, 1, 2, 5, 10, 25, 100, 250, 1000, 2500, 10000, 25000, 100000, 250000, 1000000, 2500000, 
    10000000, 25000000, 100000000, 250000000, 1000000000, 10**20
]
rarityColors = {
    'Common': 0x66cdaa,
    'Uncommon': 0xf0e68c,
    'Rare': 0xadd8e6,
    'Epic': 0xd8bfd8,
    'Legendary': 0xcc0000,
    'Mythic': 0x00008b,
    'Ultra': 0xffb6c1,
    'Super': 0x32cd32,
    'Omega': 0x404040,
    'Fabled': 0xff8c00,
    'Divine': 0x4b0082,
    'Supreme': 0xff1493,
    'Omnipotent': 0x808080,
    'Astral': 0x004d00,
    'Celestial': 0x87cefa,
    'Seraphic': 0xff69b4,
    'Transcendent': 0xffffff,
    'Quantum': 0x000000,
    'Galactic': 0xa64d79,
    'Eternal': 0x13426d,
    'cHa0s': 0x4c1130
}

# Mob types and multipliers
mobType = [
    'Ladybug', 'Bee', 'Hornet', 'Spider', 'Baby Ant', 'Worker Ant', 'Soldier Ant', 'Queen Ant', 
    'Ant Hole', 'Dandelion', 'Rock', 'Centipede', 'Evil Centipede', 'Dark Ladybug', 'Beetle', 
    'Scorpion', 'Cactus', 'Sandstorm', 'Fire Ant Burrow', 'Fire Ant', 'Fire Queen Ant', 'Desert Centipede', 
    'Locust', 'Desert Moth', 'Shiny Ladybug', 'Crab', 'Jellyfish', 'Shell', 'Starfish', 'Sponge', 
    'Leech', 'Sea Urchin', 'Bubble', 'Plastic', 'Square', 'Pentagon', 'Hexagon'
]
mobMulti = [
    1, 1.5, 1, 1, 1, 1, 1, 1.5, 1, 1.5, 1, 1, -1, -2, 1, 1, 1, 1.5, 2, 1, 1.5, 1.5, 1, 1.5, 5, 
    1, 1, 1.5, 1, 1, 1, 1.5, 1, 3, 10, 1000, -666
]

# Event when bot is ready
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def spin(ctx):
    if ctx.channel.name != 'spin':
        await ctx.send("This command can only be used in the #spin channel.")
        return

    try:
        user_id = ctx.author.id
        ensure_user_data(user_id)

        # Set default luck multiplier to 1
        luck_multiplier = db.get("custom_luck_multiplier", 1)

        # Apply sacrifice luck boost if active
        if db.get("sac_active", False):
            sac_amount = db.get("sac_amount", 0)
            luck_multiplier = round(max(0.207125 * (2.34915 * sac_amount + 463.458) ** 0.5 - 4.48083, 1), 1)

        randomValue = random.random()
        rng = randomValue / (((luck_multiplier - 1) * 0.7) + 1)

        # Determine rarity based on the adjusted RNG
        thresholds = [0.55, 0.35, 0.2, 0.1, 0.05, 0.02, 0.01, 0.005, 0.0025, 0.001, 0.00044, 0.00014, 0.00004, 0.00001, 0]
        rarity = next((i for i, threshold in enumerate(thresholds) if rng < threshold), len(thresholds) - 1)

        # Determine mob type and multiplier
        mob_index = random.randint(0, len(mobType) - 1)
        mob_name = mobType[mob_index]
        mob_multiplier = mobMulti[mob_index]

        final_credits = rarityCredits[rarity] * mob_multiplier

        current_credits = get_user_credits(user_id)
        new_credits = current_credits + final_credits
        set_user_credits(user_id, new_credits)

        # Get the color for the rarity
        raritycolor = rarityColors[rarityNames[rarity]]

        embed = discord.Embed(color=raritycolor)
        embed.add_field(name=f"{rarityNames[rarity]} {mob_name}", value=f"You got a {rarityNames[rarity]} {mob_name}!", inline=False)
        if float(luck_multiplier) > 1:
            embed.add_field(name="Frenzy!", value=f"{luck_multiplier}x luck from a sacrifice", inline=False)
        embed.add_field(name="Rare Mob Multiplier!", value=f"x{mob_multiplier}", inline=False)
        embed.add_field(name=f"+{final_credits} CREDITS", value=f"{rarityCredits[rarity]} ({rarityNames[rarity]}) x{mob_multiplier} ({mob_name})", inline=False)

        if db.get("sac_active", False):
            sac_spins = db.get("sac_spins", 0)
            if sac_spins >= db.get("sac_spins_limit", 10):
                if not db.get("sac_limit_reached", False):
                    await ctx.send("Sacrifice spins limit reached.")
                    db["sac_limit_reached"] = True
                    # Reset luck boost and other sacrifice-related values
                    db["custom_luck_multiplier"] = 1
                    db["sac_amount"] = 0
                    db["sac_active"] = False
                    db["sac_spins"] = 0
                # Send the result embed even if the limit is reached
                await ctx.send(embed=embed)
            else:
                db["sac_spins"] += 1
                await ctx.send(embed=embed)
        else:
            await ctx.send(embed=embed)
            db["spins_count"][str(user_id)] += 1

        save_db()

    except Exception as e:
        print(f"Error in !spin command: {e}")
        await ctx.send("My goofy ass did an oopsy, ping a bot coder to fix it.")

@bot.command()
async def sac(ctx, amount: int):
    try:
        user_id = ctx.author.id
        ensure_user_data(user_id)
        
        current_credits = get_user_credits(user_id)
        new_credits = (current_credits) - (amount)
        if amount > current_credits:
            await ctx.send("Nuh uh try again")
            return
        
        new_credits = current_credits - amount
        set_user_credits(user_id, new_credits)

        db["sac_active"] = True
        db["sac_amount"] = amount
        db["sac_spins"] = 0
        db["sac_limit_reached"] = False

        # Calculate luck multiplier
        luck_multiplier = round(max(0.207125 * (2.34915 * amount + 463.458) ** 0.5 - 4.48083, 1), 1)
        
        embed = discord.Embed(color=0xFFFF00)
        embed.add_field(name="The Flowr gods heed your sacrifice...", value="\u200b", inline=False)
        embed.add_field(name=f"A {luck_multiplier}x luck boost has been activated!", value="\u200b", inline=False)
        embed.add_field(name="Sacrificed Social Credit", value=f"{amount}", inline=False)
        embed.add_field(name="Successful Sacrifice", value=f"{ctx.author.mention} sacrificed {amount} credits!", inline=False)

        await ctx.send(embed=embed)

        save_db()
    
    except Exception as e:
        print(f"Error in !sac command: {e}")
        await ctx.send("My goofy ass did an oopsy, ping a bot coder to fix it.")

@bot.command()
async def endsac(ctx):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("You need to be an admin to use this command.")
        return

    if not db.get("sac_active", False):
        await ctx.send("No active sacrifice.")
        return

    db["sac_active"] = False
    db["sac_amount"] = 0
    db["sac_spins"] = 0
    db["sac_limit_reached"] = False
    await ctx.send("Sacrifice ended.")

    save_db()

@bot.command()
async def setcredits(ctx, user: discord.User, amount: int):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("You need to be an admin to use this command.")
        return

    set_user_credits(user.id, amount)
    await ctx.send(f"Set {user.name}'s credits to {amount}.")

    save_db()

@bot.command()
async def addcredits(ctx, user: discord.User, amount: int):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("You need to be an admin to use this command.")
        return

    current_credits = get_user_credits(user.id)
    new_credits = current_credits + amount
    set_user_credits(user.id, new_credits)
    await ctx.send(f"Added {amount} credits to {user.name}.")

    save_db()

@bot.command()
async def removecredits(ctx, user: discord.User, amount: int):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("You need to be an admin to use this command.")
        return

    current_credits = get_user_credits(user.id)
    new_credits = max(current_credits - amount, 0)
    set_user_credits(user.id, new_credits)
    await ctx.send(f"Removed {amount} credits from {user.name}.")

    save_db()

@bot.command()
async def pay(ctx, user: discord.User, amount: int):
    try:
        sender_id = ctx.author.id
        recipient_id = user.id

        if amount <= 0:
            await ctx.send("Amount must be greater than 0.")
            return

        ensure_user_data(sender_id)
        ensure_user_data(recipient_id)

        sender_credits = get_user_credits(sender_id)
        if sender_credits < amount:
            await ctx.send("You don't have enough credits to make this payment.")
            return

        set_user_credits(sender_id, sender_credits - amount)
        set_user_credits(recipient_id, get_user_credits(recipient_id) + amount)

        embed = discord.Embed(color=0xFFFF00)
        embed.add_field(name=f"Success!", value=f"{ctx.author.mention} has given {user.mention} {amount} credits!", inline=False)
        await ctx.send(embed=embed)

        save_db()

    except Exception as e:
        print(f"Error in !pay command: {e}")
        await ctx.send("My goofy ass did an oopsy, ping a bot coder to fix it.")

@bot.command()
async def assign_role(ctx, user: discord.User, *, role: discord.Role):
    if ctx.author.id != bot.owner_id:
        await ctx.send("Only the bot owner can use this command.")
        return

    await user.add_roles(role)
    await ctx.send(f"Assigned {role.name} to {user.name}.")

@bot.command()
async def remove_role(ctx, user: discord.User, *, role: discord.Role):
    if ctx.author.id != bot.owner_id:
        await ctx.send("Only the bot owner can use this command.")
        return

    await user.remove_roles(role)
    await ctx.send(f"Removed {role.name} from {user.name}.")

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

@bot.command()
async def rig(ctx, rarity: int):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("You need to be an admin to use this command.")
        return

    if rarity < 1 or rarity >= len(rarityNames):
        await ctx.send("Invalid rarity number.")
        return

    # Simulate rigged spin with the given rarity
    user_id = ctx.author.id
    ensure_user_data(user_id)

    final_credits = rarityCredits[rarity - 1]  # Indexing starts from 0
    mob_index = random.randint(0, len(mobType) - 1)
    mob_name = mobType[mob_index]
    mob_multiplier = mobMulti[mob_index]

    current_credits = get_user_credits(user_id)
    new_credits = current_credits + final_credits
    set_user_credits(user_id, new_credits)

    raritycolor = rarityColors[rarityNames[rarity]] 

    embed = discord.Embed(color=raritycolor)
    embed.add_field(name=f"{rarityNames[rarity]} {mob_name}", value=f"You got a {rarityNames[rarity]} {mob_name}!", inline=False)
    embed.add_field(name="Rare Mob Multiplier!", value=f"x{mob_multiplier}", inline=False)
    embed.add_field(name=f"+{final_credits} CREDITS", value=f"{rarityCredits[rarity]} ({rarityNames[rarity]}) x{mob_multiplier} ({mob_name})", inline=False)
    embed.add_field(name="RIGGED!", value="The luck is rel! (Trust)", inline=False)
    ctx.send(embed=embed)

    save_db()

# Start the bot with your token
bot.run('your-bot-token')

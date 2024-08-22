import discord
from discord.ext import commands
from replit import db
import random
from keep_alive import keep_alive

# Initialize the database
def init_db():
    if "Social_credits" not in db or not isinstance(db["Social_credits"], dict):
        db["Social_credits"] = {}
    if "luck_boost" not in db or not isinstance(db["luck_boost"], dict):
        db["luck_boost"] = {}
    if "sac_active" not in db:
        db["sac_active"] = False
    if "sac_amount" not in db:
        db["sac_amount"] = 0
    if "sac_spins" not in db:
        db["sac_spins"] = 0
    if "spins_count" not in db:
        db["spins_count"] = {}
    if "sac_spins_limit" not in db:
        db["sac_spins_limit"] = 20
    if "custom_luck_multiplier" not in db:
        db["custom_luck_multiplier"] = 1

init_db()

# Setting up bot with command prefix and intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Rarity names, credits, and colors
rarityNames = ['Common', 'Uncommon', 'Rare', 'Epic', 'Legendary', 'Mythic', 'Ultra', 'Super', 'Omega', 'Fabled', 'Divine', 'Supreme', 'Omnipotent', 'Astral', 'Celestial', 'Seraphic', 'Transcendent', 'Quantum', 'Galactic', 'Eternal', 'cHa0s', 'Quantum Shard']
rarityCredits = [-5, 1, 2, 5, 10, 25, 100, 250, 1000, 2500, 10000, 25000, 100000, 250000, 1000000, 2500000, 10000000, 25000000, 100000000, 250000000, 1000000000, 10**20]
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
mobType = ['Ladybug', 'Bee', 'Hornet', 'Spider', 'Baby Ant', 'Worker Ant', 'Soldier Ant', 'Queen Ant', 'Ant Hole', 'Dandelion', 'Rock', 'Centipede', 'Evil Centipede', 'Dark Ladybug', 'Beetle', 'Scorpion', 'Cactus', 'Sandstorm', 'Fire Ant Burrow', 'Fire Ant', 'Fire Queen Ant', 'Desert Centipede', 'Locust', 'Desert Moth', 'Shiny Ladybug', 'Crab', 'Jellyfish', 'Shell', 'Starfish', 'Sponge', 'Leech', 'Sea Urchin', 'Bubble', 'Plastic', 'Square', 'Pentagon']
mobMulti = [1, 1.5, 1, 1, 1, 1, 1, 1.5, 1, 1, 1, 1.5, 2, 1, 1, 1, 1.5, 1, 1, 2, 1.5, 1, 1, 5, 1, 1, 1.5, 1, 1, 1, 1, 1, 3, 10, 1000]

# Event when bot is ready
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# Ensure user data exists
def ensure_user_data(user_id):
    if str(user_id) not in db["Social_credits"]:
        db["Social_credits"][str(user_id)] = 0
    if str(user_id) not in db["spins_count"]:
        db["spins_count"][str(user_id)] = 0

# Get user credits
def get_user_credits(user_id):
    return db["Social_credits"].get(str(user_id), 0)

# Set user credits
def set_user_credits(user_id, credits):
    db["Social_credits"][str(user_id)] = credits

# Spin command
@bot.command()
async def spin(ctx):
    if ctx.channel.name != 'spin':
        await ctx.send("This command can only be used in the #spin channel.")
        return

    try:
        user_id = ctx.author.id
        ensure_user_data(user_id)

        # Initialize variables
        sac_amount = db.get("sac_amount", 0)
        luck_multiplier = db.get("custom_luck_multiplier", 1)  # Use custom multiplier if set

        # Calculate luck multiplier if a sacrifice is active
        if db.get("sac_active", False):
            luck_multiplier = max(0.207125 * (2.34915 * sac_amount + 463.458) ** 0.5 - 4.48083, 1)
            print(f"Luck multiplier from sacrifice: {luck_multiplier}")

        # Randomly determine rarity
        rng = random.random() / (((luck_multiplier - 1) * 0.7) + 1)
        rarity = 0

        thresholds = [0.55, 0.35, 0.2, 0.1, 0.05, 0.02, 0.01, 0.005, 0.0025, 0.001, 0.00044, 0.00014, 0.00004, 0.00001, 0.000004, 0.000001, 0.0000004, 0.0000001, 0.00000004, 0.00000001, 0.000000004]
        for threshold in thresholds:
            if rng < threshold:
                rarity += 1
            else:
                break

        # Handle overflow if the rarity is beyond the range
        rarity = min(rarity, len(rarityNames) - 1)

        # Select the corresponding rarity name and credits
        rarity_name = rarityNames[rarity]
        rarity_credit = rarityCredits[rarity]
        rarity_color = rarityColors.get(rarity_name, 0x808080)  # Default to gray if rarity not found

        # Randomly select a mob
        mob_index = random.randint(0, len(mobType) - 1)
        mob_name = mobType[mob_index]
        mob_multiplier = mobMulti[mob_index]

        # Calculate final credits
        final_credits = rarity_credit * mob_multiplier

        # Update user credits
        current_credits = get_user_credits(user_id)
        new_credits = current_credits + final_credits
        set_user_credits(user_id, new_credits)

        # Check if the spin limit for the sacrifice has been reached
        if db.get("sac_active", False) and db["sac_spins"] >= db.get("sac_spins_limit", 20):
            db["sac_active"] = False
            db["sac_amount"] = 0
            db["sac_spins"] = 0
            db["sac_user"] = None
            await ctx.send("Sacrifice period has ended. Spinning now returns to normal.")

        # Create and send embed message
        embed = discord.Embed(title=f"{rarity_name} {mob_name}", color=rarity_color)
        embed.add_field(name=f"You got a {rarity_name} {mob_name}", value="\u200b", inline=False)

        # Add the luck boost field if a sacrifice is active
        if db.get("sac_active", False):
            sac_user = ctx.author.display_name  # Added to match your existing format
            embed.add_field(name="Frenzy!", value=f"{luck_multiplier:.2f}x luck from {sac_user}'s sacrifice!", inline=False)

        # Add the mob multiplier field only if it's greater than 1
        if mob_multiplier > 1:
            embed.add_field(name="Rare mob multiplier!", value=f"x{mob_multiplier}", inline=False)

        # Add credits field
        embed.add_field(name=f"+{final_credits} SOCIAL CREDITS", value=f"Total credits: {new_credits}", inline=False)
        embed.set_footer(text=f"Current Sacrificed Credits: {sac_amount}\n{db.get('sac_spins_limit', 20) - db.get('sac_spins', 0)} spins left with increased luck!")

        await ctx.send(embed=embed)

        # Increment the spin count and sacrifice spin count if active
        db["spins_count"][str(user_id)] += 1

        if db.get("sac_active", False):
            db["sac_spins"] += 1

    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

# Credit command
@bot.command()
async def credit(ctx):
    user_id = ctx.author.id
    ensure_user_data(user_id)
    current_credits = get_user_credits(user_id)
    await ctx.send(f"You have {current_credits} social credits.")

# Sacrifice command
@bot.command()
async def sac(ctx, amount: int):
    user_id = ctx.author.id
    ensure_user_data(user_id)

    current_credits = get_user_credits(user_id)
    if current_credits < amount:
        await ctx.send("You don't have enough credits to sacrifice!")
        return

    db["Social_credits"][str(user_id)] -= amount
    db["sac_active"] = True
    db["sac_amount"] += amount
    db["sac_spins"] = 0
    db["sac_user"] = ctx.author.display_name

    sac_message = f"{ctx.author.display_name} has sacrificed {amount} social credits to the bot. Luck has been increased for the next {db.get('sac_spins_limit', 20)} spins!"
    await ctx.send(sac_message)

# Set credits command (admin only)
@bot.command()
@commands.has_permissions(administrator=True)
async def setcredits(ctx, user: discord.User, amount: int):
    user_id = user.id
    ensure_user_data(user_id)
    set_user_credits(user_id, amount)
    await ctx.send(f"Set {user.display_name}'s social credits to {amount}.")

# Add credits command (admin only)
@bot.command()
@commands.has_permissions(administrator=True)
async def addcredits(ctx, user: discord.User, amount: int):
    user_id = user.id
    ensure_user_data(user_id)
    current_credits = get_user_credits(user_id)
    new_credits = current_credits + amount
    set_user_credits(user_id, new_credits)
    await ctx.send(f"Added {amount} social credits to {user.display_name}. They now have {new_credits} credits.")

# Ends the current sacrifice (admin only)
@bot.command()
@commands.has_permissions(administrator=True)
async def endsac(ctx):
    if not db.get("sac_active", False):
        await ctx.send("There is no active sacrifice.")
        return

    db["sac_active"] = False
    db["sac_amount"] = 0
    db["sac_spins"] = 0
    db["sac_user"] = None
    await ctx.send("The sacrifice has been ended by an admin.")

# Pay command to transfer credits between users
@bot.command()
async def pay(ctx, user: discord.User, amount: int):
    payer_id = ctx.author.id
    receiver_id = user.id

    ensure_user_data(payer_id)
    ensure_user_data(receiver_id)

    payer_credits = get_user_credits(payer_id)

    if payer_credits < amount:
        await ctx.send("You don't have enough credits to complete this transaction.")
        return

    # Update credits for both users
    db["Social_credits"][str(payer_id)] = payer_credits - amount
    db["Social_credits"][str(receiver_id)] += amount

    await ctx.send(f"{ctx.author.display_name} has paid {user.display_name} {amount} social credits.")

# Role assignment command (owner only)
@bot.command()
@commands.is_owner()
async def assign_role(ctx, user: discord.User, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f"{user.display_name} has been given the {role.name} role.")

# Role removal command (owner only)
@bot.command()
@commands.is_owner()
async def remove_role(ctx, user: discord.User, role: discord.Role):
    await user.remove_roles(role)
    await ctx.send(f"{user.display_name} has had the {role.name} role removed.")

# Help command with detailed information
@bot.command()
async def help1(ctx):
    embed = discord.Embed(title="Help", description="List of available commands", color=0x00ff00)
    commands_list = {
        "!spin": "Spin the wheel to earn credits.",
        "!credit": "Check your current social credit balance.",
        "!sac [amount]": "Sacrifice a specified amount of credits to increase luck for everyone for a limited number of spins.",
        "!pay [user] [amount]": "Pay another user a specified amount of social credits.",
        "!setcredits [user] [amount] (admin only)": "Set a user's social credit balance.",
        "!addcredits [user] [amount] (admin only)": "Add a specified amount of social credits to a user's balance.",
        "!endsac (admin only)": "Ends the current sacrifice.",
        "!assign_role [user] [role] (owner only)": "Assign a role to a user.",
        "!remove_role [user] [role] (owner only)": "Remove a role from a user."
    }
    for cmd, desc in commands_list.items():
        embed.add_field(name=cmd, value=desc, inline=False)
    await ctx.send(embed=embed)

# Run the bot with the specified token
keep_alive()
bot.run('MTI0MDQ2MDA2MzY2NDI0NjkxNQ.GqsJZA.-IwgY3lkI5QWcWhkcTvTBGESKuPLIQRCUZgFw8')

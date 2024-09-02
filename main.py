import asyncio
import discord
from discord.ext import commands
import random
import json
import os
from datetime import timedelta
import re

# Default data structure
default_db = {
    "Social_credits": {},
    "luck_boost": {},
    "sac_active": False,
    "sac_amount": 0,
    "sac_spins": 0,
    "spins_count": {},  
    "sac_spins_limit": 10,
    "custom_luck_multiplier": 1,
    "market": {},
    "giveaway_data": {}
}

# Ensure the database file exists
if not os.path.exists("db.json"):
    with open("db.json", "w") as f:
        json.dump(default_db, f, indent=4)

# Load the database file
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

# Initialize bot with command prefix and intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
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
    'Common': 0x7eef6d,
    'Uncommon': 0xffe65d,
    'Rare': 0x4d52e3,
    'Epic': 0x861fde,
    'Legendary': 0xde1f1f,
    'Mythic': 0x1fdbde,
    'Ultra': 0xff2b75,
    'Super': 0x2bffa3,
    'Omega': 0x494849,
    'Fabled': 0xff5500,
    'Divine': 0x67549c,
    'Supreme': 0xb25dd9,
    'Omnipotent': 0x888888,
    'Astral': 0x046307,
    'Celestial': 0x00bfff,
    'Seraphic': 0xc77e5b,
    'Transcendent': 0xffffff,
    'Quantum': 0x61ffdd,
    'Galactic': 0xba5f7a,
    'Eternal': 0x5a8c7d,
    'cHa0s': 0x20258a
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
    1, 1, 1.5, 1, 1, 1, 1.5, 1, 3, 10, 100, -666
]

# Event when bot is ready
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def spin(ctx):
    if not ctx.author.guild_permissions.administrator:
        if ctx.channel.name != 'spin':
            await ctx.send("This command can only be used in the #spin channel.")
            return

    try:
        user_id = ctx.author.id
        ensure_user_data(user_id)

        luck_multiplier = db.get("custom_luck_multiplier", 1)
        if db.get("sac_active", False):
            sac_amount = db.get("sac_amount", 0)
            luck_multiplier = round(max(0.207125 * (2.34915 * sac_amount + 463.458) ** 0.5 - 4.48083, 1), 1)

        random_value = random.random()
        rng = random_value / (((luck_multiplier - 1) * 0.7) + 1)

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

        biased_mob_index = random.random()
        hexagon_threshold = 0.001
        pentagon_threshold = 0.005

        if biased_mob_index < hexagon_threshold:
            mob_index = mobType.index('Hexagon')
        elif biased_mob_index < pentagon_threshold:
            mob_index = mobType.index('Pentagon')
        else:
            mob_index = random.choice([i for i in range(len(mobType)) if mobType[i] not in ['Hexagon', 'Pentagon']])

        mob_name = mobType[mob_index]
        mob_multiplier = mobMulti[mob_index]
        final_credits = round(rarityCredits[rarity] * mob_multiplier)

        integer = "+" if final_credits > 0 else ""
        emoji_decide = "<:ohyes:1277612067276329052>" if final_credits > 0 else "<:ohno:1277611594401972247>"

        rarity_emoji = ""
        rarity_emoji_mapping = {
            0: "<:Common:1280053956118052875>",
            1: "<:Uncommon:1280054000586067998>",
            2: "<:Rare:1280054036913197097>",
            3: "<:Epic:1280054128126590986>",
            4: "<:Legendary:1280054164168376395>",
            5: "<:Mythic:1280054213879271581>",
            6: "<:Ultra:1280054248696188950>",
            7: "<:Super:1280054279696154737>",
            8: "<:Omega:1280054308792045609>",
            9: "<:Fabled:1280054339448209484>",
            10: "<:Divine:1280054383207252049>",
            11: "<:Supreme:1280054423741272167>",
            12: "<:Omnipotent:1280061314177437761>",
            13: "<:Astral:1280061338801934368>",
            14: "<:Celestial:1280061360532619329>",
            15: "<:Seraphic:1280061390803042415>",
            16: "<:Transcendant:1280061411879424001>",
            17: "<:Quantum:1280061433144414218>",
            18: "<:Galactic:1280061456099971133>",
            19: "<:Eternal:1280061481156608020>"
        }
        rarity_emoji = rarity_emoji_mapping.get(rarity, "")

        current_credits = get_user_credits(user_id)
        new_credits = current_credits + final_credits
        set_user_credits(user_id, new_credits)

        raritycolor = rarityColors[rarityNames[rarity]]

        embed = discord.Embed(color=raritycolor)
        embed.add_field(name=f"{rarityNames[rarity]} {mob_name}", value=f"You got a {rarityNames[rarity]} {mob_name}!", inline=False)
        if float(luck_multiplier) > 1:
            embed.add_field(name="Frenzy!", value=f"{luck_multiplier}x luck from a sacrifice", inline=False)
        embed.add_field(name="Rare Mob Multiplier!", value=f"x{mob_multiplier}", inline=False)
        embed.add_field(name=f"{integer}{final_credits} CREDITS {emoji_decide}", value=f"{rarityCredits[rarity]} ({rarityNames[rarity]}) {rarity_emoji} x{mob_multiplier} ({mob_name})", inline=False)

        if db.get("sac_active", False):
            sac_spins = db.get("sac_spins", 0)
            if sac_spins >= db.get("sac_spins_limit", 10):
                if not db.get("sac_limit_reached", False):
                    await ctx.send("Sacrifice spins limit reached.")
                    db["sac_limit_reached"] = True
                    db["custom_luck_multiplier"] = 1
                    db["sac_amount"] = 0
                    db["sac_active"] = False
                    db["sac_spins"] = 0
                await ctx.reply(embed=embed, mention_author=True)
            else:
                db["sac_spins"] += 1
                await ctx.reply(embed=embed, mention_author=True)
        else:
            await ctx.reply(embed=embed, mention_author=True)
            db["spins_count"][str(user_id)] += 1

        save_db()

    except Exception as e:
        await ctx.send(f"my goofy ass did this wrong: {e}. Ping a bot coder to fix it")

class MarketAddModal(discord.ui.Modal):
    def __init__(self, user_id):
        super().__init__(title="Add Market Item")
        self.user_id = user_id
        self.add_item(discord.ui.TextInput(label="Name of Service", placeholder="Enter the name of the service", custom_id="name_input", required=True))
        self.add_item(discord.ui.TextInput(label="Description of Service", placeholder="Enter a description", custom_id="description_input", required=True))
        self.add_item(discord.ui.TextInput(label="Price of Service (min 10k)", placeholder="Enter the price", custom_id="price_input", required=True))

    async def on_submit(self, interaction: discord.Interaction):
        name = self.children[0].value
        description = self.children[1].value
        price_str = self.children[2].value

        try:
            price = int(price_str)
            if price < 10000:
                await interaction.response.send_message("Price must be at least 10,000 credits.", ephemeral=True)
                return
        except ValueError:
            await interaction.response.send_message("Invalid price format. Please enter a valid integer.", ephemeral=True)
            return
        
        try:
            if "market" not in db:
                db["market"] = {}
            item_id = len(db["market"]) + 1
            db["market"][str(item_id)] = {
                "owner": str(self.user_id),
                "name": name,
                "description": description,
                "price": price
            }

            # Deducting the 10k credits
            ensure_user_data(self.user_id)
            current_credits = get_user_credits(self.user_id)
            new_credits = current_credits - 10000
            set_user_credits(self.user_id, new_credits)

            save_db()
            await interaction.response.send_message(f"Market item '{name}' added successfully.", ephemeral=True)
        except Exception as e:
            print(f"An error occurred: {e}")
            await interaction.response.send_message("Why the fu- ping a bot coder to fix this", ephemeral=True)

# MarketAddButton class
class MarketAddButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Create!", style=discord.ButtonStyle.blurple)

    async def callback(self, interaction: discord.Interaction):
        modal = MarketAddModal(interaction.user.id)
        await interaction.response.send_modal(modal)

# Add Market Command
@bot.command()
async def addmarket(ctx):
    view = discord.ui.View()
    view.add_item(MarketAddButton())
    await ctx.send("Click the button below to add a market item (note there is a 10k fee).", view=view)

@bot.command()
async def market(ctx, page: int = 1):
    items_per_page = 5
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    
    market_items = list(db["market"].items())[start_index:end_index]
    if not market_items:
        await ctx.send("No items found on this page.")
        return
    
    embed = discord.Embed(title=f"Market - Page {page}", color=0x00ff00)
    for item_id, item in market_items:
        embed.add_field(
            name=f"{item['name']} (ID: {item_id})",
            value=f"**Description:** {item['description']}\n**Price:** {item['price']} credits\n**Owner:** <@{item['owner']}>",
            inline=False
        )
    
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def delmarket(ctx, item_id: int):
    item_id_str = str(item_id)
    
    # Check if the item exists
    item = db["market"].get(item_id_str)
    if not item:
        await ctx.send("Item not found.")
        return

    # If the user is not an admin, check if they are the owner of the item
    if not ctx.author.guild_permissions.administrator and item["owner"] != str(ctx.author.id):
        await ctx.send("You are not the owner of this item.")
        return

    # Try to delete the item and save the database
    try:
        del db["market"][item_id_str]
        save_db()
        await ctx.send(f"Market item '{item['name']}' (ID: {item_id_str}) removed successfully.")
    except Exception as e:
        await ctx.send("An error occurred while trying to remove the item. Please try again later.")
        print(f"Error removing market item: {e}")

@bot.command()
@commands.is_owner()
async def assign_role(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f"Assigned {role.name} to {user.name}.")

    save_db()

@bot.command()
@commands.is_owner()
async def remove_role(ctx, user: discord.Member, role: discord.Role):
    await user.remove_roles(role)
    await ctx.send(f"Removed {role.name} from {user.name}.")

    save_db()

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Check if the message starts with !credit
    if message.content.startswith("!credit"):
        ctx = await bot.get_context(message)
        try:
            # Extract the portion after !credit
            user_id_or_name = message.content[7:].strip()  # Strip the part after "!credit"
            
            if user_id_or_name:  # If there is something after !credit
                try:
                    # Try to convert it to a member using mention or name
                    user = await commands.MemberConverter().convert(ctx, user_id_or_name)
                except commands.BadArgument:
                    # If conversion fails, assume the user meant the author
                    user = ctx.author
            else:
                user = ctx.author  # Default to the author if no argument is provided

            user_id = user.id
            ensure_user_data(user_id)
            current_credits = get_user_credits(user_id)

            embed = discord.Embed(title="Social Credits!", color=0x00ff00)
            embed.add_field(name="Credits", value=f"{user.mention} has {current_credits} credits!", inline=False)

            await ctx.reply(embed=embed, mention_author=True)

            # Ensure any changes are saved
            save_db()

        except Exception as e:
            print(f"Error in !credit command: {e}")
            await ctx.send("An error occurred while retrieving the credits.")

    await bot.process_commands(message)

@bot.command()
@commands.has_permissions(administrator=True)
async def addcredits(ctx, user: discord.Member, amount: int):
    if amount < 0:
        await ctx.send("Cannot add negative credits.")
        return

    user_id = user.id
    ensure_user_data(user_id)
    current_credits = get_user_credits(user_id)
    new_credits = current_credits + float(amount)
    set_user_credits(user_id, new_credits)

    await ctx.send(f"Added {float(amount)} credits to {user.mention}. They now have {float(new_credits)} credits.")
    
    save_db()

@bot.command()
@commands.has_permissions(administrator=True)
async def removecredits(ctx, user: discord.Member, amount: int):
    if amount < 0:
        await ctx.send("Cannot remove negative credits.")
        return

    user_id = user.id
    ensure_user_data(user_id)
    current_credits = get_user_credits(user_id)

    if amount > current_credits:
        await ctx.send(f"{user.mention} does not have enough credits to remove {amount}. They currently have {current_credits} credits.")
        return

    new_credits = current_credits - amount
    set_user_credits(user_id, new_credits)

    await ctx.send(f"Removed {amount} credits from {user.mention}. They now have {new_credits} credits.")
    
    save_db()

@bot.command()
@commands.has_permissions(administrator=True)
async def setcredits(ctx, user: discord.Member, amount: int):
    if amount < 0:
        await ctx.send("Cannot set negative credits.")
        return

    user_id = user.id
    ensure_user_data(user_id)
    set_user_credits(user_id, amount)
    await ctx.send(f"Set {user.name}'s credits to {amount}.")

    save_db()

@bot.command()
@commands.has_permissions(administrator=True)
async def endsac(ctx):
    if not db.get("sac_active", False):
        await ctx.send("No sacrifice is currently active.")
        return

    db["custom_luck_multiplier"] = 1
    db["sac_amount"] = 0
    db["sac_active"] = False
    db["sac_spins"] = 0
    db["sac_limit_reached"] = False
    await ctx.send("Sacrifice ended.")

    save_db()

@bot.command()
@commands.has_permissions(administrator=True)
async def unsac(ctx):
    db["sac_active"] = False
    db["sac_amount"] = 0
    db["custom_luck_multiplier"] = 1
    db["sac_spins"] = 0
    db["sac_limit_reached"] = False
    await ctx.send("Sacrifice has been disabled.")
    save_db()

@bot.command()
@commands.has_permissions(administrator=True)
async def rig(ctx, rarity: int):
    if rarity < 1 or rarity >= len(rarityNames):
        await ctx.send("Invalid rarity level.")
        return

    user_id = ctx.author.id
    ensure_user_data(user_id)

    # Set rigged result
    db["rigged_result"] = rarity
    await ctx.send(f"Set rigged result to {rarityNames[rarity]}.")

    save_db()

@bot.command()
async def leaderboard(ctx):
    sorted_users = sorted(db["Social_credits"].items(), key=lambda x: x[1], reverse=True)
    top_users = sorted_users[:10]

    embed = discord.Embed(title="Leaderboard", color=0x00ff00)
    for i, (user_id, credits) in enumerate(top_users):
        try:
            # Attempt to convert user_id to an int and fetch the member
            member = await bot.fetch_user(int(user_id))
            username = member.mention if member else f"Unknown User (ID: {user_id})"
        except ValueError:
            # If user_id isn't an integer, use it as is
            username = f"Invalid User ID: {user_id}"
        except discord.NotFound:
            # Handle case where the user is not found by Discord
            username = f"User Not Found (ID: {user_id})"
        except discord.HTTPException:
            # Handle any other HTTP-related issues
            username = f"Failed to fetch user (ID: {user_id})"

        # Set credits to "∞" if they exceed a certain threshold
        if credits >= 1000000000000000000000000000:
            credits = "∞"
        else:
            credits = str(credits)

        embed.add_field(name="", value=f"{i + 1}. {username} has {credits} credits", inline=False)

    await ctx.send(embed=embed)
    save_db()

@bot.command()
async def pay(ctx, user: discord.Member, amount: int):
    if amount <= 0:
        await ctx.send("Amount must be positive.")
        return

    sender_id = ctx.author.id
    recipient_id = user.id

    ensure_user_data(sender_id)
    ensure_user_data(recipient_id)

    tax = int(amount * 0.1)
    net_amount = amount + tax

    old_sender_credits = get_user_credits(sender_id)
    new_sender_credits = old_sender_credits - net_amount

    old_recipient_credits = get_user_credits(recipient_id)
    new_recipient_credits = old_recipient_credits + amount

    sender_credits = get_user_credits(sender_id)
    if sender_credits < net_amount:
        await ctx.send("You don't have enough credits. (note ther is a 10% tax)")
        return

    # Transfer credits
    set_user_credits(sender_id, sender_credits - net_amount)
    set_user_credits(recipient_id, get_user_credits(recipient_id) + amount)

    embed = discord.Embed(color=0xFFFF00)
    embed.add_field(name="Success!", value=f"{ctx.author.mention} has given {user.mention} {amount} credits!", inline=False)
    embed.add_field(name="", value=f"{ctx.author.mention} has been charged {net_amount} credits!", inline=False)
    embed.add_field(name=f"", value=f"{ctx.author.mention} has {old_sender_credits} -> {new_sender_credits} Social Credits!", inline=True )
    embed.add_field(name=f"", value=f"{user.mention} has {old_recipient_credits} -> {new_recipient_credits} Social Credits!", inline=True)
    await ctx.send(embed=embed)

    save_db()

@bot.command()
async def sac(ctx, amount: int):
    if amount <= 0:
        await ctx.send("Amount must be positive.")
        return
    
    if amount < 100:
        await ctx.send("amount must be positive.")

    user_id = ctx.author.id
    ensure_user_data(user_id)

    if db.get("sac_active", False):
        await ctx.send("A sacrifice is already active.")
        return
    
    tax = int(amount * 0.1)
    net_amount = amount + tax

    credits = get_user_credits(user_id)
    if credits < net_amount:
        await ctx.send("You don't have enough credits to sacrifice. (note there is a 10% tax)")
        return

    db["sac_amount"] = amount
    db["sac_active"] = True
    db["sac_spins"] = 0
    db["sac_limit_reached"] = False
    db["custom_luck_multiplier"] = round(max(0.207125 * (2.34915 * amount + 463.458) ** 0.5 - 4.48083, 1), 1)

    luck_multiplier = db["custom_luck_multiplier"]

    set_user_credits(user_id, credits - amount)
    embed = discord.Embed(color=0xFFFF00)
    embed.add_field(name="The Flowr gods heed your sacrifice...", value="\u200b", inline=False)
    embed.add_field(name=f"A {luck_multiplier}x luck boost has been activated!", value="\u200b", inline=False)
    embed.add_field(name="Sacrificed Social Credit", value=f"{amount}", inline=False)
    embed.add_field(name="Successful Sacrifice", value=f"{ctx.author.mention} sacrificed {amount} credits!", inline=False)

    await ctx.send(embed=embed)

    save_db()

@bot.command()
async def help1(ctx):
    embed = discord.Embed(title="Help", color=0x00ff00)
    embed.add_field(name="!spin", value="Spin the wheel to earn credits and receive a random rarity based on luck and mob type.", inline=False)
    embed.add_field(name="!credit", value="Check your current credit balance.", inline=False)
    embed.add_field(name="!pay <user> <amount>", value="Pay credits to another user with a 10% tax.", inline=False)
    embed.add_field(name="!sac <amount>", value="Sacrifice credits to increase your luck boost.", inline=False)
    embed.add_field(name="!leaderboard", value="Show the top 10 users based on credits.", inline=False)
    embed.add_field(name="!market <page>", value="Show the current market", inline=False)
    embed.add_field(name="!addmarket", value="Contribute to the madness of the market", inline=False)
    embed.add_field(name="!delmarket", value="Delete your own market", inline=False)
    embed.add_field(name="!buy <Makret_ID>", value="Buy another persons offer", inline=False)
    embed.add_field(name="!enter", value="If a giveaway is active you enter it.", inline=False)
    embed.add_field(name="!help1", value="Shows this message.", inline=False)
    await ctx.send(embed=embed)

    save_db()

@bot.command()
@commands.has_permissions(administrator=True)
async def giveaway(ctx, duration: int, *, prize: str):
    """Start a giveaway. Only admins can use this command.
    
    Args:
    duration (int): Duration of the giveaway in minutes.
    prize (str): Description of the prize.
    """
    if duration <= 0:
        await ctx.send("Duration must be greater than 0 minutes.")
        return

    # Check if there is an active giveaway
    if "giveaway_data" in db and db["giveaway_data"].get("active", False):
        await ctx.send("A giveaway is already active.")
        return

    # Start the giveaway
    end_time = discord.utils.utcnow() + timedelta(minutes=duration)
    db["giveaway_data"] = {
        "active": True,
        "prize": prize,
        "end_time": end_time.isoformat(),
        "entries": []
    }
    save_db()

    embed = discord.Embed(title="Giveaway Started!", description=f"Prize: {prize}\nDuration: {duration} minutes", color=0x00ff00)
    embed.set_footer(text=f"Ends at {end_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    await ctx.send(embed=embed)

@bot.command()
async def enter(ctx):
    """Enter the active giveaway."""
    if "giveaway_data" not in db or not db["giveaway_data"].get("active", False):
        await ctx.send("There is no active giveaway.")
        return

    user_id = str(ctx.author.id)

    # Check if the user has already entered
    if user_id in db["giveaway_data"]["entries"]:
        await ctx.send("You have already entered the giveaway.")
        return

    # Add the user to the giveaway entries
    db["giveaway_data"]["entries"].append(user_id)
    save_db()

    await ctx.send(f"{ctx.author.mention} has been entered into the giveaway!")

@bot.command()
@commands.has_permissions(administrator=True)
async def endgiveaway(ctx):
    """End the active giveaway and announce the winner."""
    if "giveaway_data" not in db or not db["giveaway_data"].get("active", False):
        await ctx.send("No active giveaway to end.")
        return

    giveaway_data = db["giveaway_data"]
    giveaway_data["active"] = False
    save_db()

    # Determine the winner
    if giveaway_data["entries"]:
        winner_id = random.choice(giveaway_data["entries"])
        winner = await bot.fetch_user(int(winner_id))
        prize = int(giveaway_data["prize"])  # Ensure prize is an integer

        embed = discord.Embed(title="Giveaway Ended!", description=f"Congratulations {winner.mention}! You won {prize} Credits!", color=0x00ff00)
        await ctx.send(embed=embed)

        # Ensure user data exists and update credits
        ensure_user_data(winner_id)
        current_credits = get_user_credits(winner_id)
        new_credits = current_credits + prize
        set_user_credits(winner_id, new_credits)
        save_db()
        
    else:
        await ctx.send("No one entered the giveaway. No winner to announce.")

    # Clear the giveaway data
    db["giveaway_data"] = {}
    save_db()

# Error handler for the command
@giveaway.error
async def giveaway_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You do not have permission to use this command.")

@bot.command()
async def buy(ctx, market_id: int):
    # Ensure the market item exists
    market_item = db["market"].get(str(market_id))
    if not market_item:
        await ctx.send("This market item does not exist.")
        return

    buyer_id = ctx.author.id
    item_price = market_item["price"]

    ensure_user_data(buyer_id)
    buyer_credits = get_user_credits(buyer_id)

    # Check if the buyer has enough credits
    if buyer_credits < item_price:
        await ctx.send("You do not have enough credits to purchase this item.")
        return

    seller_id = int(market_item["owner"])
    ensure_user_data(seller_id)
    seller_credits = get_user_credits(seller_id)

    # Calculate tax (10%)
    tax = item_price * 0.1
    net_price = item_price + tax

    # Deduct the price from the buyer's credits
    new_buyer_credits = buyer_credits - net_price
    set_user_credits(buyer_id, new_buyer_credits)

    # Add the net price to the seller's credits
    new_seller_credits = seller_credits + item_price
    set_user_credits(seller_id, new_seller_credits)

    # Send confirmation message to the buyer
    await ctx.send(
        f"{ctx.author.mention} has purchased '{market_item['name']}' from the market for {net_price} credits! "
        f"The seller received {item_price} credits after tax."
    )

    # DM the seller about the purchase
    seller = bot.get_user(seller_id)
    if seller:
        try:
            await seller.send(
                f"Your item '{market_item['name']}' was purchased by {ctx.author.name}#{ctx.author.discriminator} "
                f"You received {item_price}"
            )
        except discord.Forbidden:
            await ctx.send(f"Could not DM the seller about the purchase, but the transaction was completed.")

bot.run('your-bot-token')

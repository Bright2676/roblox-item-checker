import discord
from discord.ext import commands
import requests
import asyncio

TOKEN = "not taking my token little bro"
CHANNEL_ID = 0
ITEM_FILE = "item_ids.txt"

def load_item_ids():
    try:
        with open(ITEM_FILE, "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []

def save_item_ids():
    with open(ITEM_FILE, "w") as file:
        file.writelines(f"{item_id}\n" for item_id in ITEM_IDS)

ITEM_IDS = load_item_ids()

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="?", intents=intents)

async def is_item_on_sale(item_id):
    url = f"https://economy.roblox.com/v2/assets/{item_id}/details"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("IsForSale", False), data.get("PriceInRobux", None)
        else:
            print(f"Failed to fetch data for item {item_id}. Status code: {response.status_code}")
            return False, None
    except Exception as e:
        print(f"Error checking item {item_id}: {e}")
        return False, None

async def monitor_items():
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    notified = {}

    while not bot.is_closed():
        for item_id in ITEM_IDS:
            if item_id not in notified:
                notified[item_id] = None

            on_sale, price = await is_item_on_sale(item_id)

            if on_sale and notified[item_id] != "on_sale":
                notified[item_id] = "on_sale"
                embed = discord.Embed(
                    title="Item On Sale",
                    description=f"The item with ID {item_id} is now on sale for {price} Robux! <:yeah:1328531380849737739>\nCheck it out: [Click here](https://www.roblox.com/catalog/{item_id})",
                    color=discord.Color.green()
                )
                await channel.send(embed=embed)

            elif not on_sale and notified[item_id] != "off_sale":
                notified[item_id] = "off_sale"
                embed = discord.Embed(
                    title="Item Off Sale",
                    description=f"The item with ID {item_id} is now off sale. <:nope:1328532071903399967>\nCheck it out: [Click here](https://www.roblox.com/catalog/{item_id})",
                    color=discord.Color.red()
                )
                await channel.send(embed=embed)

        await asyncio.sleep(60)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    await bot.tree.sync()
    await bot.loop.create_task(monitor_items())

@bot.tree.command(name="add_item", description="Add a new Roblox item ID to monitor")
async def add_item(interaction: discord.Interaction, item_id: str):
    if item_id in ITEM_IDS:
        embed = discord.Embed(
            title="Item ID Monitoring",
            description=f"Item ID {item_id} is already being monitored.",
            color=discord.Color.yellow()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        ITEM_IDS.append(item_id)
        save_item_ids()
        embed = discord.Embed(
            title="Item ID Monitoring",
            description=f"Added item ID {item_id} to the monitoring list.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="list_items", description="List all currently monitored Roblox item IDs")
async def list_items(interaction: discord.Interaction):
    if ITEM_IDS:
        item_list = "\n".join(ITEM_IDS)
        embed = discord.Embed(
            title="Currently Monitored Item IDs",
            description=f"The following item IDs are being monitored:\n{item_list}",
            color=discord.Color.blue()
        )
    else:
        embed = discord.Embed(
            title="No Items Monitored",
            description="No item IDs are currently being monitored.",
            color=discord.Color.red()
        )
    await interaction.response.send_message(embed=embed, ephemeral=True)

bot.run(TOKEN)
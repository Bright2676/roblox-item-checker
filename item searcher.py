import discord
from discord.ext import commands
import requests
import asyncio

TOKEN = "YOUR TOKEN GOES HERE"
CHANNEL_ID = 0
ITEM_FILE = "item_ids.txt"

def load_item_ids():
    try:
        with open(ITEM_FILE, "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []

def save_item_ids(item_ids):
    with open(ITEM_FILE, "w") as file:
        file.writelines(f"{item_id}\n" for item_id in item_ids)

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
        item_ids = load_item_ids()
        for item_id in item_ids:
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
                embed.set_footer(text="Created by bright2676 - Version 1.0", icon_url="https://static.wikia.nocookie.net/nicos-nextbots/images/9/94/Steam.png/revision/latest?cb=20240428120708")
                await channel.send(embed=embed)

            elif not on_sale and notified[item_id] != "off_sale":
                notified[item_id] = "off_sale"
                embed = discord.Embed(
                    title="Item Off Sale",
                    description=f"The item with ID {item_id} is now off sale. <:nope:1328532071903399967>\nCheck it out: [Click here](https://www.roblox.com/catalog/{item_id})",
                    color=discord.Color.red()
                )
                embed.set_footer(text="Created by bright2676 - Version 1.0", icon_url="https://static.wikia.nocookie.net/nicos-nextbots/images/9/94/Steam.png/revision/latest?cb=20240428120708")
                await channel.send(embed=embed)

        await asyncio.sleep(60)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    await bot.tree.sync()
    bot.loop.create_task(monitor_items())

@bot.event
async def on_guild_join(guild):
    print(f"Joined guild {guild.name} (ID: {guild.id})")

    embed = discord.Embed(
        title="Guild Joined",
        description=(
            "Hello! \n"
            "I'm `roblox-item-checker`, an open-source GitHub repository for anyone to fork and run for their purposes. "
            "You can view the repo here: [GitHub Repo](https://github.com/Bright2676/roblox-item-checker) \n"
            "If you have any questions, please DM `bright2676`."
        ),
        color=discord.Color.green()
    )
    embed.set_footer(
        text="Created by bright2676 - Version 1.0",
        icon_url="https://static.wikia.nocookie.net/nicos-nextbots/images/9/94/Steam.png/revision/latest?cb=20240428120708"
    )
    
    if guild.system_channel:
        try:
            await guild.system_channel.send(embed=embed)
            print(f"Sent welcome message to the system channel of guild {guild.name}.")
        except discord.Forbidden:
            print(f"Unable to send a message to the system channel of guild {guild.name}.")
        except Exception as e:
            print(f"An unexpected error occurred while sending a message to the system channel: {e}")
    else:
        print(f"Guild {guild.name} does not have a system channel set.")

@bot.tree.command(name="add_item", description="Add a new Roblox item ID to monitor")
async def add_item(interaction: discord.Interaction, item_id: str):
    item_ids = load_item_ids()
    if item_id in item_ids:
        embed = discord.Embed(
            title="Item ID Monitoring",
            description=f"Item ID {item_id} is already being monitored.",
            color=discord.Color.yellow()
        )
        embed.set_footer(text="Created by bright2676 - Version 1.0", icon_url="https://static.wikia.nocookie.net/nicos-nextbots/images/9/94/Steam.png/revision/latest?cb=20240428120708")
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        item_ids.append(item_id)
        save_item_ids(item_ids)
        embed = discord.Embed(
            title="Item ID Monitoring",
            description=f"Added item ID {item_id} to the monitoring list.",
            color=discord.Color.green()
        )
        embed.set_footer(text="Created by bright2676 - Version 1.0", icon_url="https://static.wikia.nocookie.net/nicos-nextbots/images/9/94/Steam.png/revision/latest?cb=20240428120708")
        await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="remove_item", description="Remove an existing Roblox item ID from the monitoring list")
async def remove_item(interaction: discord.Interaction, item_id: str):
    item_ids = load_item_ids()
    if item_id in item_ids:
        item_ids.remove(item_id)
        save_item_ids(item_ids)
        embed = discord.Embed(
            title="Item ID Removed",
            description=f"Removed item ID {item_id} from the monitoring list.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Created by bright2676 - Version 1.0", icon_url="https://static.wikia.nocookie.net/nicos-nextbots/images/9/94/Steam.png/revision/latest?cb=20240428120708")
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(
            title="Item ID Not Found",
            description=f"Item ID {item_id} is not in the monitoring list.",
            color=discord.Color.orange()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="list_items", description="List all currently monitored Roblox item IDs")
async def list_items(interaction: discord.Interaction):
    item_ids = load_item_ids()
    if item_ids:
        item_list = "\n".join(item_ids)
        embed = discord.Embed(
            title="Currently Monitored Item IDs",
            description=f"The following item IDs are being monitored:\n{item_list}",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Created by bright2676 - Version 1.0", icon_url="https://static.wikia.nocookie.net/nicos-nextbots/images/9/94/Steam.png/revision/latest?cb=20240428120708")
    else:
        embed = discord.Embed(
            title="No Items Monitored",
            description="No item IDs are currently being monitored.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Created by bright2676 - Version 1.0", icon_url="https://static.wikia.nocookie.net/nicos-nextbots/images/9/94/Steam.png/revision/latest?cb=20240428120708")
    await interaction.response.send_message(embed=embed, ephemeral=True)

bot.run(TOKEN)

# Roblox Item Checker
A Discord bot that monitors Roblox items and notifies users when specific items go onsale or offsale.

## Features

- Tracks Roblox catalog items
- Sends notifications in Discord when an item goes onsale or offsale
- Configurable item list and notification channels
- Easy to run

## Usage

1. Invite the bot to your Discord server using the [bot invite link](https://discord.com/oauth2/authorize?client_id=1328532981153009664&permissions=8&integration_type=0&scope=applications.commands+bot).
2. Use commands to configure the bot (`add_item` and `remove_item` respectively)
3. The bot will automatically monitor items and send updates to the configured channel.

## Commands (thus far)

| Command               | Description                                         |
|-----------------------|-----------------------------------------------------|
| `/add_item <id>`      | Add an item to the item watchlist.                  |
| `/remove_item <id>`   | Remove an item from the item watchlist.             |
| `/list_items`         | View the current item watchlist.                    |

## Notes

Any contributions are welcome and respected! Please ensure that you aren't just cloning my bot and making it your own. Add something that makes it unique to you.
This project (if you couldn't tell) uses Discord.py, requests, and the Roblox API. Please ensure that you have these all installed.

import nextcord
from nextcord.ext import commands
import json
import os

# Load config
with open('config.json') as f:
    config = json.load(f)

TOKEN = config['discord_token']
GUILD_ID = int(config['guild_id'])

# Initialize bot with specific intents
intents = nextcord.Intents.default()
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix="mc ", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready! Logged in as {bot.user}')
    print(f'Bot is in {len(bot.guilds)} guilds')
    
    # Load commands
    for filename in os.listdir("commands"):
        if filename.endswith(".py"):
            try:
                bot.load_extension(f"commands.{filename[:-3]}")
                print(f'Loaded extension: {filename}')
            except Exception as e:
                print(f'Failed to load extension {filename}: {e}')

    # List registered commands
    print("\nRegistered Commands:")
    for cmd in bot.commands:
        print(f"- mc {cmd.name}: {cmd.description if cmd.description else 'No description'}")

@bot.event
async def on_command_error(ctx, error):
    print(f'Error in command {ctx.command}: {str(error)}')
    try:
        await ctx.send("❌ An error occurred")
    except Exception as e:
        print(f"Failed to send error message: {e}")

print('Starting bot...')
bot.run(TOKEN)

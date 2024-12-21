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

# Remove default help command
bot.remove_command('help')

@bot.command(name="help")
async def help(ctx):
    help_text = [
        "> 🤖 **Ulticraft Discord Bot - Minecraft Server Management**",
        "> ",
        "> Available Commands:",
        "> • `mc ping` - Check bot latency",
        "> • `mc gitupdate` - Update bot from Git",
        "> • `mc morning` - Set server time to morning",
        "> • `mc players` - List online players",
        "> • `mc start` - Start the server",
        "> • `mc stop` - Stop the server",
        "> • `mc restart` - Restart the server",
        "> • `mc rcon` - Send command to server",
        "> • `mc help` - Show this help message"
    ]
    await ctx.send("\n".join(help_text), ephemeral=True, suppress_embeds=True)

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
    error_msg = f'Error in command {ctx.command}: {str(error)}'
    print(error_msg)
    try:
        await ctx.send(f"> ❌ An error occurred\n```\n{error_msg}\n```", ephemeral=True, suppress_embeds=True)
    except Exception as e:
        print(f"Failed to send error message: {e}")

print('Starting bot...')
bot.run(TOKEN)

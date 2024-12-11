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
bot = commands.Bot(command_prefix="!", intents=intents)

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

    # Sync commands
    try:
        print("\nSyncing commands...")
        await bot.sync_all_application_commands()
        print("Command sync complete")
        
        # List registered commands
        commands = bot.get_all_application_commands()
        print("\nRegistered Commands:")
        for cmd in commands:
            print(f"- /{cmd.name}: {cmd.description}")
    except Exception as e:
        print(f"Error syncing commands: {e}")

@bot.event
async def on_application_command(interaction: nextcord.Interaction):
    print(f'Command {interaction.application_command.name} was triggered by {interaction.user}')

@bot.event
async def on_application_command_error(interaction: nextcord.Interaction, error: Exception):
    print(f'Error in command {interaction.application_command.name}: {str(error)}')
    try:
        if not interaction.response.is_done():
            await interaction.response.send_message("❌ An error occurred", ephemeral=True)
    except Exception as e:
        print(f"Failed to send error message: {e}")

print('Starting bot...')
bot.run(TOKEN)

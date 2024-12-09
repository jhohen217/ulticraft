import os
import json
import sys
import nextcord
from nextcord.ext import commands
from version import VERSION

# Load configuration
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    print("Error: config.json not found!")
    sys.exit(1)
except json.JSONDecodeError:
    print("Error: config.json is invalid!")
    sys.exit(1)

# Setup bot with all intents
intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    """Bot startup event handler"""
    print(f"=== Ulticraft Bot v{VERSION} ===")
    print(f"Logged in as {bot.user}")
    print(f"Bot is ready to serve in guild: {config['guild_id']}")
    print(f"Bot channel: {config['bot_channel_id']}")
    
    try:
        # Sync commands globally first
        print("Starting global command sync...")
        await bot.sync_all_application_commands()
        print("Global command sync complete!")
        
        # Then sync for specific guild
        guild_id = int(config['guild_id'])
        print(f"Syncing commands for guild ID: {guild_id}")
        guild = bot.get_guild(guild_id)
        if guild:
            await bot.sync_application_commands(guild_id=guild_id)
            print(f"Successfully synced commands for guild: {guild.name}")
            
            # Send startup message to bot channel
            channel = guild.get_channel(int(config['bot_channel_id']))
            if channel:
                await channel.send(f"🚀 Ulticraft Bot v{VERSION} is now online!")
            else:
                print(f"Warning: Could not find channel with ID: {config['bot_channel_id']}")
        else:
            print(f"Warning: Could not find guild with ID: {guild_id}")
            print("Available guilds:", [f"{g.name} ({g.id})" for g in bot.guilds])
    except Exception as e:
        print(f"Error during startup: {str(e)}")

def load_commands():
    """Load all command modules from the commands directory"""
    commands_dir = os.path.join(os.path.dirname(__file__), 'commands')
    for filename in os.listdir(commands_dir):
        if filename.endswith('.py'):
            command_module = f'commands.{filename[:-3]}'
            try:
                bot.load_extension(command_module)
                print(f"Loaded command module: {command_module}")
            except Exception as e:
                print(f"Failed to load command module {command_module}: {str(e)}")

if __name__ == "__main__":
    try:
        load_commands()
        bot.run(config['discord_token'])
    except Exception as e:
        print(f"Failed to start bot: {e}")
        sys.exit(1)

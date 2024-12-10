import os
import json
import sys
import asyncio
import nextcord
from nextcord.ext import commands
from version import VERSION

# Add the project root directory to Python path for proper imports
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

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

def load_commands():
    """Load all command modules from the commands directory"""
    commands_dir = os.path.join(project_root, 'commands')
    print(f"Loading commands from: {commands_dir}")
    
    for filename in os.listdir(commands_dir):
        if filename.endswith('.py'):
            command_module = f'commands.{filename[:-3]}'
            try:
                bot.load_extension(command_module)
                print(f"✓ Loaded command module: {command_module}")
            except Exception as e:
                print(f"✗ Failed to load command module {command_module}: {str(e)}")
                import traceback
                traceback.print_exc()

async def sync_commands():
    """Sync commands with Discord"""
    try:
        print("Starting command sync...")
        guild_id = int(config['guild_id'])
        guild = bot.get_guild(guild_id)
        
        if guild:
            print(f"Found guild: {guild.name}")
            # Sync commands specifically for our guild
            await bot.sync_application_commands(guild_id=guild_id)
            print(f"Successfully synced commands for guild: {guild.name}")
            
            # List registered commands
            print("\nRegistered commands:")
            for cmd in bot.application_commands:
                print(f"- /{cmd.name}")
        else:
            print(f"Warning: Could not find guild with ID: {guild_id}")
            print("Available guilds:", [f"{g.name} ({g.id})" for g in bot.guilds])
            
            # Try global sync as fallback
            print("Attempting global command sync...")
            await bot.sync_all_application_commands()
            print("Global command sync complete!")
    except Exception as e:
        print(f"Error during command sync: {str(e)}")
        import traceback
        traceback.print_exc()

@bot.event
async def on_ready():
    """Bot startup event handler"""
    print(f"=== Ulticraft Bot v{VERSION} ===")
    print(f"Logged in as {bot.user}")
    print(f"Bot is ready to serve in guild: {config['guild_id']}")
    print(f"Bot channel: {config['bot_channel_id']}")
    
    try:
        # Sync commands first
        await sync_commands()
        
        # Send startup message to bot channel
        guild_id = int(config['guild_id'])
        guild = bot.get_guild(guild_id)
        if guild:
            channel = guild.get_channel(int(config['bot_channel_id']))
            if channel:
                await channel.send(f"🚀 Ulticraft Bot v{VERSION} is now online!")
                
                # List available commands
                if bot.application_commands:
                    command_list = "\n".join([f"- /{cmd.name}" for cmd in bot.application_commands])
                    await channel.send(f"Available commands:\n```\n{command_list}\n```")
                else:
                    await channel.send("⚠️ No commands are currently registered!")
            else:
                print(f"Warning: Could not find channel with ID: {config['bot_channel_id']}")
    except Exception as e:
        print(f"Error during startup message: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        print("Starting command loading process...")
        load_commands()
        print("Command loading complete, starting bot...")
        bot.run(config['discord_token'])
    except Exception as e:
        print(f"Failed to start bot: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

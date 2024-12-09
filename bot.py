import os
import json
import subprocess
import sys
import nextcord
from nextcord.ext import commands
from nextcord import Interaction

VERSION = "1.1.0"

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

def check_channel(interaction: Interaction) -> bool:
    """Check if the command is used in the correct channel"""
    return str(interaction.channel_id) == config['bot_channel_id']

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

def is_authorized(interaction: Interaction) -> bool:
    """Check if the user is authorized to use admin commands"""
    return str(interaction.user.id) in config['authorized_users']

@bot.slash_command(
    name="ping",
    description="Simple ping command to check if bot is responsive."
)
async def ping(interaction: Interaction):
    if not check_channel(interaction):
        await interaction.response.send_message(
            f"⚠️ Please use this command in <#{config['bot_channel_id']}>", 
            ephemeral=True
        )
        return
    
    await interaction.response.send_message(
        f"🏓 Pong! Bot v{VERSION}", 
        ephemeral=True
    )

@bot.slash_command(
    name="gitupdate",
    description="Pull latest code from Git and restart the bot."
)
async def gitupdate(interaction: Interaction):
    if not check_channel(interaction):
        await interaction.response.send_message(
            f"⚠️ Please use this command in <#{config['bot_channel_id']}>", 
            ephemeral=True
        )
        return

    if not is_authorized(interaction):
        await interaction.response.send_message(
            "⛔ You are not authorized to use this command.", 
            ephemeral=True
        )
        return

    await interaction.response.defer(ephemeral=True)

    try:
        # Get the directory where the bot script is located
        bot_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Change to the bot directory before git operations
        os.chdir(bot_dir)
        
        # Perform a git pull
        git_output = subprocess.check_output(
            ["git", "pull"], 
            stderr=subprocess.STDOUT
        ).decode("utf-8")

        # Send update message to bot channel
        channel = bot.get_channel(int(config['bot_channel_id']))
        if channel:
            await channel.send(f"📥 Bot update initiated by {interaction.user.display_name}")

        # Notify command user
        await interaction.followup.send(
            f"📥 Git pull output:\n```{git_output}```\n🔄 Restarting bot...", 
            ephemeral=True
        )

        # Exit the bot process - systemd or another supervisor should restart it
        print("Bot restart triggered by gitupdate command")
        os._exit(0)

    except subprocess.CalledProcessError as e:
        error_output = e.output.decode("utf-8")
        await interaction.followup.send(
            f"❌ Failed to update:\n```{error_output}```", 
            ephemeral=True
        )
    except Exception as e:
        await interaction.followup.send(
            f"❌ An unexpected error occurred:\n```{str(e)}```", 
            ephemeral=True
        )

if __name__ == "__main__":
    try:
        bot.run(config['discord_token'])
    except Exception as e:
        print(f"Failed to start bot: {e}")
        sys.exit(1)

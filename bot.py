import os
import json
import subprocess
import sys
import nextcord
from nextcord.ext import commands
from nextcord import Interaction

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

# Setup bot with intents
intents = nextcord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"Bot is ready to serve in guild: {config['guild_id']}")

def is_authorized(interaction: Interaction) -> bool:
    """Check if the user is authorized to use admin commands"""
    return str(interaction.user.id) in config['authorized_users']

@bot.slash_command(
    guild_ids=[int(config['guild_id'])],
    description="Simple ping command to check if bot is responsive."
)
async def ping(interaction: Interaction):
    await interaction.response.send_message("🏓 Pong!", ephemeral=True)

@bot.slash_command(
    guild_ids=[int(config['guild_id'])], 
    description="Pull latest code from Git and restart the bot."
)
async def gitupdate(interaction: Interaction):
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

        # Notify in Discord what happened
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

import os
import sys
import subprocess
import nextcord
from nextcord.ext import commands
import json

from utils import check_channel, is_authorized

# Load config for guild ID
with open('config.json') as f:
    config = json.load(f)

GUILD_ID = int(config['guild_id'])

class GitUpdateCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Initializing GitUpdateCommand cog")

    @nextcord.slash_command(name="gitupdate", description="Pull latest code from Git and restart the bot", guild_ids=[GUILD_ID])
    async def gitupdate(self, interaction: nextcord.Interaction):
        """Pull latest code from Git and restart the bot"""
        try:
            if not is_authorized(interaction):
                await interaction.response.send_message("⛔ You are not authorized to use this command.", ephemeral=True)
                return

            await interaction.response.defer(ephemeral=True)

            # Get the directory where the bot script is located
            bot_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            # Change to the bot directory before git operations
            os.chdir(bot_dir)
            
            # Perform a git pull
            git_output = subprocess.check_output(
                ["git", "pull"], 
                stderr=subprocess.STDOUT
            ).decode("utf-8")

            # Send update message
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
            print(f"Error in gitupdate command: {e}")
            await interaction.followup.send("❌ An error occurred", ephemeral=True)

def setup(bot):
    print(f"Setting up {__file__}")
    bot.add_cog(GitUpdateCommand(bot))

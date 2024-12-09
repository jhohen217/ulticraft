import os
import sys
import subprocess
from nextcord import Interaction
from nextcord.ext import commands

# Add the project root directory to Python path for proper imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from utils import check_channel, is_authorized, config

class GitUpdateCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="gitupdate",
        description="Pull latest code from Git and restart the bot.",
        guild_ids=[int(config['guild_id'])]
    )
    async def gitupdate(self, interaction: Interaction):
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
            bot_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            # Change to the bot directory before git operations
            os.chdir(bot_dir)
            
            # Perform a git pull
            git_output = subprocess.check_output(
                ["git", "pull"], 
                stderr=subprocess.STDOUT
            ).decode("utf-8")

            # Send update message to bot channel
            channel = self.bot.get_channel(int(config['bot_channel_id']))
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

def setup(bot):
    print(f"Setting up {__file__}")
    bot.add_cog(GitUpdateCommand(bot))

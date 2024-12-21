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

    @commands.command(name="gitupdate", description="Pull latest code from Git and restart the bot")
    async def gitupdate(self, ctx):
        """Pull latest code from Git and restart the bot"""
        try:
            if not is_authorized(ctx):
                await ctx.send("⛔ You are not authorized to use this command.")
                return

            # Send initial message
            status_msg = await ctx.send("⏳ Processing git update...")

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
            await status_msg.edit(
                content=f"📥 Git pull output:\n```{git_output}```\n🔄 Restarting bot..."
            )

            # Exit the bot process - systemd or another supervisor should restart it
            print("Bot restart triggered by gitupdate command")
            os._exit(0)

        except subprocess.CalledProcessError as e:
            error_output = e.output.decode("utf-8")
            await ctx.send(
                f"❌ Failed to update:\n```{error_output}```"
            )
        except Exception as e:
            print(f"Error in gitupdate command: {e}")
            await ctx.send("❌ An error occurred")

def setup(bot):
    print(f"Setting up {__file__}")
    bot.add_cog(GitUpdateCommand(bot))

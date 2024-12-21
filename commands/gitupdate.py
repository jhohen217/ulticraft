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

    @commands.command(
        name="gitupdate",
        help="Update bot from Git and restart (authorized users only)",
        brief="Update bot from Git",
        description="Update bot code and restart"
    )
    async def gitupdate(self, ctx):
        """Pull latest code from Git and restart the bot"""
        try:
            if not is_authorized(ctx):
                error_embed = nextcord.Embed(
                    description="⛔ You are not authorized to use this command.",
                    color=0xe74c3c
                )
                error_embed.set_author(name="", icon_url="https://i.imgur.com/1YBYnHn.png")
                await ctx.send(embed=error_embed)
                return

            # Send initial message
            processing_embed = nextcord.Embed(
                description="⏳ Processing git update...",
                color=0x2ecc71
            )
            processing_embed.set_author(name="", icon_url="https://i.imgur.com/1YBYnHn.png")
            status_msg = await ctx.send(embed=processing_embed)

            # Get the directory where the bot script is located
            bot_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            # Change to the bot directory before git operations
            os.chdir(bot_dir)
            
            # Perform a git pull
            git_output = subprocess.check_output(
                ["git", "pull"], 
                stderr=subprocess.STDOUT
            ).decode("utf-8")

            # Update message with git output and restart notice
            update_embed = nextcord.Embed(
                description=f"📥 **Git Pull Output:**\n```{git_output}```\n🔄 **Restarting bot...**",
                color=0x2ecc71
            )
            update_embed.set_author(name="", icon_url="https://i.imgur.com/1YBYnHn.png")
            await status_msg.edit(embed=update_embed)

            # Exit the bot process - systemd or another supervisor should restart it
            print("Bot restart triggered by gitupdate command")
            os._exit(0)

        except subprocess.CalledProcessError as e:
            error_output = e.output.decode("utf-8")
            error_embed = nextcord.Embed(
                description=f"❌ **Failed to update:**\n```{error_output}```",
                color=0xe74c3c
            )
            error_embed.set_author(name="", icon_url="https://i.imgur.com/1YBYnHn.png")
            await ctx.send(embed=error_embed)
        except Exception as e:
            print(f"Error in gitupdate command: {e}")
            error_embed = nextcord.Embed(
                description="❌ An error occurred",
                color=0xe74c3c
            )
            error_embed.set_author(name="", icon_url="https://i.imgur.com/1YBYnHn.png")
            await ctx.send(embed=error_embed)

def setup(bot):
    print(f"Setting up {__file__}")
    bot.add_cog(GitUpdateCommand(bot))

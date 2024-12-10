import os
import sys
from nextcord import Interaction, slash_command
from nextcord.ext import commands

# Add the project root directory to Python path for proper imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from utils import check_channel, config
from version import VERSION

class PingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="ping",
        description="Simple ping command to check if bot is responsive.",
        guild_ids=[int(config['guild_id'])]
    )
    async def ping(self, interaction: Interaction):
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

def setup(bot):
    print(f"Setting up {__file__}")
    bot.add_cog(PingCommand(bot))

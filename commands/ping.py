from nextcord import Interaction
from nextcord.ext import commands
from utils import check_channel, config
from version import VERSION

class PingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="ping",
        description="Simple ping command to check if bot is responsive."
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
    bot.add_cog(PingCommand(bot))

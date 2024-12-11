import nextcord
from nextcord.ext import commands

class PingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="ping",
        description="Check bot latency",
        guild_ids=[1086083334075068466]
    )
    async def ping(self, interaction: nextcord.Interaction):
        print(f"Ping command triggered by {interaction.user}")
        try:
            # Respond immediately
            await interaction.response.send_message("🏓 Calculating ping...")
            
            # Then edit the message with the actual latency
            latency = round(self.bot.latency * 1000)
            await interaction.edit_original_message(content=f"🏓 Pong! ({latency}ms)")
            print("Ping command response sent and updated")
        except Exception as e:
            print(f"Error in ping command: {str(e)}")
            if not interaction.response.is_done():
                await interaction.response.send_message("❌ An error occurred", ephemeral=True)

def setup(bot):
    bot.add_cog(PingCommand(bot))

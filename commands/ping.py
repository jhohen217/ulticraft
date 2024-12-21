import nextcord
from nextcord.ext import commands

class PingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="ping",
        help="Check the bot's latency in milliseconds",
        brief="Check bot latency"
    )
    async def ping(self, ctx):
        print(f"Ping command triggered by {ctx.author}")
        try:
            # Calculate and send latency in one message
            latency = round(self.bot.latency * 1000)
            await ctx.send(f"> 🏓 Pong! Latency: {latency}ms", ephemeral=True)
            print("Ping command response sent and updated")
        except Exception as e:
            print(f"Error in ping command: {str(e)}")
            await ctx.send("> ❌ An error occurred", ephemeral=True)

def setup(bot):
    bot.add_cog(PingCommand(bot))

import nextcord
from nextcord.ext import commands

class PingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="ping",
        description="Check bot latency"
    )
    async def ping(self, ctx):
        print(f"Ping command triggered by {ctx.author}")
        try:
            # Send initial message
            message = await ctx.send("🏓 Calculating ping...")
            
            # Then edit the message with the actual latency
            latency = round(self.bot.latency * 1000)
            await message.edit(content=f"🏓 Pong! ({latency}ms)")
            print("Ping command response sent and updated")
        except Exception as e:
            print(f"Error in ping command: {str(e)}")
            await ctx.send("❌ An error occurred")

def setup(bot):
    bot.add_cog(PingCommand(bot))

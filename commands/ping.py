import nextcord
from nextcord.ext import commands

class PingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="ping",
        help="Check bot's connection latency",
        brief="Check bot latency",
        description="Show bot latency"
    )
    async def ping(self, ctx):
        print(f"Ping command triggered by {ctx.author}")
        try:
            # Calculate latency
            latency = round(self.bot.latency * 1000)
            
            # Create embed with green border
            embed = nextcord.Embed(
                description=f"🏓 Current latency: **{latency}ms**",
                color=0x2ecc71  # Green color
            )
            
            # Set left border (similar to freak.fm style)
            embed.set_author(name="", icon_url="https://i.imgur.com/1YBYnHn.png")  # Transparent 1x1 pixel
            
            # Send message
            await ctx.send(embed=embed)
            
            print("Ping command response sent")
        except Exception as e:
            print(f"Error in ping command: {str(e)}")
            error_embed = nextcord.Embed(
                description="❌ An error occurred",
                color=0xe74c3c  # Red color for error
            )
            await ctx.send(embed=error_embed)

def setup(bot):
    bot.add_cog(PingCommand(bot))

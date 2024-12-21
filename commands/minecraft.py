import nextcord
from nextcord.ext import commands
from mcipc.rcon import Client
import json

# Load config
with open('config.json') as f:
    config = json.load(f)

GUILD_ID = int(config['guild_id'])
RCON_HOST = config['rcon']['host']
RCON_PORT = config['rcon']['port']
RCON_PASSWORD = config['rcon']['password']

class MinecraftCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Initializing MinecraftCommands cog")

    async def connect_rcon(self):
        try:
            with Client(RCON_HOST, RCON_PORT, passwd=RCON_PASSWORD) as client:
                return client
        except Exception as e:
            print(f"Failed to connect to RCON: {e}")
            return None

    @commands.command(
        name="morning",
        help="Set time to morning (6:00 AM)",
        brief="Set server time to morning",
        description="Set time to morning"
    )
    async def morning(self, ctx):
        # Send initial message
        processing_embed = nextcord.Embed(
            description="⏳ Setting time to morning...",
            color=0x2ecc71
        )
        processing_embed.set_author(name="", icon_url="https://i.imgur.com/1YBYnHn.png")
        status_msg = await ctx.send(embed=processing_embed)
        
        try:
            client = await self.connect_rcon()
            if client:
                resp = client.run('time set day')
                success_embed = nextcord.Embed(
                    description="☀️ Time set to morning!",
                    color=0x2ecc71
                )
                success_embed.set_author(name="", icon_url="https://i.imgur.com/1YBYnHn.png")
                await status_msg.edit(embed=success_embed)
            else:
                error_embed = nextcord.Embed(
                    description="❌ Failed to connect to server",
                    color=0xe74c3c
                )
                error_embed.set_author(name="", icon_url="https://i.imgur.com/1YBYnHn.png")
                await status_msg.edit(embed=error_embed)
        except Exception as e:
            print(f"Error in morning command: {e}")
            error_embed = nextcord.Embed(
                description="❌ An error occurred",
                color=0xe74c3c
            )
            error_embed.set_author(name="", icon_url="https://i.imgur.com/1YBYnHn.png")
            await status_msg.edit(embed=error_embed)

    @commands.command(
        name="players",
        help="Show list of online players",
        brief="List online players",
        description="Show online players"
    )
    async def players(self, ctx):
        # Send initial message
        processing_embed = nextcord.Embed(
            description="⏳ Getting player list...",
            color=0x2ecc71
        )
        processing_embed.set_author(name="", icon_url="https://i.imgur.com/1YBYnHn.png")
        status_msg = await ctx.send(embed=processing_embed)
        
        try:
            client = await self.connect_rcon()
            if client:
                resp = client.run('list')
                success_embed = nextcord.Embed(
                    description=f"👥 {resp}",
                    color=0x2ecc71
                )
                success_embed.set_author(name="", icon_url="https://i.imgur.com/1YBYnHn.png")
                await status_msg.edit(embed=success_embed)
            else:
                error_embed = nextcord.Embed(
                    description="❌ Failed to connect to server",
                    color=0xe74c3c
                )
                error_embed.set_author(name="", icon_url="https://i.imgur.com/1YBYnHn.png")
                await status_msg.edit(embed=error_embed)
        except Exception as e:
            print(f"Error in players command: {e}")
            error_embed = nextcord.Embed(
                description="❌ An error occurred",
                color=0xe74c3c
            )
            error_embed.set_author(name="", icon_url="https://i.imgur.com/1YBYnHn.png")
            await status_msg.edit(embed=error_embed)

def setup(bot):
    bot.add_cog(MinecraftCommands(bot))

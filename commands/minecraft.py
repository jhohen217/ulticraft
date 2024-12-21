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
        help="Sets the time to morning (6:00 AM) on the Minecraft server",
        brief="Set server time to morning"
    )
    async def morning(self, ctx):
        # Send initial message
        status_msg = await ctx.send("> ⏳ Setting time to morning...", ephemeral=True, suppress_embeds=True)
        
        try:
            client = await self.connect_rcon()
            if client:
                resp = client.run('time set day')
                await status_msg.edit(content="> ☀️ Time set to morning!", suppress_embeds=True)
            else:
                await status_msg.edit(content="> ❌ Failed to connect to server", suppress_embeds=True)
        except Exception as e:
            print(f"Error in morning command: {e}")
            await status_msg.edit(content="> ❌ An error occurred", suppress_embeds=True)

    @commands.command(
        name="players",
        help="Shows a list of all players currently online on the Minecraft server",
        brief="List online players"
    )
    async def players(self, ctx):
        # Send initial message
        status_msg = await ctx.send("> ⏳ Getting player list...", ephemeral=True, suppress_embeds=True)
        
        try:
            client = await self.connect_rcon()
            if client:
                resp = client.run('list')
                await status_msg.edit(content=f"> 👥 {resp}", suppress_embeds=True)
            else:
                await status_msg.edit(content="> ❌ Failed to connect to server", suppress_embeds=True)
        except Exception as e:
            print(f"Error in players command: {e}")
            await status_msg.edit(content="> ❌ An error occurred", suppress_embeds=True)

def setup(bot):
    bot.add_cog(MinecraftCommands(bot))

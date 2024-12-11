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

    async def connect_rcon(self, interaction: nextcord.Interaction):
        try:
            with Client(RCON_HOST, RCON_PORT, passwd=RCON_PASSWORD) as client:
                return client
        except Exception as e:
            print(f"Failed to connect to RCON: {e}")
            return None

    @nextcord.slash_command(
        name="morning",
        description="Set the time to morning on the server",
        guild_ids=[GUILD_ID]
    )
    async def morning(self, interaction: nextcord.Interaction):
        # Respond immediately
        await interaction.response.defer(ephemeral=True)
        
        try:
            client = await self.connect_rcon(interaction)
            if client:
                resp = client.run('time set day')
                await interaction.followup.send("☀️ Time set to morning!", ephemeral=True)
            else:
                await interaction.followup.send("❌ Failed to connect to server", ephemeral=True)
        except Exception as e:
            print(f"Error in morning command: {e}")
            await interaction.followup.send("❌ An error occurred", ephemeral=True)

    @nextcord.slash_command(
        name="players",
        description="List all online players",
        guild_ids=[GUILD_ID]
    )
    async def players(self, interaction: nextcord.Interaction):
        # Respond immediately
        await interaction.response.defer(ephemeral=True)
        
        try:
            client = await self.connect_rcon(interaction)
            if client:
                resp = client.run('list')
                await interaction.followup.send(f"👥 {resp}", ephemeral=True)
            else:
                await interaction.followup.send("❌ Failed to connect to server", ephemeral=True)
        except Exception as e:
            print(f"Error in players command: {e}")
            await interaction.followup.send("❌ An error occurred", ephemeral=True)

def setup(bot):
    bot.add_cog(MinecraftCommands(bot))

import nextcord
from nextcord.ext import commands
from mcipc.rcon import Client
import json
import os
import subprocess
import asyncio
import signal

# Load config
with open('config.json') as f:
    config = json.load(f)

GUILD_ID = int(config['guild_id'])
RCON_HOST = config['rcon']['host']
RCON_PORT = config['rcon']['port']
RCON_PASSWORD = config['rcon']['password']
SERVER_DIR = config['minecraft_server']['directory']
START_COMMAND = config['minecraft_server']['start_command']
STOP_TIMEOUT = config['minecraft_server']['stop_timeout']

class ServerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server_process = None
        print("Initializing ServerCommands cog")

    async def connect_rcon(self):
        try:
            with Client(RCON_HOST, RCON_PORT, passwd=RCON_PASSWORD) as client:
                return client
        except Exception as e:
            print(f"Failed to connect to RCON: {e}")
            return None

    @nextcord.slash_command(
        name="start",
        description="Start the Minecraft server",
        guild_ids=[GUILD_ID]
    )
    async def start(self, interaction: nextcord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        try:
            if self.server_process and self.server_process.poll() is None:
                await interaction.followup.send("❌ Server is already running!", ephemeral=True)
                return

            # Change to server directory and start the server
            os.chdir(SERVER_DIR)
            self.server_process = subprocess.Popen(START_COMMAND.split())
            await interaction.followup.send("🚀 Starting Minecraft server...", ephemeral=True)
        except Exception as e:
            print(f"Error starting server: {e}")
            await interaction.followup.send("❌ Failed to start server", ephemeral=True)

    @nextcord.slash_command(
        name="stop",
        description="Stop the Minecraft server",
        guild_ids=[GUILD_ID]
    )
    async def stop(self, interaction: nextcord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        try:
            client = await self.connect_rcon()
            if client:
                # Send stop command through RCON
                client.run('stop')
                await interaction.followup.send("🛑 Stopping Minecraft server...", ephemeral=True)
                
                # Wait for process to end
                if self.server_process:
                    try:
                        self.server_process.wait(timeout=STOP_TIMEOUT)
                    except subprocess.TimeoutExpired:
                        self.server_process.kill()
                    self.server_process = None
            else:
                await interaction.followup.send("❌ Failed to connect to server", ephemeral=True)
        except Exception as e:
            print(f"Error stopping server: {e}")
            await interaction.followup.send("❌ Failed to stop server", ephemeral=True)

    @nextcord.slash_command(
        name="restart",
        description="Restart the Minecraft server",
        guild_ids=[GUILD_ID]
    )
    async def restart(self, interaction: nextcord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        try:
            # Stop server
            client = await self.connect_rcon()
            if client:
                client.run('stop')
                await interaction.followup.send("🔄 Restarting Minecraft server...", ephemeral=True)
                
                # Wait for process to end
                if self.server_process:
                    try:
                        self.server_process.wait(timeout=STOP_TIMEOUT)
                    except subprocess.TimeoutExpired:
                        self.server_process.kill()
                    self.server_process = None

                # Wait a moment before starting
                await asyncio.sleep(5)

                # Start server
                os.chdir(SERVER_DIR)
                self.server_process = subprocess.Popen(START_COMMAND.split())
            else:
                await interaction.followup.send("❌ Failed to connect to server", ephemeral=True)
        except Exception as e:
            print(f"Error restarting server: {e}")
            await interaction.followup.send("❌ Failed to restart server", ephemeral=True)

    @nextcord.slash_command(
        name="rcon",
        description="Send a command to the server",
        guild_ids=[GUILD_ID]
    )
    async def rcon(self, interaction: nextcord.Interaction, command: str):
        await interaction.response.defer(ephemeral=True)
        
        try:
            client = await self.connect_rcon()
            if client:
                resp = client.run(command)
                await interaction.followup.send(f"✅ Command response:\n```\n{resp}\n```", ephemeral=True)
            else:
                await interaction.followup.send("❌ Failed to connect to server", ephemeral=True)
        except Exception as e:
            print(f"Error executing RCON command: {e}")
            await interaction.followup.send("❌ Failed to execute command", ephemeral=True)

def setup(bot):
    bot.add_cog(ServerCommands(bot))

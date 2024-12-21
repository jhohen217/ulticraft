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

    @commands.command(
        name="start",
        description="Start the Minecraft server"
    )
    async def start(self, ctx):
        status_msg = await ctx.send("⏳ Processing server start...")
        
        try:
            if self.server_process and self.server_process.poll() is None:
                await status_msg.edit(content="❌ Server is already running!")
                return

            # Change to server directory and start the server
            os.chdir(SERVER_DIR)
            self.server_process = subprocess.Popen(START_COMMAND.split())
            await status_msg.edit(content="🚀 Starting Minecraft server...")
        except Exception as e:
            print(f"Error starting server: {e}")
            await status_msg.edit(content="❌ Failed to start server")

    @commands.command(
        name="stop",
        description="Stop the Minecraft server"
    )
    async def stop(self, ctx):
        status_msg = await ctx.send("⏳ Processing server stop...")
        
        try:
            client = await self.connect_rcon()
            if client:
                # Send stop command through RCON
                client.run('stop')
                await status_msg.edit(content="🛑 Stopping Minecraft server...")
                
                # Wait for process to end
                if self.server_process:
                    try:
                        self.server_process.wait(timeout=STOP_TIMEOUT)
                    except subprocess.TimeoutExpired:
                        self.server_process.kill()
                    self.server_process = None
            else:
                await status_msg.edit(content="❌ Failed to connect to server")
        except Exception as e:
            print(f"Error stopping server: {e}")
            await status_msg.edit(content="❌ Failed to stop server")

    @commands.command(
        name="restart",
        description="Restart the Minecraft server"
    )
    async def restart(self, ctx):
        status_msg = await ctx.send("⏳ Processing server restart...")
        
        try:
            # Stop server
            client = await self.connect_rcon()
            if client:
                client.run('stop')
                await status_msg.edit(content="🔄 Restarting Minecraft server...")
                
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
                await status_msg.edit(content="❌ Failed to connect to server")
        except Exception as e:
            print(f"Error restarting server: {e}")
            await status_msg.edit(content="❌ Failed to restart server")

    @commands.command(
        name="rcon",
        description="Send a command to the server"
    )
    async def rcon(self, ctx, *, command: str):
        status_msg = await ctx.send("⏳ Executing command...")
        
        try:
            client = await self.connect_rcon()
            if client:
                resp = client.run(command)
                await status_msg.edit(content=f"✅ Command response:\n```\n{resp}\n```")
            else:
                await status_msg.edit(content="❌ Failed to connect to server")
        except Exception as e:
            print(f"Error executing RCON command: {e}")
            await status_msg.edit(content="❌ Failed to execute command")

def setup(bot):
    bot.add_cog(ServerCommands(bot))

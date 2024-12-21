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
        help="Start the Minecraft server if not running",
        brief="Start the server",
        description="Start the Minecraft server"
    )
    async def start(self, ctx):
        processing_embed = nextcord.Embed(
            description="⏳ Processing server start...",
            color=0x2ecc71
        )
        processing_embed.set_author(name="", icon_url="https://i.imgur.com/1YBYnHn.png")
        status_msg = await ctx.send(embed=processing_embed)
        
        try:
            if self.server_process and self.server_process.poll() is None:
                error_embed = nextcord.Embed(
                    description="❌ Server is already running!",
                    color=0xe74c3c
                )
                error_embed.set_author(name="", icon_url="https://i.imgur.com/1YBYnHn.png")
                await status_msg.edit(embed=error_embed)
                return

            # Change to server directory and start the server
            os.chdir(SERVER_DIR)
            self.server_process = subprocess.Popen(START_COMMAND.split())
            success_embed = nextcord.Embed(
                description="🚀 Starting Minecraft server...",
                color=0x2ecc71
            )
            success_embed.set_author(name="", icon_url="https://i.imgur.com/1YBYnHn.png")
            await status_msg.edit(embed=success_embed)
        except Exception as e:
            print(f"Error starting server: {e}")
            error_embed = nextcord.Embed(
                description="❌ Failed to start server",
                color=0xe74c3c
            )
            error_embed.set_author(name="", icon_url="https://i.imgur.com/1YBYnHn.png")
            await status_msg.edit(embed=error_embed)

    @commands.command(
        name="stop",
        help="Stop the Minecraft server safely (saves all data)",
        brief="Stop the server",
        description="Stop the Minecraft server"
    )
    async def stop(self, ctx):
        processing_embed = nextcord.Embed(
            description="⏳ Processing server stop...",
            color=0x2ecc71
        )
        processing_embed.set_author(name="", icon_url="https://i.imgur.com/1YBYnHn.png")
        status_msg = await ctx.send(embed=processing_embed)
        
        try:
            client = await self.connect_rcon()
            if client:
                # Send stop command through RCON
                client.run('stop')
                stopping_embed = nextcord.Embed(
                    description="🛑 Stopping Minecraft server...",
                    color=0x2ecc71
                )
                stopping_embed.set_author(name="", icon_url="https://i.imgur.com/1YBYnHn.png")
                await status_msg.edit(embed=stopping_embed)
                
                # Wait for process to end
                if self.server_process:
                    try:
                        self.server_process.wait(timeout=STOP_TIMEOUT)
                    except subprocess.TimeoutExpired:
                        self.server_process.kill()
                    self.server_process = None
            else:
                error_embed = nextcord.Embed(
                    description="❌ Failed to connect to server",
                    color=0xe74c3c
                )
                error_embed.set_author(name="", icon_url="https://i.imgur.com/1YBYnHn.png")
                await status_msg.edit(embed=error_embed)
        except Exception as e:
            print(f"Error stopping server: {e}")
            error_embed = nextcord.Embed(
                description="❌ Failed to stop server",
                color=0xe74c3c
            )
            error_embed.set_author(name="", icon_url="https://i.imgur.com/1YBYnHn.png")
            await status_msg.edit(embed=error_embed)

    @commands.command(
        name="restart",
        help="Restart the Minecraft server (players will need to reconnect)",
        brief="Restart the server",
        description="Restart the Minecraft server"
    )
    async def restart(self, ctx):
        processing_embed = nextcord.Embed(
            description="⏳ Processing server restart...",
            color=0x2ecc71
        )
        processing_embed.set_author(name="", icon_url="https://i.imgur.com/1YBYnHn.png")
        status_msg = await ctx.send(embed=processing_embed)
        
        try:
            # Stop server
            client = await self.connect_rcon()
            if client:
                client.run('stop')
                restarting_embed = nextcord.Embed(
                    description="🔄 Restarting Minecraft server...",
                    color=0x2ecc71
                )
                restarting_embed.set_author(name="", icon_url="https://i.imgur.com/1YBYnHn.png")
                await status_msg.edit(embed=restarting_embed)
                
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
                error_embed = nextcord.Embed(
                    description="❌ Failed to connect to server",
                    color=0xe74c3c
                )
                error_embed.set_author(name="", icon_url="https://i.imgur.com/1YBYnHn.png")
                await status_msg.edit(embed=error_embed)
        except Exception as e:
            print(f"Error restarting server: {e}")
            error_embed = nextcord.Embed(
                description="❌ Failed to restart server",
                color=0xe74c3c
            )
            error_embed.set_author(name="", icon_url="https://i.imgur.com/1YBYnHn.png")
            await status_msg.edit(embed=error_embed)

    @commands.command(
        name="rcon",
        help="Send a Minecraft command (e.g. `mc rcon say Hello`)",
        brief="Send server command",
        description="Execute Minecraft commands via RCON"
    )
    async def rcon(self, ctx, *, command: str):
        processing_embed = nextcord.Embed(
            description="⏳ Executing command...",
            color=0x2ecc71
        )
        processing_embed.set_author(name="", icon_url="https://i.imgur.com/1YBYnHn.png")
        status_msg = await ctx.send(embed=processing_embed)
        
        try:
            client = await self.connect_rcon()
            if client:
                resp = client.run(command)
                success_embed = nextcord.Embed(
                    description=f"✅ Command response:\n```\n{resp}\n```",
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
            print(f"Error executing RCON command: {e}")
            error_embed = nextcord.Embed(
                description="❌ Failed to execute command",
                color=0xe74c3c
            )
            error_embed.set_author(name="", icon_url="https://i.imgur.com/1YBYnHn.png")
            await status_msg.edit(embed=error_embed)

def setup(bot):
    bot.add_cog(ServerCommands(bot))

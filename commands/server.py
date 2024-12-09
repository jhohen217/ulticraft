import os
import subprocess
import time
import psutil
from nextcord import Interaction
from nextcord.ext import commands
from utils import check_channel, is_authorized, get_rcon_client, config

class ServerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server_process = None

    def is_server_running(self):
        """Check if the Minecraft server is running"""
        if self.server_process:
            try:
                # Check if process still exists
                process = psutil.Process(self.server_process.pid)
                return process.is_running()
            except (psutil.NoSuchProcess, AttributeError):
                self.server_process = None
                return False
        
        # Check if we can connect via RCON
        rcon = get_rcon_client()
        if rcon:
            rcon.stop()
            return True
        return False

    async def stop_server(self, interaction):
        """Stop the Minecraft server gracefully"""
        rcon = get_rcon_client()
        if rcon:
            try:
                # Warn players
                rcon.command("say §c⚠️ Server is shutting down in 10 seconds!")
                await interaction.followup.send("⏳ Warning players about shutdown...")
                time.sleep(10)
                
                # Save and stop
                rcon.command("save-all")
                time.sleep(2)
                rcon.command("stop")
                rcon.stop()
                
                # Wait for server to fully stop
                timeout = config['minecraft_server'].get('stop_timeout', 60)
                start_time = time.time()
                
                while self.is_server_running():
                    if time.time() - start_time > timeout:
                        await interaction.followup.send("⚠️ Server stop timeout reached!")
                        return False
                    time.sleep(1)
                
                return True
            except Exception as e:
                await interaction.followup.send(f"❌ Error during graceful shutdown: {str(e)}")
                return False
        return False

    @commands.slash_command(
        name="start",
        description="Start the Minecraft server."
    )
    async def start(self, interaction: Interaction):
        if not check_channel(interaction):
            await interaction.response.send_message(
                f"⚠️ Please use this command in <#{config['bot_channel_id']}>", 
                ephemeral=True
            )
            return

        if not is_authorized(interaction):
            await interaction.response.send_message(
                "⛔ You are not authorized to use this command.", 
                ephemeral=True
            )
            return

        await interaction.response.defer()

        if self.is_server_running():
            await interaction.followup.send("⚠️ Server is already running!")
            return

        try:
            server_dir = config['minecraft_server']['directory']
            start_cmd = config['minecraft_server']['start_command'].split()
            
            # Change to server directory and start
            os.chdir(server_dir)
            self.server_process = subprocess.Popen(
                start_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            await interaction.followup.send("🚀 Starting Minecraft server...")
            
            # Wait for server to start accepting connections
            max_attempts = 30
            for _ in range(max_attempts):
                if self.is_server_running():
                    await interaction.followup.send("✅ Server is now running!")
                    return
                time.sleep(2)
            
            await interaction.followup.send("⚠️ Server start timed out!")
        except Exception as e:
            await interaction.followup.send(f"❌ Error starting server: {str(e)}")

    @commands.slash_command(
        name="stop",
        description="Stop the Minecraft server."
    )
    async def stop(self, interaction: Interaction):
        if not check_channel(interaction):
            await interaction.response.send_message(
                f"⚠️ Please use this command in <#{config['bot_channel_id']}>", 
                ephemeral=True
            )
            return

        if not is_authorized(interaction):
            await interaction.response.send_message(
                "⛔ You are not authorized to use this command.", 
                ephemeral=True
            )
            return

        await interaction.response.defer()

        if not self.is_server_running():
            await interaction.followup.send("⚠️ Server is not running!")
            return

        if await self.stop_server(interaction):
            await interaction.followup.send("✅ Server has been stopped!")
        else:
            await interaction.followup.send("❌ Failed to stop server!")

    @commands.slash_command(
        name="restart",
        description="Restart the Minecraft server."
    )
    async def restart(self, interaction: Interaction):
        if not check_channel(interaction):
            await interaction.response.send_message(
                f"⚠️ Please use this command in <#{config['bot_channel_id']}>", 
                ephemeral=True
            )
            return

        if not is_authorized(interaction):
            await interaction.response.send_message(
                "⛔ You are not authorized to use this command.", 
                ephemeral=True
            )
            return

        await interaction.response.defer()

        if not self.is_server_running():
            await interaction.followup.send("⚠️ Server is not running! Starting...")
        else:
            await interaction.followup.send("🔄 Stopping server for restart...")
            if not await self.stop_server(interaction):
                await interaction.followup.send("❌ Failed to stop server for restart!")
                return
            await interaction.followup.send("✅ Server stopped, restarting...")

        # Start the server
        try:
            server_dir = config['minecraft_server']['directory']
            start_cmd = config['minecraft_server']['start_command'].split()
            
            # Change to server directory and start
            os.chdir(server_dir)
            self.server_process = subprocess.Popen(
                start_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for server to start accepting connections
            max_attempts = 30
            for _ in range(max_attempts):
                if self.is_server_running():
                    await interaction.followup.send("✅ Server has been restarted!")
                    return
                time.sleep(2)
            
            await interaction.followup.send("⚠️ Server restart timed out!")
        except Exception as e:
            await interaction.followup.send(f"❌ Error during restart: {str(e)}")

def setup(bot):
    bot.add_cog(ServerCommands(bot))

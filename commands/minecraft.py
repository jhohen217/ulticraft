import os
import sys
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

# Add the project root directory to Python path for proper imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from utils import check_channel, is_authorized, get_rcon_client, config

class MinecraftCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="rcon",
        description="Send a command to the Minecraft server via RCON.",
        guild_ids=[int(config['guild_id'])]
    )
    async def rcon(
        self,
        interaction: Interaction,
        command: str = SlashOption(
            name="command",
            description="The Minecraft command to execute",
            required=True
        )
    ):
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

        rcon = get_rcon_client()
        if rcon:
            try:
                response = rcon.command(command)
                rcon.stop()
                
                if response:
                    await interaction.followup.send(f"```\n{response}\n```")
                else:
                    await interaction.followup.send("Command executed successfully (no output)")
            except Exception as e:
                await interaction.followup.send(f"❌ Error executing command: {str(e)}")
        else:
            await interaction.followup.send("❌ Failed to connect to Minecraft server")

    @commands.slash_command(
        name="players",
        description="List all currently connected players.",
        guild_ids=[int(config['guild_id'])]
    )
    async def players(self, interaction: Interaction):
        if not check_channel(interaction):
            await interaction.response.send_message(
                f"⚠️ Please use this command in <#{config['bot_channel_id']}>", 
                ephemeral=True
            )
            return

        await interaction.response.defer()

        rcon = get_rcon_client()
        if rcon:
            try:
                response = rcon.command("list")
                rcon.stop()
                
                if response:
                    # Format the response to be more readable
                    formatted_response = response.replace("There are", "👥 There are")
                    await interaction.followup.send(f"```\n{formatted_response}\n```")
                else:
                    await interaction.followup.send("❌ No response from server")
            except Exception as e:
                await interaction.followup.send(f"❌ Error getting player list: {str(e)}")
        else:
            await interaction.followup.send("❌ Failed to connect to Minecraft server")

    @commands.slash_command(
        name="whitelist",
        description="Add a player to the server whitelist.",
        guild_ids=[int(config['guild_id'])]
    )
    async def whitelist(
        self,
        interaction: Interaction,
        username: str = SlashOption(
            name="username",
            description="Minecraft username to whitelist",
            required=True
        )
    ):
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

        rcon = get_rcon_client()
        if rcon:
            try:
                # Execute whitelist add command
                response = rcon.command(f"whitelist add {username}")
                
                # Get updated whitelist to confirm
                whitelist = rcon.command("whitelist list")
                rcon.stop()
                
                # Format response message
                message = f"```\n{response}\n```"
                if whitelist:
                    message += f"\nCurrent whitelist: ```\n{whitelist}\n```"
                
                await interaction.followup.send(message)
            except Exception as e:
                await interaction.followup.send(f"❌ Error updating whitelist: {str(e)}")
        else:
            await interaction.followup.send("❌ Failed to connect to Minecraft server")

    @commands.slash_command(
        name="morning",
        description="Skip to morning time in the Minecraft server.",
        guild_ids=[int(config['guild_id'])]
    )
    async def morning(self, interaction: Interaction):
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

        rcon = get_rcon_client()
        if rcon:
            try:
                # Set time to day (1000 ticks = morning)
                response = rcon.command("time set 1000")
                
                # Send message to all players
                rcon.command("say 🌅 Time has been set to morning!")
                rcon.stop()
                
                await interaction.followup.send("☀️ Time set to morning!")
            except Exception as e:
                await interaction.followup.send(f"❌ Error setting time: {str(e)}")
        else:
            await interaction.followup.send("❌ Failed to connect to Minecraft server")

def setup(bot):
    print(f"Setting up {__file__}")
    bot.add_cog(MinecraftCommands(bot))

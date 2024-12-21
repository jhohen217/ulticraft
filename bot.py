import nextcord
from nextcord.ext import commands
import json
import os
import asyncio
from mcipc.rcon import Client

# Load config
with open('config.json') as f:
    config = json.load(f)

TOKEN = config['discord_token']
GUILD_ID = int(config['guild_id'])

# Initialize bot with specific intents
intents = nextcord.Intents.default()
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix="mc ", intents=intents)

# Remove default help command
bot.remove_command('help')

@bot.command(name="help")
async def help(ctx):
    # Get all commands and sort them alphabetically
    commands = sorted(bot.commands, key=lambda x: x.name)
    
    # Create help text
    help_text = "🤖 **Ulticraft Discord Bot - Minecraft Server Management**\n\n"
    help_text += "**Available Commands:**\n"
    
    # Add each command with its description
    for cmd in commands:
        desc = cmd.help if cmd.help else (cmd.brief if cmd.brief else "No description available")
        help_text += f"• `mc {cmd.name}` - {desc}\n"

    help_text += "\nType `mc help <command>` for more details about a specific command.\n"
    help_text += "Example: `mc help ping` will show detailed help for the ping command."

    try:
        # Create embed with green border
        embed = nextcord.Embed(
            description=help_text,
            color=0x2ecc71  # Green color
        )
        embed.set_author(name="", icon_url="https://i.imgur.com/1YBYnHn.png")
        
        await ctx.send(embed=embed)
    except Exception as e:
        print(f"Error sending help message: {e}")
        error_embed = nextcord.Embed(
            description="❌ An error occurred while displaying help",
            color=0xe74c3c
        )
        await ctx.send(embed=error_embed)

@bot.command(name="helpfor")
async def helpfor(ctx, command_name: str):
    """Get detailed help for a specific command"""
    command = bot.get_command(command_name)
    if command:
        help_text = f"📖 **Help for `mc {command.name}`**\n\n"
        help_text += command.help if command.help else (command.brief if command.brief else 'No description available')
        
        if command.aliases:
            help_text += "\n\n**Aliases:** " + ", ".join(f"`mc {alias}`" for alias in command.aliases)
        
        embed = nextcord.Embed(
            description=help_text,
            color=0x2ecc71
        )
        embed.set_author(name="", icon_url="https://i.imgur.com/1YBYnHn.png")
        await ctx.send(embed=embed)
    else:
        error_embed = nextcord.Embed(
            description=f"❌ Command `{command_name}` not found.",
            color=0xe74c3c
        )
        await ctx.send(embed=error_embed)

async def update_status():
    while True:
        try:
            # Connect to RCON using config settings
            with Client(config['rcon']['host'], config['rcon']['port'], passwd=config['rcon']['password']) as client:
                # Get player list
                response = client.run('list')
                # Parse player count from response (format: "There are X of Y players online:")
                player_count = int(response.split()[2])  # Gets the number after "are"
                activity = nextcord.Activity(
                    type=nextcord.ActivityType.watching,
                    name=f"{player_count} players"
                )
                await bot.change_presence(activity=activity)
        except Exception as e:
            print(f"Error updating status: {e}")
            # Set default status on error
            activity = nextcord.Activity(
                type=nextcord.ActivityType.watching,
                name="0 players"
            )
            await bot.change_presence(activity=activity)
        await asyncio.sleep(240)  # Update every minute

@bot.event
async def on_ready():
    print(f'Bot is ready! Logged in as {bot.user}')
    print(f'Bot is in {len(bot.guilds)} guilds')
    
    # Start status update task
    bot.loop.create_task(update_status())
    
    # Load commands
    for filename in os.listdir("commands"):
        if filename.endswith(".py"):
            try:
                bot.load_extension(f"commands.{filename[:-3]}")
                print(f'Loaded extension: {filename}')
            except Exception as e:
                print(f'Failed to load extension {filename}: {e}')

    # List registered commands
    print("\nRegistered Commands:")
    for cmd in bot.commands:
        print(f"- mc {cmd.name}: {cmd.description if cmd.description else 'No description'}")

@bot.event
async def on_command_error(ctx, error):
    error_msg = f'Error in command {ctx.command}: {str(error)}'
    print(error_msg)
    try:
        error_embed = nextcord.Embed(
            description=f"❌ An error occurred\n```\n{error_msg}\n```",
            color=0xe74c3c
        )
        await ctx.send(embed=error_embed)
    except Exception as e:
        print(f"Failed to send error message: {e}")

print('Starting bot...')
bot.run(TOKEN)

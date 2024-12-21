import json
from mctools import RCONClient
from nextcord.ext.commands import Context

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

def check_channel(ctx: Context) -> bool:
    """Check if the command is being used in the correct channel"""
    return str(ctx.channel.id) == str(config['bot_channel_id'])

def is_authorized(ctx: Context) -> bool:
    """Check if the user is authorized to use admin commands"""
    return str(ctx.author.id) in config['authorized_users']

def get_rcon_client() -> RCONClient:
    """Get an RCON client connected to the Minecraft server"""
    try:
        rcon = RCONClient(
            config['rcon']['host'],
            port=config['rcon']['port']
        )
        rcon.login(config['rcon']['password'])
        return rcon
    except Exception as e:
        print(f"Failed to connect to RCON: {e}")
        return None

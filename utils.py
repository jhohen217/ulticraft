import json
from mctools import RCONClient
from nextcord import Interaction

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

def check_channel(interaction: Interaction) -> bool:
    """Check if the command is being used in the correct channel"""
    return str(interaction.channel_id) == str(config['bot_channel_id'])

def is_authorized(interaction: Interaction) -> bool:
    """Check if the user is authorized to use admin commands"""
    return str(interaction.user.id) in config['authorized_users']

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

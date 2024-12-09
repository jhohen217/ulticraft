from mctools import RCONClient
from nextcord import Interaction
import json

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

def get_rcon_client():
    """Create and return an RCON client"""
    try:
        rcon = RCONClient(config['rcon']['host'], port=config['rcon']['port'])
        if rcon.login(config['rcon']['password']):
            return rcon
        else:
            return None
    except Exception as e:
        print(f"RCON connection error: {e}")
        return None

def check_channel(interaction: Interaction) -> bool:
    """Check if the command is used in the correct channel"""
    return str(interaction.channel_id) == config['bot_channel_id']

def is_authorized(interaction: Interaction) -> bool:
    """Check if the user is authorized to use admin commands"""
    return str(interaction.user.id) in config['authorized_users']

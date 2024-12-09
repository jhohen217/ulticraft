# Ulticraft Discord Bot

A Discord bot for managing a Minecraft server with RCON integration.

## Features

- Discord slash command integration
- RCON connection to Minecraft server
- Server management capabilities
- Whitelist management
- Time control
- Player listing

## Commands

### General Commands
- `/ping` - Check if the bot is responsive

### Server Management
- `/start` - Start the Minecraft server
- `/stop` - Stop the Minecraft server gracefully
- `/restart` - Restart the Minecraft server
- `/gitupdate` - Update the bot from GitHub and restart

### Minecraft Commands
- `/rcon [command]` - Execute any Minecraft command via RCON
- `/players` - List all currently connected players
- `/whitelist [username]` - Add a player to the server whitelist
- `/morning` - Skip to morning time in-game

## Setup

1. Clone the repository
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `config.json.example` to `config.json` and fill in your settings:
   ```json
   {
       "discord_token": "YOUR_DISCORD_BOT_TOKEN",
       "authorized_users": [
           "USER_ID_1",
           "USER_ID_2"
       ],
       "guild_id": "YOUR_GUILD_ID",
       "bot_channel_id": "YOUR_CHANNEL_ID",
       "rcon": {
           "host": "YOUR_MINECRAFT_SERVER_IP",
           "port": 25575,
           "password": "YOUR_RCON_PASSWORD"
       },
       "minecraft_server": {
           "directory": "PATH_TO_SERVER_DIRECTORY",
           "start_command": "java -Xmx4G -Xms4G -jar server.jar nogui",
           "stop_timeout": 60
       }
   }
   ```

## Configuration

### Discord Settings
- `discord_token`: Your Discord bot token
- `authorized_users`: List of Discord user IDs allowed to use admin commands
- `guild_id`: The Discord server ID
- `bot_channel_id`: Channel ID where the bot will operate

### RCON Settings
- `rcon.host`: Minecraft server IP address
- `rcon.port`: RCON port (default: 25575)
- `rcon.password`: RCON password

### Minecraft Server Settings
- `minecraft_server.directory`: Path to Minecraft server directory
- `minecraft_server.start_command`: Command to start the server
- `minecraft_server.stop_timeout`: Timeout in seconds for server stop operations

## Requirements

- Python 3.8+
- nextcord
- mctools
- psutil

## Security

- Only authorized users can execute administrative commands
- Commands are restricted to a specific Discord channel
- RCON password is stored in config.json (keep this file secure)

## Version History

- 1.2.3: Fixed command registration compatibility with nextcord
- 1.2.2: Enhanced command registration with improved sync process
- 1.2.1: Fixed command registration and improved module imports
- 1.2.0: Added server management commands and RCON integration
- 1.1.0: Restructured commands and added version tracking
- 1.0.0: Initial release

# Ulticraft Discord Bot

A Discord bot that interfaces with a Minecraft server through slash commands.

## Features

- `/ping` - Simple command to check if the bot is responsive
- `/gitupdate` - Automatically pulls latest code from Git and restarts the bot (authorized users only)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/jhohen217/ulticraft.git
cd ulticraft
```

2. Set up configuration:
```bash
# Copy the example config file
cp config.json.example config.json

# Edit the config file with your settings
nano config.json
```

3. Install required Python packages:
```bash
pip3 install -r requirements.txt
```

4. Set up the systemd service:
```bash
# Copy service file to systemd directory
sudo cp discord-bot.service /etc/systemd/system/

# Reload systemd daemon
sudo systemctl daemon-reload

# Enable and start the service
sudo systemctl enable discord-bot
sudo systemctl start discord-bot
```

5. Check bot status:
```bash
sudo systemctl status discord-bot
```

## Configuration

The bot uses `config.json` for configuration. Copy `config.json.example` to `config.json` and update the following values:

- `discord_token`: Your Discord bot token from the Discord Developer Portal
- `authorized_users`: List of Discord user IDs allowed to use admin commands
- `guild_id`: The Discord server ID where the bot will operate

To get these IDs:
1. Enable Developer Mode in Discord (User Settings > App Settings > Advanced > Developer Mode)
2. Right-click on your server name and select "Copy ID" for the guild_id
3. Right-click on a user and select "Copy ID" for authorized_users

## Usage

The bot provides the following slash commands:
- `/ping` - Returns "Pong!" to confirm the bot is responsive
- `/gitupdate` - Pulls latest code from Git and automatically restarts the bot (only available to authorized users)

## Monitoring Logs

To view bot logs in real-time:
```bash
sudo journalctl -u discord-bot -f
```

## Security Note

The `config.json` file contains sensitive information and is automatically ignored by git. Never commit your actual `config.json` file to the repository. The `config.json.example` template is provided as a reference for setting up your own configuration.

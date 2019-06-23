# Raspberry Telegram Bot in Docker

This app runs a telegram bot in container to listen for messages.

## Requirements

- Docker (or anyone containerd)
- Internet access (to pull messages from Telegram servers)

## Usage

### Building image

Simple run:

    $ docker build -t rpi-telegram-bot .

### Running

Justs acess [How do I create a bot?](https://core.telegram.org/bots#3-how-do-i-create-a-bot) in Telegram Documentation and follow steps. When you receive your TOKEN, just fill in TELEGRAM_TOKEN environment variable in Docker.

    $ docker run -d -e "TELEGRAM_TOKEN=$YOUR_TELEGRAM_TOKEN" --restart unless-stopped --name rpi-telegram-bot rpi-telegram-bot

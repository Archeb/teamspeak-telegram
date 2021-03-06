# TeamSpeak-Telegram Bot
You can use this bot to integrate TeamSpeak with Telegram. With the support of Azure Text-to-Speech broadcast.

The main framework of this bot is from [ShaBren/ts-irc](https://github.com/ShaBren/ts-irc).

## Installation

1. Start your TeamSpeak Server, set up Server Query for it. Don't forget to whitelist your IP.
2. Ask @BotFather on Telegram to create a bot.
3. Apply for Azure Speech Service API.
4. Get [TS3AudioBot](https://github.com/Splamy/TS3AudioBot) running.
5. Rename `config.example.py` to `config.py`, then fill all your API information.
6. Modify the `bot.py` as you need. (For example, the English prompts were commented out, just uncomment them. And you may also need to edit `get_ssml()` to produce proper voice prompts)
7. Run `start.cmd`

Remember, Channel 1 will always be the "intercommunicating channel". To protect your private chat, add a channel password for it.

## Usage

- `/ts_getinfo` See who's in the server and which channels they're chatting on.
- `/ts [MESSAGE]` The message followed will be broadcasted serverwide, with voice prompts.


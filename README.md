# Sonus-Discord-Bot

__VERSION 1.0__

Sonus Bot is a bot that I've developed through the Python Programming language, it's developed for being implemented on a Discord server with simple to understand commands and easy source code structure and syntax.
As the first version of this bot, it currently has various bugs which will be improved in the near future.

Dependencies:

- Python Interpreter
- FFMPEG
- youtube_dl
- Discord API

Features/Commands:

- Playing music from YouTube URLs
- Pause command to pause music
- Resume command to resume paused music
- Stop command to stop music
- Ping command to output latency stats

Known Bugs (To be fixed):

- Already connected to voice_channel: when playing a song after the first song has finished, this error is output on the terminal.
- OSError: [Errno 9] Bad file descriptor: error output when the file is tried to be accessed on certain occasions.
- discord.ext.commands.errors.CommandInvokeError: Command raised an exception: TypeError: object NoneType can't be used in 'await' expression: this error is output on the terminal when the music is paused, resumed or stopped.
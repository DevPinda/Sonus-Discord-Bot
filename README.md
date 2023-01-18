# Sonus-Discord-Bot

__VERSION 1.1__

Sonus Bot is a bot that plays music from YouTube URLs and YouTube search on Discord, it's written in Python and mainly uses the discord.py API wrapper to send music to the voice channel through the use of the VoiceProtocol, with the coming of the V1.1 there has been an addition of a vast amount of bug fixing, feature implementing, optimization, comment writing and the addition of a newly made GUI that can be used to start and stop the bot with ease.

Dependencies:

- Python Interpreter
- ffmpeg
- yt-dlp
- discord.py
- YouTube API Token
- dotenv
- tkinter

Features/Commands:

- Playing music from YouTube URLs and YouTube search
- Pause command to pause music
- Resume command to resume paused music
- Stop command to stop music
- Ping command to output latency stats
- GUI to start/stop the bot

Known Bugs and issues (To be fixed):

- Issue with the YouTube library yt-dlp running a synchronous function 'play()' within an asynchronous event loop, this causes the bot to crash when a song with a long duration is played as it causes the bot's heartbeat to stop. This is a known issue with the library and is being worked on.
- After YouTube API search returns 5 results, there should be a way to cancel the search and return to previous state.
- Randomly there is a file error that is hard to reproduce, it involves the song file with the error being that it already exists when it had been previously deleted (I suspect file naming might be at blame but I need to run more tests for more conclusive evidence).
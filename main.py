# Below I have imported the modules, libraries and other dependancies crucial for the Discord bot
# to function such as the discord module that allows the program to communicate with the
# Discord API and to send and receive commands which shape the bot for what it is
import os
import discord
import requests
import json
import yt_dlp
from dotenv import load_dotenv
from discord.ext import commands

# Below I've called the 'load_dotenv' function that parses the 'TOKEN_file.env' file that is used in
# order to store the tokens for the Discord and YouTube APIs
load_dotenv('TOKEN_file.env')
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
YOUTUBE_TOKEN = os.getenv("YOUTUBE_TOKEN")

# Below I created the 'bot' variable that allows me to create Bot commands with the conjunction of
# the intents variable that specifies the bot's permission flags alongside the definition of the
# command prefix 'p!' and the case insensivity of commands that help mobile device users that
# possess auto-capitalisation
intents = discord.Intents.all()
bot = commands.Bot(case_insensitive=True, command_prefix=("p!"), intents = intents)

# Below I created the function which prints that the bot has come online successfully the moment
# when the bot has come online and is useful to realise the moment the bot is ready for when this
# script is ran in a command line interface program
@bot.event
async def on_ready():
    print("Bot online successfully!")  

# Below I created this utility method that sends a message to the channel containing the latency
# of the bot, this can be useful for users that may be experiencing packet loss, jitter and other
# possible network issues that may influence the bot's functionality
@bot.command()
async def ping(ctx):
    message = await ctx.send("Ping is: ")
    await message.edit(content = f"Ping is:  {round(bot.latency*1000,2)} ms !")

# Method below is the play method that is used in order to play songs, this is done by using the dependencies
# such as 'ffmpeg', 'yt_dlp' and the 'os', they are all used in conjunction to provide reliable and high
# quality audio as VoIP, I have included various way to combat the potential errors through conditional
# statements that check for instantiation and also exceptions
@bot.command()
async def play(ctx, url : str):
    channel = discord.utils.get(ctx.guild.voice_channels, name='General')
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)


    # Checks if the VoiceProtocol is instantiated and if it's connected, if so it disconnects and then
    # reconnects the VoiceProtocol, this is important as it avoids the issue when the bot is already
    # connected to the voice channel and it attempts to connect to it when it already is, this would
    # cause an error but I handled it properly which avoids a potential runtime error from occuring

    if voice and voice.is_connected():
        await voice.disconnect()
    voice = await channel.connect()

    # Makes sure to check if the VoiceProtocol is connected first and then checks if the song file exists,
    # which is called 'song.mp3' as the file name with a .mp3 file format
    if voice.is_connected():
        song_file = "song.mp3"
        song = os.path.isfile(song_file)

    # Tries to delete the song file if the song exists on the system by using the 'os' module, if it fails
    # due to insufficient permissions there is a PermissionError exception as contingency for any error
    try:
        if song:
            os.remove(song_file)
    except PermissionError:
        await ctx.send("Error: Stop the currently playing song using the 'stop' command") 
        return

    # These are the options that I specified for the yt_dlp (youtube_dl) such as the format, key,
    # preferred codec and quality for the 'song.mp3' file
    ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
    }

    # Implementation of the yt_dlt (youtube_dl) functionality in conjunction with the options defined just
    # before which are then downloaded using the url.
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # After downloading, the program will then find the file that ends with .mp3 (mp3 format files) and if
    # a match is found, the file is renamed to song_file variable's value
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file,song_file)

    # Plays the audio file named 'song_file' as the variable name using the ffmpeg dependency to transmit
    # the audio in VoIP in the Discord voice channel
    voice.volume = 100
    voice.play(discord.FFmpegPCMAudio(song_file))


# Method below defines a bot command that disconnects the bot by disconnecting the VoiceProtocol
@bot.command()
async def quit(ctx):
    voice = ctx.guild.voice_client

    try:
        await voice.disconnect()
        await ctx.send("Bot quit the channel successfuly!")
    except:
        print("Error while quitting bot!")

# Method below defines a bot command that pausing the song by pausing the VoiceProtocol 
@bot.command()
async def pause(ctx):
    voice = ctx.guild.voice_client
    if voice.is_playing():
        try:
            await voice.pause()
            await ctx.send("Bot paused successfully!")
        except:
            print("Error while pausing!")
    else:
        await ctx.send("Error: Bot isn't currently playing anything!")

# Method below defines a bot command that resumes the song by resuming the VoiceProtocol 
@bot.command()
async def resume(ctx):
    voice = ctx.guild.voice_client
    if voice.is_paused():
        try:
            await voice.resume()
            await ctx.send("Bot resumed successfully!")
        except:
            print("Error while resuming!")
    else:
        await ctx.send("Error: Bot isn't currently paused!")

# Method below defines a bot command that skips the song by stopping the VoiceProtocol 
@bot.command()
async def skip(ctx):
    voice = ctx.guild.voice_client
    if voice and voice.is_connected():
        if voice.is_playing():
            try:
                await voice.stop()
                await ctx.send("Bot skipped successfully!")
            except:
                print("Error while skipping!")
    else:
        await ctx.send("Error: Bot isn't currently connected to a voice channel.")

# Below is the method 'on_message' which is used in accordance with bot events that trigger whenever
# the bot registers that a message is received within a channel and within that message it compares
# its contents with strings in conditional statements and when they match they cause the bot to
# send messages or even create long and complex methods such as the '/play' functionality
@bot.event
async def on_message(message):
    # Used for utility to test whether the bot responds to message prompts by checking if the message
    # sent contains 'test' and if so, it returns a message to the channel
    if message.content == "test":
        await message.channel.send("Test: testing successful!")

    # Else-if below checks if the message's content starts with '/play' and if so it runs the code within,
    # which I will explain in numerous comments below
    elif message.content.startswith("-play"):
        searchQuery = message.content[len("-play "):]
        # This specifies the YouTube APIs URL through which the user's query and the token is sent to the
        # YouTube API as a requests which is then fulfilled by the API contacting the server and then
        # returning the JSON data as a response to the request
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={searchQuery}&key={YOUTUBE_TOKEN}"
        # Utilises the URL to perform the request and response action with the API and stores the JSON
        # information that is then assigned to the response variable
        response = requests.get(url)
        # Parses the response variable's JSON content into actual JSON which is then assigned to the
        # data variable
        data = json.loads(response.text)
        # Returns 5 items from the json data that are then stored in the results variable
        results = data["items"][:5]
        # Sets string value of the prompt which will be sent to the user on the channel
        response = "Please select a song by typing the corresponding number:\n"
        
        # For loop that is utilized to iterate over the results which are then 'split' into individual
        # results that are sent to channel one-by-one at every iteration, with an expected iteration
        # amount of 5 times, this naturally allows 5 individual results to be sent to the channel
        for i, result in enumerate(results):
            # title variable has been assigned the 'snippet' and 'title' key's values of the individual
            # result that was earlier split from the results
            title = result["snippet"]["title"]
            # Try block tries to run the code and avoids the KeyError with an exception that may arise due
            # to the possibility of the record not potentially possessing 'id' or 'videoId' keys 
            try:
                # video_id stores the 'id' and 'videoId' key's values
                video_id = result["id"]['videoId']
                # URL that is generated from the user's search as it is composed based on the static
                # YouTube base URL and the video_id variable defined earlier
                url = f"https://www.youtube.com/watch?v={video_id}"
                # Formats every output string each iteration that will be sent to the channel, this is done
                # on a one-by-one basis every iteration and not all at once
                response += f"{i+1}. {title}\n"
            except KeyError:
                continue
        # Sends message to the channel that prompts user to send int value that specifies their chosen song
        await message.channel.send(response)
    
        # Defined the 'check' function below which is used in order to check check the user's input based on
        # prompts that were sent to the channel earlier with a concise list of all results, however it is
        # not only limited to this as it also used in order to call the 'play', 'skip', 'pause' and 'resume'
        # functions that are defined later, this is triggered through a conditional check of the user's
        # input that performs a specific function call based on the match
        def check(m):
            # Returns the int digit value from 1-6 as it's specified that 5 results can be displayed
            return m.content.isdigit() and int(m.content) in range(1, 6)
        # Bot waits for the user to input an integer value to confirm one of the results in the results' range
        picked_number = await bot.wait_for('message', check=check)
        # Converts the variables' value string containing the int to a correct integer value
        picked_number = int(picked_number.content)
        # Adjusts the picked number's index value by decreasing it by 1
        picked_song = results[picked_number - 1]

        title = picked_song["snippet"]["title"]
        try:
            if picked_song["id"]["kind"] == 'youtube#video':
                video_id = picked_song["id"]['videoId']
        except KeyError:
            await message.channel.send("An error occurred while fetching the song details.")
        url = f"https://www.youtube.com/watch?v={video_id}"
        response = f"You picked {title}\n\nPlease wait a moment until the song is done loading, enjoy :)"
        await message.channel.send(response)
        await play(message,url)
    # If the message contains the specified string it tries to run the try block that contains the function
    # call to the method or if an exception occurs it prints an error to the console
    elif message.content == "-skip":
        try:
            await skip(message)
            await message.channel.send("Skipped successfully!")
        except:
            await message.channel.send("Error while skipping!")
    elif message.content == "-resume":
        try:
            await resume(message)
            await message.channel.send("Resumed successfully!")
        except:
            await message.channel.send("Error while resuming!")
    elif message.content == "-pause":
        try:
            await pause(message)
            await message.channel.send("Paused successfully!")
        except:
            await message.channel.send("Error while pausing!")
    elif message.content == "-quit":
        try:
            await quit(message)
            await message.channel.send("Bot has quit successfully!")
        except:
            await message.channel.send("Error while quitting!")
    # Call to the process_commands function that runs the API coroutine that processes the bot commands
    await bot.process_commands(message)

# Runs the bot by authenticating with the Discord API using the token
bot.run(DISCORD_TOKEN)
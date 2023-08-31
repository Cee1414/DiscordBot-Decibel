import discord
import os
import responses
import asyncio
import youtube_dl

async def send_message(message, user_message, is_private):
        try:
                response = responses.handle_response(user_message)
                await message.author.send(response) if is_private else await message.channel.send(response)
        except Exception as e:
                print(e)


def run_discord_bot(): 
        file_path = "~/Desktop/keys/DBGPT.txt"         #may be differnet depending on pc
        expanded_path = os.path.expanduser(file_path)  #may be differnet depending on pc
        tokenVar = open(expanded_path, "r").read().strip()
        
        TOKEN = tokenVar
        
        intents = discord.Intents.default()
        intents.message_content = True  # Allow reading message content
        intents.guilds = True
        
        client = discord.Client(intents=intents)

        voice_clients = {}

        yt_dl_opts = {'format': 'bestaudio/best'}
        ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

        ffmpeg_options = {'options': "-vn"}

        @client.event
        async def on_ready():
                print(f"{client.user} is now running")

        @client.event
        async def on_message(message):
                if message.author == client.user:
                        return
                        
                username = str(message.author)
                user_message = str(message.content)
                channel = str(message.channel)

                print(f"{username} said: '{user_message}' ({channel})")
                if user_message == "?help":
                        await send_message(message, user_message, is_private=True)
                elif user_message.startswith("?play"):
                        try:
                                url = user_message.split()[1]

                                voice_client = await message.author.voice.channel.connect()
                                voice_clients[voice_client.guild.id] = voice_client

                                loop = asyncio.get_event_loop()
                                data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

                                song = data[url]
                                player = discord.FFmpegPCMAudio(song, **ffmpeg_options, executable="/usr/bin/ffmpeg") #may be differnet depending on pc

                                voice_client.play(player)

                        except Exception as e:
                                print(e)
                                
                else: 
                        await send_message(message, user_message, is_private=False)
                        
                        

        client.run(TOKEN)
    

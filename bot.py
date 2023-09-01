import discord
import os
import responses
import asyncio
import yt_dlp

async def send_message(message, user_message, is_private):
        try:
                response = responses.handle_response(user_message)
                await message.author.send(response) if is_private else await message.channel.send(response)
        except Exception as e:
                print(f"An error occurred while sending message {e}")


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

        yt_dl_opts = {'format': 'bestaudio/best', "noplaylist": "True"}
        ytdl = yt_dlp.YoutubeDL(yt_dl_opts)

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
                        await send_message(message, user_message, is_private=False)

                        try:
                                url = user_message.split()[1]

                                voice_client = await message.author.voice.channel.connect()
                                voice_clients[voice_client.guild.id] = voice_client

                                loop = asyncio.get_event_loop()
                                data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

                                if 'is_live' in data and data['is_live']:
                                        print("Skipping live stream or playlist")
                                        return
                                if 'extractor_key' in data and data['extractor_key'] == 'YoutubePlaylist':
                                        print("Skipping playlist")
                                        return        
                                
                                best_audio_format = None
                                for fmt in data['formats']:
                                        if fmt['ext'] in ['mp3', 'm4a', 'aac']:  # Choose audio formats that you support
                                                best_audio_format = fmt
                                                break  # Stop after finding the first suitable audio format
                                        
                                if best_audio_format:
                                        audio_url = best_audio_format['url']
                                        print(best_audio_format)
                                        player = discord.FFmpegPCMAudio(audio_url, **ffmpeg_options, executable="/usr/bin/ffmpeg") #may be differnet depending on pc
                                        voice_client.play(player)
                                


                        except Exception as e:
                                print(f"An error occurred while playing audio:  {e}")
                                
                else: 
                        await send_message(message, user_message, is_private=False)
                        
                        

        client.run(TOKEN)
    

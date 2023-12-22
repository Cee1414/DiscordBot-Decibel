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
        file_path = "~/Desktop/keys/DBGPT.txt"         #may be different depending on pc
        expanded_path = os.path.expanduser(file_path)  #may be different depending on pc
        tokenVar = open(expanded_path, "r").read().strip()
        
        TOKEN = tokenVar
        
        intents = discord.Intents.default()
        intents.message_content = True  # Allow reading message content
        intents.guilds = True
        
        client = discord.Client(intents=intents)

        voice_clients = {}
        music_queue = []                                                                                        ##FIXME add music queue

        yt_dl_opts = {'format': 'bestaudio/best', "noplaylist": "True"}
        ytdl = yt_dlp.YoutubeDL(yt_dl_opts)

        ffmpeg_options = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
        "options": "-vn"}

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

                print(f"{username} said: '{user_message}' ({channel})")         #for debugging

                if user_message == "?help":
                        await send_message(message, user_message, is_private=False)
                
                elif user_message == "?join":
                        

                        try:
                                
                                voice_client = await message.author.voice.channel.connect()
                                voice_clients[voice_client.guild.id] = voice_client           #saves current voice client bot is in

                        except Exception as e:
                                print(f"An error occurred while attempting to join vc: {e}")

                elif user_message == "?dc":
                        

                        try:
                                
                                await voice_clients[message.guild.id].disconnect()
                                     

                        except Exception as e:
                                print(f"An error occurred while attempting to disconnect from vc: {e}")

                elif user_message == "?pause":
                        

                        try:
                                
                                await voice_clients[message.guild.id].pause()
                                     

                        except Exception as e:
                                print(f"An error occurred while attempting to pause: {e}")

                elif user_message == "?resume":
                        

                        try:
                                
                                await voice_clients[message.guild.id].resume()
                                     

                        except Exception as e:
                                print(f"An error occurred while attempting to resume music: {e}")                                          
        
                elif user_message.startswith("?play"):
                        await send_message(message, user_message, is_private=False)

                        try:
                                
                                voice_client = await message.author.voice.channel.connect()
                                voice_clients[voice_client.guild.id] = voice_client           #saves current voice client bot is in

                        except Exception as e:
                                print(f"An error occurred while connecting to vc:  {e}")
                        
                        try:
                                url = user_message.split()[1]
                                loop = asyncio.get_event_loop()
                                data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))     
                                
                                best_audio_format = None
                                for fmt in data['formats']:
                                        if fmt['ext'] in ['mp3', 'm4a', 'aac']:  # Choose audio formats that you support
                                                best_audio_format = fmt
                                                break  # Stop after finding the first suitable audio format
                                        
                                if best_audio_format:
                                        audio_url = best_audio_format['url']
                                        
                                        player = discord.FFmpegPCMAudio(audio_url, **ffmpeg_options, executable="/usr/bin/ffmpeg") #may be different depending on pc
                                        voice_clients[message.guild.id].play(player)
                                
                        except Exception as e:
                                print(f"An error occurred while playing audio:  {e}")

                elif user_message == "?stop":
                        try:
                                voice_clients[message.guild.id].stop()

                        except Exception as e:
                                print(f"An error occurred while stopping music:  {e}")              
                                
                else: 
                        await send_message(message, user_message, is_private=False)
                        
                        

        client.run(TOKEN)
    

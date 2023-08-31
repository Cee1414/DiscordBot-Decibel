import discord
import os
import responses

async def send_message(message, user_message, is_private):
        try:
                response = responses.handle_response(user_message)
                await message.author.send(response) if is_private else await message.channel.send(response)
        except Exception as e:
                print(e)


def run_discord_bot(): 
        file_path = "~/Desktop/keys/DBGPT.txt"
        expanded_path = os.path.expanduser(file_path) 
        tokenVar = open(expanded_path, "r").read().strip()
        
        TOKEN = tokenVar
        
        intents = discord.Intents.default()
        intents.message_content = True  # Allow reading message content
        

        client = discord.Client(intents=intents)


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
                if user_message[0] == "?":
                        user_message = send_message[1:]
                        await send_message(message, user_message, is_private=True)
                else: 
                        await send_message(message, user_message, is_private=False)
                        

        client.run(TOKEN)
    

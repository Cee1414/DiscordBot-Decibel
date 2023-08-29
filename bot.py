import discord
import os



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
        
        client.run(TOKEN)
    

import discord
import time

async def try_discord_chat(function):
    while True:
        try:
            await function()
            print("connection +")
            break
        except discord.errors.DiscordServerError:
            print("Discord Server Error")
            await time.sleep(2)
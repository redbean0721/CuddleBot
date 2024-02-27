from dotenv import load_dotenv
import discord
import json
import os

load_dotenv()

version = json.load(open("version.json", "r"))["version"]

bot = discord.Client(intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"Logged in: {bot.user} | {bot.user.id}\nVersion: {version}")


bot.run(os.getenv("TOKEN"))

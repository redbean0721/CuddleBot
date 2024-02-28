from dotenv import load_dotenv
import discord
import logging
import json
import os

from modules.log import setup_logging

setup_logging()
load_dotenv()

version = json.load(open("version.json", "r"))["version"]

bot = discord.Client(intents=discord.Intents.all())


@bot.event
async def on_ready():
    logging.info(f"Logged in: {bot.user} | {bot.user.id}")
    logging.info(f"Version: {version}")


bot.run(os.getenv("TOKEN"))

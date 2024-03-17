from dotenv import load_dotenv
import discord
from discord.ext import commands
import logging
import json
import os

from src.utils.log import setup_logging
# from src.utils.voice import connect_wavelink

setup_logging()
load_dotenv()

version = json.load(open("version.json", "r"))["version"]

bot = commands.AutoShardedBot(command_prefix="?", intents=discord.Intents.all())


# tree = app_commands.CommandTree(bot)


@bot.event
async def on_ready():
    # await bot.change_presence(activity=discord.Game(name="a game")) # Setting `Playing ` status
    # await bot.change_presence(activity=discord.Streaming(name="My Stream", url=my_twitch_url))  # Setting `Streaming ` status
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a song"))    # Setting `Listening ` status
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"))    # Setting `Watching ` status
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=":)"))
    logging.info(f"Logged in: {bot.user} | {bot.user.id}")
    logging.info(f"Version: {version}")
    slash = await bot.tree.sync()
    logging.info(f"Loaded {len(slash)} slash command(s)")
    # await connect_wavelink(bot)


# 載入指令程式檔案
@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f"src.cogs.{extension}")
    await ctx.send(f"Loaded {extension} done.")


# 卸載指令檔案
@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f"src.cogs.{extension}")
    await ctx.send(f"UnLoaded {extension} done.")


# 重新載入程式檔案
@bot.command()
async def reload(ctx, extension):
    await bot.reload_extension(f"src.cogs.{extension}")
    await ctx.send(f"ReLoaded {extension} done.")


# 一開始bot開機需載入全部程式檔案
async def load_extensions():
    for filename in os.listdir("./src/cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"src.cogs.{filename[:-3]}")


async def main():
    async with bot:
        setup_logging()
        await load_extensions()
        await bot.start(os.getenv("TOKEN"))

import datetime

import discord
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    token: str
    invite_link: str


bot = discord.Bot(intents=discord.Intents.all())


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="/help"), status=discord.Status.online)
    print(f"Logged in: {bot.user} | {bot.user.id}")

@bot.slash_command(name="hello", description="Say hello to the bot")
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond("Hey!")

@bot.slash_command(name="help", description="Say hello to the bot")
async def help(ctx: discord.ApplicationContext):
    embed = discord.Embed(title="CuddleBot 的指令列表", description="/about - 顯示關於機器人的訊息\n/ping - 查看機器人ㄉ延遲", color=0xb423ff, timestamp=datetime.datetime.now())
    embed.add_field(name="主要:", value="/help - 指令列表\n/hello - 跟你say Hellow\n/ping - ping我看我ㄉ延遲", inline=False)
    embed.add_field(name="Music:", value="目前停用此功能", inline=False)
    embed.add_field(name="歡迎加入支援群組", value=settings.invite_link, inline=False)
    embed.set_footer(text="Made with ❤")
    await ctx.respond(embed=embed)

@bot.slash_command(name="ping", description="ping我看我ㄉ延遲")
async def ping(ctx: discord.ApplicationContext):
    await ctx.respond(f'Discord延遲 {round(bot.latency * 1000)} ms')

@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
        if payload.message_id == 1114422293024751749:
            guild = bot.get_guild(payload.guild_id)
            if payload.emoji.name == "\u2705":  # ✅
                await payload.member.add_roles(guild.get_role(969627339107479582))
            elif payload.emoji.name == "\U0001F4E2":  # 📢
                await payload.member.add_roles(guild.get_role(1114418672358924320))
            elif payload.emoji.name == "\U0001F4AC":  # 💬
                await payload.member.add_roles(guild.get_role(1114418922234593320))
            elif payload.emoji.name == "\u2764\ufe0f":  # ❤️
                await payload.member.add_roles(guild.get_role(1046732884628733952))
            elif payload.emoji.name == "\U0001F515":  # 🔕
                await payload.member.add_roles(guild.get_role(1114417888581918781))
            elif payload.emoji.name == "\U0001F3B6":  # 🎶
                await payload.member.add_roles(guild.get_role(1114418404615528468))
            elif payload.emoji.name == "\u2642\ufe0f":  # ♂️
                await payload.member.add_roles(guild.get_role(1025069054492426305))
            elif payload.emoji.name == "\u2640\ufe0f":  # ♀️
                await payload.member.add_roles(guild.get_role(974553210075381760))

@bot.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    if payload.message_id == 1114422293024751749:
            guild = bot.get_guild(payload.guild_id)
            if payload.emoji.name == "\u2705":  # ✅
                await guild.get_member(payload.user_id).remove_roles(guild.get_role(969627339107479582))
            elif payload.emoji.name == "\U0001F4E2":  # 📢
                await guild.get_member(payload.user_id).remove_roles(guild.get_role(1114418672358924320))
            elif payload.emoji.name == "\U0001F4AC":  # 💬
                await guild.get_member(payload.user_id).remove_roles(guild.get_role(1114418922234593320))
            elif payload.emoji.name == "\u2764\ufe0f":  # ❤️
                await guild.get_member(payload.user_id).remove_roles(guild.get_role(1046732884628733952))
            elif payload.emoji.name == "\U0001F515":  # 🔕
                await guild.get_member(payload.user_id).remove_roles(guild.get_role(1114417888581918781))
            elif payload.emoji.name == "\U0001F3B6":  # 🎶
                await guild.get_member(payload.user_id).remove_roles(guild.get_role(1114418404615528468))
            elif payload.emoji.name == "\u2642\ufe0f":  # ♂️
                await guild.get_member(payload.user_id).remove_roles(guild.get_role(1025069054492426305))
            elif payload.emoji.name == "\u2640\ufe0f":  # ♀️
                await guild.get_member(payload.user_id).remove_roles(guild.get_role(974553210075381760))

if __name__ == "__main__":
    settings = Settings()
    bot.run(settings.token)

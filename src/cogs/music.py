import discord
import logging
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
from src.core.classes import Cog_Extension
from typing import Optional
import asyncio
from typing import cast
import wavelink

from src.utils.voice import connect_wavelink


class Music(Cog_Extension):
    logging.info("Cog 'Music' is loaded!")

    @commands.Cog.listener()
    async def on_ready(self):
        await connect_wavelink(self.bot)

    @commands.Cog.listener()
    async def on_wavelink_inactive_player(self, player: wavelink.Player) -> None:
        await player.channel.send(f"The player has been inactive for `{player.inactive_timeout}` seconds. Goodbye!")
        await player.disconnect()

    @app_commands.command()
    async def voice_status(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Identifier: {wavelink.Node.identifier()}\nuri: {wavelink.Node.uri()}\nStatus: {wavelink.Node.status()}\nplayers: {wavelink.Node.players()}")

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, payload: wavelink.NodeReadyEventPayload):
        logging.info(f"Wavelink Node connected: {payload.node!r} | Resumed: {payload.resumed}")

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, payload: wavelink.TrackStartEventPayload) -> None:
        player: wavelink.Player | None = payload.player
        if not player:
            return
        original: wavelink.Playable | None = payload.original
        track: wavelink.Playable = payload.track
        embed: discord.Embed = discord.Embed(title="Now Playing")
        embed.description = f"**{track.title}** by `{track.author}`"
        if track.artwork:
            embed.set_image(url=track.artwork)
        if original and original.recommended:
            embed.description += f"\n\n`This track was recommended via {track.source}`"
        if track.album.name:
            embed.add_field(name="Album", value=track.album.name)
        await player.home.send(embed=embed)

    @commands.command()
    async def play(self, ctx: commands.Context, *, query: str):
        if not ctx.guild:
            return

        player: wavelink.Player
        player = cast(wavelink.Player, ctx.voice_client)  # type: ignore

        if not player:
            try:
                player = await ctx.author.voice.channel.connect(cls=wavelink.Player)  # type: ignore
            except AttributeError:
                await ctx.send("Please join a voice channel first before using this command.")
                return
            except discord.ClientException:
                await ctx.send("I was unable to join this voice channel. Please try again.")
                return
        player.autoplay = wavelink.AutoPlayMode.partial
        if not hasattr(player, "home"):
            player.home = ctx.channel
        elif player.home != ctx.channel:
            await ctx.send(
                f"You can only play songs in {player.home.mention}, as the player has already started there.")
            return

        tracks: wavelink.Search = await wavelink.Playable.search(query)
        if not tracks:
            await ctx.send(f"{ctx.author.mention} - Could not find any tracks with that query. Please try again.")
            return

        if isinstance(tracks, wavelink.Playlist):
            added: int = await player.queue.put_wait(tracks)
            await ctx.send(f"Added the playlist **`{tracks.name}`** ({added} songs) to the queue.")
        else:
            track: wavelink.Playable = tracks[0]
            await player.queue.put_wait(track)
            await ctx.send(f"Added **`{track}`** to the queue.")

        if not player.playing:
            await player.play(player.queue.get(), volume=30)

        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

    @commands.command()
    async def skip(self, ctx: commands.Context):
        """Skip the current song."""
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        if not player:
            return

        await player.skip(force=True)
        await ctx.message.add_reaction("\u2705")

    @commands.command()
    async def nightcore(self, ctx: commands.Context):
        """Set the filter to a nightcore style."""
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        if not player:
            return

        filters: wavelink.Filters = player.filters
        filters.timescale.set(pitch=1.2, speed=1.2, rate=1)
        await player.set_filters(filters)

        await ctx.message.add_reaction("\u2705")

    @commands.command(name="toggle", aliases=["pause", "resume"])
    async def pause_resume(self, ctx: commands.Context):
        """Pause or Resume the Player depending on its current state."""
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        if not player:
            return

        await player.pause(not player.paused)
        await ctx.message.add_reaction("\u2705")

    @commands.command()
    async def volume(self, ctx: commands.Context, value: int):
        """Change the volume of the player."""
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        if not player:
            return

        await player.set_volume(value)
        await ctx.message.add_reaction("\u2705")

    @commands.command(aliases=["dc"])
    async def disconnect(self, ctx: commands.Context):
        """Disconnect the Player."""
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        if not player:
            return

        await player.disconnect()
        await ctx.message.add_reaction("\u2705")


async def setup(bot):
    await bot.add_cog(Music(bot))

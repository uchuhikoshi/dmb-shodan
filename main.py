import os
import asyncio
import discord

from discord.ext import commands
from yt_dlp import YoutubeDL

bot = commands.Bot(command_prefix='.')
queue = []

@bot.command()
async def isalive(ctx):
    await ctx.send("Look at you, hacker. A pathetic creature of meat and bones. Panting and sweating as you run through my corridors. How can you challenge a perfect, immortal machine?")

@bot.command(aliases=['j'])
async def join(ctx):
    author = ctx.author
    bot_vc = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)

    if author.voice is None:
        await ctx.send("You must be in a voice chat.")
    else:
        if bot_vc is None:
            return await author.voice.channel.connect()
        else:
            return bot_vc

@bot.command(aliases=['s'])
async def search(ctx, *, search_string):
    embed = discord.Embed()
    embed.title = f"Found for: {search_string}"
    embed.description = 'Type the `number` of desired track to play, or type `c`.'

    with YoutubeDL({
        'skip_download': 'True',
        'noplaylist': 'True',
        'format': 'bestaudio/best[height<=?720]',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            'preferredquality': '320',
        }]
    }) as ydl:
        info_dict = ydl.extract_info(f"ytsearch10:{search_string}")

    for i in range(len(info_dict['entries'])):
        track = info_dict['entries'][i]
        track_duration = 'Streaming'
        if not track['is_live']:
            track_duration = track['duration_string']

        embed.add_field(
            name=f"`{i+1}`. {track['title']} ({track_duration})",
            value=f"{track['webpage_url']}",
            inline=False
        )

    await ctx.send(embed=embed)

    def check(m):
        return m.author == ctx.author
    
    try:
        message = await bot.wait_for('message', timeout=30.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send("Timeout.")
        return

    user_respond = message.content
    if user_respond.isdigit() and int(user_respond) not in range(1, info_dict['playlist_count']):
        await ctx.send("Please, use your brains.")
        return
    elif user_respond == 'c':
        await ctx.send("Query canceled.")
        return
    
    user_respond = int(user_respond)-1
    queue.append({
        'title': info_dict['entries'][user_respond]['title'],
        'duration': info_dict['entries'][user_respond]['duration_string'],
        'url': info_dict['entries'][user_respond]['requested_downloads'][0]['url']
    })

@bot.command(aliases=['p'])
async def play(ctx, track):
    vc = await join(ctx)
    if vc is None:
        return

    FFMPEG_OPTS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }

    await ctx.send(f"Now playing: `{track['title']}` ({track['duration']})")
    if vc.is_playing():
        vc.stop()
    vc.play(discord.FFmpegPCMAudio(track['url'], **FFMPEG_OPTS))

@bot.command(aliases=['pq'])
async def play_queue(ctx):
    while queue:
        await play(ctx, queue.pop(0))
    await ctx.send("Queue is empty.")

@bot.command(aliases=['pp'])
async def pause(ctx):
    pass

if __name__ == '__main__':
    db_pk = os.environ['SHODAN_PK']
    bot.run(db_pk)


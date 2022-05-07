import os
import asyncio
import discord
import yapi_wrapper

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
    elif bot_vc is None:
        return await author.voice.channel.connect()

@bot.command(aliases=['s'])
async def search(ctx, *, content: yapi_wrapper.search):
    embed = discord.Embed()
    embed.title = f"Found for {ctx.message.content[3:]}:"
    embed.description = 'Type the `number` of desired track to play, or type `c`.'

    for i in range(len(content)):
        embed.add_field(
            name=f"`{i+1}`. {content[i]['title']}\t{content[i]['duration']}",
            value=f"{content[i]['url']}",
            inline=False
        )

    await ctx.send(embed=embed)

    def check(m):
        return m.author == ctx.author
    
    try: msg = await bot.wait_for('message', timeout=30.0, check=check)
    except asyncio.TimeoutError: await ctx.send("Timeout.")

    queue.append(content[int(msg.content)])

@bot.command(aliases=['p'])
async def play(ctx, url):
    vc = await join(ctx)
    if vc is None:
        bot_vc = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if bot_vc is None:
            return
        
        vc = bot_vc

    with YoutubeDL({'format': 'bestaudio', 'noplaylist': 'True'}) as ydl:
        info = ydl.extract_info(url, download=False)

    source = info['formats'][4]['url']

    FFMPEG_OPTS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }

    await ctx.send(f"Now playing: {info['title']}.")
    if vc.is_playing():
        vc.stop()
    vc.play(discord.FFmpegPCMAudio(source, **FFMPEG_OPTS))

@bot.command(aliases=['pq'])
async def play_queue(ctx):
    while queue:
        await play(queue.pop(0))

    await ctx.send("Queue is empty.")

@bot.command(aliases=['pp'])
async def pause(ctx):
    pass

if __name__ == '__main__':
    db_pk = os.environ['SHODAN_PK']
    bot.run(db_pk)


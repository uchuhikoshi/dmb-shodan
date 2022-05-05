import os
import asyncio
import discord
import youtube_dl
import yapi_wrapper

from discord.ext import commands

bot = commands.Bot(command_prefix='.')
queue = []

@bot.command()
async def isalive(ctx):
    await ctx.send("Look at you, hacker. A pathetic creature of meat and bones. Panting and sweating as you run through my corridors. How can you challenge a perfect, immortal machine?")

@bot.command(aliases=['j'])
async def join(ctx):
    author = ctx.author
    voice_channel = await author.voice.channel.connect()
    voice_channel.play(discord.FFmpegPCMAudio("lookatyou.mp3"))

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
            #if type(m.content) is type(int()) and m.content in range(1,11):
    
    try:
        msg = await bot.wait_for('message', timeout=30.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send("Timeout.")

    queue.append(content[int(msg.content)])

@bot.command(aliases=['p'])
async def play(ctx):
    ydl_opts = {
        'cachedir': 'none',
        'format': 'worst',
        'outtmpl': './dwnld'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([queue[0]['url']])
    
    vc = await ctx.author.voice.channel.connect()
    vc.play(discord.FFmpegPCMAudio("./dwnld"))

if __name__ == '__main__':
    db_pk = os.environ['SHODAN_PK']
    bot.run(db_pk)


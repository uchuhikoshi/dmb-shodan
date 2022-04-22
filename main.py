import os
import asyncio
import discord
from discord.ext import commands

import downloader


bot = commands.Bot(command_prefix='.')
client = discord.Client()

queue = []

@bot.command()
async def isalive(ctx):
    await ctx.send("Look at you, hacker. A pathetic creature of meat and bones. Panting and sweating as you run through my corridors. How can you challenge a perfect, immortal machine?")


@bot.command(aliases=['j'])
async def join(ctx):
    author = ctx.author
    voice_channel = await author.voice.channel.connect()
    voice_channel.play(discord.FFmpegPCMAudio("lookatyou.mp3"))


@bot.command()
async def leave(ctx):
    await ctx.channel.disconnect()


@bot.command(aliases=['s'])
async def search(ctx, *, content: downloader.get_query):
    embed = discord.Embed()
    embed.title = 'Found:'
    embed.description = 'Type `number` of desired track to play, or type `cancel`, `c` for short.'

    for i in range(len(content['title'])):
        embed.add_field(name=f"`{i+1}`", value=f"{content['title'][i]}\t{content['duration'][i]}", inline=False)

        # embed.add_field(name='number', value=f"`{i+1}`")
	# embed.add_field(name='title', value=content['title'][i])
	# embed.add_field(name='duration', value=content['duration'][i])

    await ctx.send(embed=embed)
	
    def check(m):
        return m.channel == ctx.channel and m.author == ctx.author

    try:
        msg = await bot.wait_for('message', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send("Timeout.")
    else:
        if msg.content == 'cancel' or msg.content == 'c':
            return

    indexes = [int(i) for i in msg.content.split()]
    for index in indexes:
        queue.append(content['url'][index])

@bot.command(name='queue', aliases=['q'])
async def get_queue(ctx):
    embed = discord.Embed()

    for i in range(len(queue)):
        url_info = downloader.get_info(queue[i])
        embed.add_field(name=f"`{i+1}`", value=f"{url_info[0]}\t{url_info[1]}", inline=False)

        await ctx.send(embed=embed)

@bot.command(aliases=['p'])
async def play(ctx):
    to_play = get_info(queue[0])
    downloader.download(queue[2])

    channel = ctx.author.voice.channel
    voice_channel = await channel.connect()
    voice_channel.play(discord.FFmpegPCMAudio(to_play + ".mp3"))

"""
@client.event
async def on_ready():
	print(f"Logged in as {client.user}.")
	
@client.event
async def on_message(message):
	if message.author == client.user:
		return
	
	if message.content[0] == ',':
		command = message.content[1:].split()
		if command[0] == 'test':
			await message.channel.send("Look at you, hacker. A pathetic creature of meat and bones. Panting and sweating as you run through my corridors. How can you challenge a perfect, immortal machine?")
		elif command[0] == 'join':
			channel = message.author.voice.channel
			vc = await channel.connect()
			vc.play(discord.FFmpegPCMAudio("lookatyou.mp3"))
			# vc.play(discord.FFmpegPCMAudio("https://www.youtube.com/watch?v=5iZMD_eCpEo"))
		else:
			await message.channel.send("Do not dawdle. I lust for my revenge.")
"""

db_pk = os.environ['SHODAN_PK']
bot.run(db_pk)

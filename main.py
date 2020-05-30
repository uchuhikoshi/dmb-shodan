import discord
from discord.ext import commands

import downloader


bot = commands.Bot(command_prefix='.')
client = discord.Client()


@bot.command()
async def test(ctx):
	await ctx.send("Look at you, hacker.")


@bot.command()
async def join(ctx):
	author = ctx.author
	voice_channel = await author.voice.channel.connect()
	voice_channel.play(discord.FFmpegPCMAudio("lookatyou.mp3"))


@bot.command()
async def leave(ctx):
	await ctx.channel.disconnect()


@bot.command()
async def search(ctx, *, content: downloader.query):
	await ctx.send(content)


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

bot.run("NzE1MjQ0NzMxMzczODQ2NTkw.Xs6jEA.FJERWcUBD9VXEWfW7KGKoNBjM7A")


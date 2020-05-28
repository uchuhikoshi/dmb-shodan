import discord

from discord.ext import commands


bot = commands.Bot(command_prefix='.')
client = discord.Client()

queue = {}

@bot.command(pass_context=True)
async def test(ctx):
	print("Excucuting test.")
	await ctx.send("Look at you, hacker.")

@bot.command(pass_context=True)
async def join(ctx):
	author = ctx.author
	voice_channel = await author.voice.channel.connect()
	# voice_channel.play(discord.FFmpegPCMAudio("lookatyou.mp3"))
	voice_channel.play(discord.FFmpegPCMAudio("https://upload.wikimedia.org/wikipedia/ru/transcoded/8/84/%D0%93%D0%BE%D0%BB%D0%BE%D1%81_SHODAN.ogg/%D0%93%D0%BE%D0%BB%D0%BE%D1%81_SHODAN.ogg.mp3"))

@bot.command(pass_context=True)
async def leave(ctx):
	author = ctx.author
	voice_channel = await author.voice.channel.close()

"""
@bot.command
async def search(ctx, url):
	server = ctx.message.server
	voice_channel = bot.voice_client_in(server)
	player = await voice_channel.create_ytdl_player(url, after: lambda: check_queue(server.id))

	if server.id in queue:
		queue[server.id].append(player)
	else:
		queue[server.id] = [player]

	await bot.say('')
"""
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


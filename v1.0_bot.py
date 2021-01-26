import discord
from discord.ext import commands, tasks
import os
from itertools import cycle

bot = commands.Bot(command_prefix = '.')

#cogs exception settings
ex_cogs = []

#status settings
status = cycle([".help", "Put on your mask!"])

#initiation
@bot.event
async def on_ready():
	change_status.start()
	print("Bot is ready!")

@tasks.loop(seconds = 15)
async def change_status():
	await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = next(status)))

#help command
bot.remove_command("help")
@bot.command()
async def help(ctx):
	help_em = discord.Embed(
		color = discord.Colour.blue())
	help_em.set_author(name = "Help Command", icon_url="https://drive.google.com/uc?export=download&id=1z6avV4IqkvJRvRl5eCu1LA_8WuyQL2eU")
	help_em.add_field(name = "Manual Request Daily Trend", value = "`.trend <n> <l> <c>` to show today's trends leaderboard \n> `<n>` = number of result (**num**, default value = `3`)\n> `<l>` = link search (**on/off**, default value = `off`)\n> `<c>` = country name/country iso code (**str**, default value = `indonesia`)\n> **! disclaimer :** please take note that this bot is using a __free API from google__, so there's a __limit of queries__ that can be requested daily. If not important, **please keep the link search value as off**", inline=False)
	help_em.add_field(name = "Automatic Daily Trend", value = "`.start_daily <c>` to enable automatic daily trend post\n> `<c>` = country name/country iso code (**str**, default value = `indonesia`)\n> **! disclaimer :** automatic update every mid-night (server time)\n`.stop_daily` to remove current automatic daily trend post", inline=False)
	help_em.add_field(name = "Server Ping Check", value = "`.ping` to check the current server latency", inline=False)
	help_em.set_footer(text= "Any technical issues? please drop a DM at my discord Gamaliel#0388")
	await ctx.send(embed=help_em)

#cogs
@bot.command()
async def load(ctx, extension):
	bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx, extension):
	bot.unload_extension(f'cogs.{extension}')

@bot.command()
async def reload(ctx, extension):
	bot.unload_extension(f'cogs.{extension}')
	bot.load_extension(f'cogs.{extension}')

#importing cogs
print("importing cogs...")
for filename in os.listdir('./cogs'):
	
	if filename.endswith(".py") and filename[:-3] not in ex_cogs:
		bot.load_extension(f'cogs.{filename[:-3]}')
print("all cogs imported!")

bot.run(os.environ['DISCORD_TOKEN'])

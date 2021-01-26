import discord
from discord.ext import commands

class test_ping(commands.Cog):

	# initial
	def __init__(self, client):
		self.client = client
		print("loading ping cogs...")

	# # event
	# @commands.Cog.listener()
	# async def on_ready(self):
	# 	print("ping cogs is loaded!")

	# command
	@commands.command()
	async def ping(self, ctx):
		ping_em = discord.Embed(
			description = f":green_circle: `{round(self.client.latency*1000)} ms`", 
			color= discord.Colour.blue())
		await ctx.send(embed=ping_em)

def setup(client):
	client.add_cog(test_ping(client))
	print("loaded ping cogs succesfully!")
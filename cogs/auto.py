import discord
from discord.ext import commands, tasks
import pandas as pd
from googlesearch import search
from datetime import datetime
from pytrends.request import TrendReq
import country_code_finder

def trending_searches(country, pytrends):
	country=country.lower()
	data = pytrends.trending_searches(country.replace(" ", "_"))
	return(data)

class auto(commands.Cog):
	# initial
	def __init__(self, client):
		self.client = client
		print("loading auto cogs...")

	@tasks.loop(minutes=1)
	async def automatic_daily_trend(self, channel_id, country):
		hour = datetime.now().strftime('%H%M')
		channel = self.client.get_channel(channel_id)
		if hour == "0000":
			#generate trending searches
			pytrends = TrendReq(hl='en-US')
			data = trending_searches(country, pytrends)

			#declare embed msg
			t = datetime.now()
			auto_em = discord.Embed(
				title = "<< Mas Trendy: Daily Trending Searches >>", 
				description = f"***Top Searches***, based on google search \n Country = **{country.title()}** \n Language Code = **{country_code_finder.country_to_iso(country).upper()}** \n Updated on: **{t.strftime('%a, %d %b %Y')}**",
				color = discord.Colour.blue()
				)
			auto_em.set_image(url="https://assets.stickpng.com/images/580b57fcd9996e24bc43c51f.png")
			auto_em.set_thumbnail(url="https://drive.google.com/uc?export=download&id=1z6avV4IqkvJRvRl5eCu1LA_8WuyQL2eU")
			auto_em.set_footer(text = "(This is Automatic-daily-update message)")

			for i in range(10):
				links = search(data.loc[i][0], num_results=5, lang=country_code_finder.country_to_iso(country))
				chained_link = ""
				link_counter = 0
				ex_searches = ["/search", "wikipedia.org", "instagram.com"]

				for link in links:
					if (all(ex_search not in link for ex_search in ex_searches) and link_counter <2):
						chained_link += f"Related link-{link_counter+1} \n {link} \n"
						link_counter += 1

				if not chained_link: #if there's no good link inserted to chained_link
					chained_link = "(there's no related link available)"

				auto_em.add_field(name = f"Top {i+1} : {data.loc[i][0]}", value = chained_link, inline = False)

			#push embed msg
			await channel.send(embed=auto_em)

	@automatic_daily_trend.before_loop
	async def before_automatic_daily_trend(self):
		await self.client.wait_until_ready()


	@commands.command()
	async def start_daily(self, ctx, country="indonesia"):
		channel = discord.utils.get(ctx.guild.channels, name="mas-trendy-daily") #harus pake strip namanya
		if channel is None:
			guild = ctx.message.guild
			await guild.create_text_channel("auto-hehe")
			channel = discord.utils.get(ctx.guild.channels, name="mas-trendy-daily")

		#iso code decoder
		if len(country) == 3 or len(country) == 2:
			country = country_code_finder.iso_to_country(country)

		self.automatic_daily_trend.start(channel.id, country)
		notif_auto_em = discord.Embed(
				title = "<< Mas Trendy: Daily Trending Searches >>", 
				description = f"Automatic daily update has been set. \n Country = `{country.title()}` \n Language Code = `{country_code_finder.country_to_iso(country).upper()}`",
				color = discord.Colour.blue()
				)
		notif_auto_em.set_thumbnail(url="https://drive.google.com/uc?export=download&id=1z6avV4IqkvJRvRl5eCu1LA_8WuyQL2eU")
		await channel.send(embed=notif_auto_em)

	@commands.command()
	async def stop_daily(self, ctx):
		self.automatic_daily_trend.cancel()

def setup(client):
	client.add_cog(auto(client))
	print("loaded auto cogs succesfully!")
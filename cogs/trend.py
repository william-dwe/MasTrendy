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

class trend(commands.Cog):

	# initial
	def __init__(self, client):
		self.client = client
		print("loading trend cogs...")

	@commands.command()
	async def trend(self, ctx, n_result=3, link_search="off", *, country="indonesia"):
		# await ctx.message.channel.purge(limit=1)
		if n_result > 10:
			await ctx.send("The maximal result is 10!")
		else: #result within limit
			t = datetime.now()
			
			if len(country) == 3 or len(country) == 2:
				country = country_code_finder.iso_to_country(country)
			#generate trending searches
			pytrends = TrendReq(hl='en-US')
			try:
				data = trending_searches(country, pytrends)

				#declare embed msg
				daily_em = discord.Embed(
					title = "<< Mas Trendy: Daily Trending Searches >>", 
					description = f"***Top Searches***, based on google search \n Country = `{country.title()}` \n Language Code = `{country_code_finder.country_to_iso(country).upper()}` \n Updated on: `{t.strftime('%a, %d %b %Y')}`",
					color = discord.Colour.blue()
					)
				daily_em.set_image(url="https://assets.stickpng.com/images/580b57fcd9996e24bc43c51f.png")
				daily_em.set_thumbnail(url="https://drive.google.com/uc?export=download&id=1z6avV4IqkvJRvRl5eCu1LA_8WuyQL2eU")
				daily_em.set_footer(icon_url = ctx.author.avatar_url, text = "Requested by " + ctx.author.name)

				#adding the result on embed msg's field
				for i in range(min(n_result, 10)):
					if link_search == "on":
						try:
							links = search(data.loc[i][0], num_results=3, lang=country_code_finder.country_to_iso(country))
						except:
							links = ["Daily link-search limit has been reached"]
						chained_link = ""
						link_counter = 0
						ex_searches = ["/search", "wikipedia.org", "instagram.com"]

						for link in links:
							if (all(ex_search not in link for ex_search in ex_searches) and link_counter <2):
								chained_link += f"Related link-{link_counter+1} \n {link} \n"
								link_counter += 1

						if not chained_link: #if there's no good link inserted to chained_link
							chained_link = "(there's no related link available)"
					elif link_search == "off":
						chained_link = "(link not listed by default)"

					daily_em.add_field(name = f"Top {i+1} : {data.loc[i][0]}", value = chained_link, inline = False)

				#push the result (embed msg)
				await ctx.send(embed=daily_em)
			except:
				error_em = discord.Embed(
					description = "Error: country not found / not listed!",
					color = discord.Colour.blue()
					)
				await ctx.send(embed=error_em)


def setup(client):
	client.add_cog(trend(client))
	print("loaded trend cogs succesfully!")
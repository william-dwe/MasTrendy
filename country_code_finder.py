import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

#scrapping
r = requests.get("https://countrycode.org/")
soup = bs(r.content, features = "html.parser")

tab = soup.find("table", attrs={"class":"table table-hover table-striped main-table"})
table_head = ["COUNTRY", "COUNTRY CODE", "ISO CODE", "POPULATION", "AREA", "GDP"]
table_rows = tab.tbody.find_all("tr")

df=[]
for row in table_rows:
    td = row.find_all("td")
    row = [tr.get_text() for tr in td]
    df.append(row)
data = pd.DataFrame(df, columns = table_head)

def country_to_iso(country):
	return (data[data["COUNTRY"] == country.title()]["ISO CODE"].iloc[0][:2].lower())

def iso_to_country(iso):
	if len(iso) == 3:
		return (data[data["ISO CODE"].str.contains(iso.upper())]["COUNTRY"].iloc[0])
	elif len(iso) == 2:
		return (data[data["ISO CODE"].str.startswith(iso.upper())]["COUNTRY"].iloc[0])
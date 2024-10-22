import urllib.request
import json

from Brewery import Brewery

def fetchBreweries():
    url = "https://api.openbrewerydb.org/breweries?per_page=20"
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        request = urllib.request.Request(url, headers=headers)

        data = urllib.request.urlopen(request).read()
        breweriesData = json.loads(data)
        breweries = []

        for data in breweriesData:
            brewery = Brewery(data)
            breweries.append(brewery)

        return breweries

    except urllib.error.URLError as e:
        print(f"Błąd połączenia z API: {e}")
        return []

breweriesList = fetchBreweries()

for brewery in breweriesList:
    print(brewery)
    print("-" * 40)
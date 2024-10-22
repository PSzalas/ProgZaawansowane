import urllib.request
import json
import argparse

from zad_7.Brewery import Brewery

def fetchBreweries(city=None):
    url = "https://api.openbrewerydb.org/breweries"

    if city:
        url += f"?by_city={city}&per_page=20"
    else:
        url += "?per_page=20"

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


parser = argparse.ArgumentParser(description='pobierz browary z Open Browary DB')
parser.add_argument('--city', type=str, help='Filtruj po nazwie miasta')

args = parser.parse_args()

breweriesList = fetchBreweries(city=args.city)

for brewery in breweriesList:
    print(brewery)
    print("-" * 40)

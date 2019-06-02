import pandas as pd


# retorna un DataFrame amb totes les ciutats amb un minim de poblacio
def get_cities_data(min_population):
    # parametres
    url_internet = 'https://github.com/jordi-petit/lp-graphbot-2019/blob/master/dades/worldcitiespop.csv.gz?raw=true'
    url = './worldcitiespop.csv'
    index = 'Index'
    country = 'Country'
    city = 'City'
    population = 'Population'
    lat = 'Latitude'
    lon = 'Longitude'

    # data = pd.read_csv(url, compression='gzip', usecols=[country, city, population, lat, lon])

    data = pd.read_csv(url, usecols=[country, city, population, lat, lon])
    data = data.loc[data[population] >= min_population]

    return data




class City:
    def __init__(self, country, city, population, lat, lon):
        self.country = country
        self.city = city
        self.population = population
        self.lat = lat
        self.lon = lon

    # retorna la tupla (lat, lon)
    def lat_lon(self):
        return self.lat, self.lon

    # retorna la tupla (lon, lat)
    def lon_lat(self):
        return self.lon, self.lat

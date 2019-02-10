import string
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
import folium
import operator


def maps():
    def color_creator(number):
        if number > 100:
            if number > 300:
                return 'black'
            return 'brown'
        if number < 20:
            if number < 10:
                return 'yellow'
            return 'orange'
        if number > 50:
            return 'blue'
        return 'green'

    def adress(city):
        geolocator = Nominatim(user_agent="specify_your_app_name")
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
        try:
            for point in [city]:
                location = geolocator.geocode(point)
                return (location.latitude, location.longitude)
        except:
            return False

    f = open('locations.list')
    year = input()
    lines1 = []
    lines = []
    counter = 0
    for line in f:
        if year in line:
            if '}' in line:
                pass
            else:
                lines1.append(line.split(year))
                lines.append(lines1[counter][len(lines1[counter]) - 1])
                counter += 1
    for i in range(0, len(lines)):
        lines[i] = lines[i].split(',')
    for i in range(0, len(lines)):
        if lines[i][-1].endswith(')'):
            lines[i][-1] = lines[i][-1][:rindex('(')]
        for j in range(0, len(lines[i])):
            lines[i][j] = lines[i][j].replace('\t', '')
            lines[i][j] = lines[i][j].replace('\n', '')
            if '(' in lines[i][j]:
                index = lines[i][j].find('(')
                lines[i][j] = lines[i][j][:index]
            if ')' in lines[i][j]:
                lines[i][j] = lines[i][j].replace(')', '')
            if lines[i][j].startswith(' '):
                lines[i][j] = lines[i][j][1:]

    countries_dict = {}
    countries_dict2 = {}

    for i in range(0, len(lines)):
        country = lines[i][-1]
        if country not in countries_dict:
            countries_dict[country] = 0
        countries_dict[country] += 1

    for i in range(0, len(lines)):
        country = lines[i][0]
        if country not in countries_dict2:
            countries_dict2[country] = 0
        countries_dict2[country] += 1

    popular_cities = sorted(countries_dict2.items(), key=operator.itemgetter(1), reverse=True)
    map = folium.Map(location=[48.314775, 25.082925], zoom_start=3)

    fe = folium.FeatureGroup(name="Most popular cities")
    counter2 = 0
    for i in range(0, len(popular_cities)):
        coord = adress(popular_cities[i][0])
        if coord:
            lt = coord[0]
            ln = coord[1]
            number = popular_cities[i][1]
            fe.add_child(folium.CircleMarker(location=[lt, ln], radius=10, popup=str(number),
                                             fill_color=color_creator(number), fill_opacity=0.7))
            counter2 += 1
            if counter2 == 50:
                break

    map.add_child(fe)
    f_pp = folium.FeatureGroup(name="Population")
    f_pp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(), style_function=lambda x: {'fillColor': 'green'
                                                                                                                       if x['properties']['POP2005'] < 10000000
                                                                                                                       else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
                                                                                                                       else 'red'}))
    map.add_child(f_pp)
    locations_dict = {}
    for countries in countries_dict:
        location = adress(countries)
        if location:
            locations_dict[location] = countries_dict[countries]

    fg = folium.FeatureGroup(name="Countries")
    for locations in locations_dict:
        lt = locations[0]
        ln = locations[1]
        number = locations_dict[locations]
        fg.add_child(folium.CircleMarker(location=[lt, ln], radius=10, popup=str(
            number), fill_color=color_creator(number), fill_opacity=0.7))
    map.add_child(fg)
    map.add_child(folium.LayerControl())
    map.save('Map.html')


if __name__ == '__main__':
    maps()

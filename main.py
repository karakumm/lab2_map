'''
Module for creating a map from data
'''
import folium
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderUnavailable
from geopy.distance import geodesic

def read_data(path):
    '''
    Reads data and returns list of films
    '''
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    result = []

    for line in lines:
        line = line.strip().split('\t')
        line = list(filter(lambda a: a != '', line))

        try:
            new_line = line[0].split('{')
        except: IndexError
        if len(new_line) == 2:
            new_line.remove(new_line[1])

        try:
            new_line.append(line[1])
        except: IndexError

        result.append(new_line)

    new_list = [list(el_) for el_ in set(tuple(lst) for lst in result)]

    films_lst = []

    for film in new_list:
        film_1 = film[0].split('(')

        try:
            film_1.append(film[1])
            film_1[1] = film_1[1][:4]

            if (len(film_1) >= 4) or (film_1[1] == '????'):
                del film_1

            films_lst.append(film_1)
        except: IndexError

    return films_lst
# print(read_data('locations.list'))


def filter_year(films):
    '''
    Returns films only of the year of user's input
    '''
    film_year = []
    for film in films:
        if film[1] == year:
            film_year.append(film)

    return film_year[:1000]

# print(films)


def get_coords(films):
    '''
    Gets latitude and longtitude of addresses, where the films were directed
    '''
    films_lst = []
    try:
        for film in films:
            try:
                location = geolocator.geocode(film[2])
                film.append(location.latitude)
                film.append(location.longitude)

                films_lst.append(film)
            except: GeocoderUnavailable
    except: AttributeError
    return films_lst
# print(get_coords(films))


def find_distance(films_lst):
    '''
    Finds the distance from user location to location the film was directed
    '''
    user_coords = tuple((map(float, coordinates.split(','))))
    for film in films_lst:
        film_coords = tuple(film[-2:])
        dist = geopy.distance.geodesic(user_coords, film_coords).km
        film.append(dist)
    return films_lst
# print(find_distance(get_coords(films)))


def find_nearest(lst_distances):
    '''
    Find 10 films with the nearest location to the user's one
    '''
    sorted_lst = sorted(lst_distances, key=lambda x: x[-1])
    locations = sorted_lst[:11]
    return locations
# print(find_nearest(with_distances))


def create_map(film_locations):
    '''
    Creates the map with three layers: user's location, my hometown(Kalush)\
        and films' locations
    '''

    latitude = float(coordinates.split(',')[0])
    longtitude = float(coordinates.split(',')[1])
    loc = [latitude, longtitude]
    map = folium.Map(location= loc,
                    zoom_start=100)

    fg1 = folium.FeatureGroup(name="Your location")
    fg1.add_child(folium.Marker(location=loc,
                            popup="You are here!",
                            icon=folium.Icon()))
    map.add_child(fg1)

    mee  = [49.043005102937286, 24.36109362474663]

    fg2 = folium.FeatureGroup(name="My location")
    fg2.add_child(folium.Marker(location=mee,
                            popup="And I am here!",
                            icon=folium.Icon()))
    map.add_child(fg2)

    fg3 = folium.FeatureGroup(name="Nearest film's locations")
    for loc in film_locations:
        fg3.add_child(folium.Marker(location=[loc[-3], loc[-2]],
                            popup=loc[0],
                            icon=folium.Icon()))
        map.add_child(fg3)

    map.add_child(folium.LayerControl())
    map.save('map.html')


if __name__ == "__main__":

    geolocator = Nominatim(user_agent="karakum")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    year = input("Please enter the film year: ")
    coordinates = input("Please enter your coordinates: ")


    films = filter_year(read_data('locations.list'))
    with_distances = find_distance(get_coords(films))

    create_map(find_nearest(with_distances))

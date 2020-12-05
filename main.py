"""
* Carol Lei & Kenny "Ackerson" Le 
* 11/19/20
* Twitter Trends
* Description: HCDE 310 Final Project
"""

import json
import tweepy
import googlemaps
import urllib.error
import urllib.parse
import urllib.request
from flask import Flask, render_template, request
import math

app = Flask(__name__)

with open("API_Keys.json") as json_file:
    file = json.load(json_file)
    _gmaps_key = file["Google Maps API"]
    _twitter_key = file["Twitter API key"]
    _twitter_secret = file["Twitter secret"]
    _twitter_beartoken = file["Twitter bear_token"]
    gmaps = googlemaps.Client(key=_gmaps_key)

    # Authenciating with tweepy Get Trends at Location
    auth = tweepy.OAuthHandler(_twitter_key, _twitter_secret)
    api = tweepy.API(auth)


def safe_get(url):
    try:
        return urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        print("The server couldn't fulfill the request.")
        print("Error code: ", e.code)
    except urllib.error.URLError as e:
        print("We failed to reach a server")
        print("Reason: ", e.reason)
    return None


# https://developers.google.com/maps/documentation/embed/get-started#forming_the_url
def gmaps_rest(query, mode="place"):
    """
    Takes a location and returns a HTTP address to embed an interactive map from Google Maps
    """
    # https://www.google.com/maps/embed/v1/MODE?key=YOUR_API_KEY&parameters
    base_url = "https://www.google.com/maps/embed/v1"
    key = f"key={_gmaps_key}"
    q_dict = {"q": query, "zoom": "7"}
    # q = query_encode(urllib.parse.urlencode(q_dict))
    q = urllib.parse.urlencode(q_dict).replace("%2C+", ",")
    url = f"{base_url}/{mode}?{key}&{q}"
    return url


def get_lat_long(location):
    """
    Takes a location and returns the latitude and longitude coordinates
    """
    geo_info = gmaps.geocode(location)
    coords = geo_info[0]["geometry"]["location"]
    return coords["lat"], coords["lng"]


def get_location(coordinates):
    """
    Takes a latitude and longitude coordinate and returns a list of addresses at that location
    """
    location_info = gmaps.reverse_geocode(latlng=coordinates)
    location_list = list()
    for location in location_info:
        if "locality" in location["types"]:
            return location["formatted_address"]
        # location_list.append(location["formatted_address"])
    # return location_list


# Implement a way to determine if there's more cities on one side than the other
def get_center(coords_list):
    # lat_sum = 0
    # long_sum = 0
    #
    # for coords in coords_list:
    #     lat_sum += coords[0]
    #     long_sum += coords[1]
    #
    # return lat_sum / len(coords_list), long_sum / len(coords_list)
    # "https://stackoverflow.com/questions/6671183/calculate-the-center-point-of-multiple-latitude-longitude-coordinate-pairs"
    x = 0.0
    y = 0.0
    z = 0.0

    for coord in coords_list:
        lat = math.radians(coord[0])
        long = math.radians(coord[1])

        x += math.cos(lat) * math.cos(long)
        y += math.cos(lat) * math.sin(long)
        z += math.sin(lat)

    x = x / len(coords_list)
    y = y / len(coords_list)
    z = z / len(coords_list)

    center_long = math.atan2(y, x)
    center_hyp = math.sqrt(x * x + y * y)
    center_lat = math.atan2(z, center_hyp)

    return math.degrees(center_lat), math.degrees(center_long)


def get_location_trends(lat, long):
    """
    Takes a latitude and longitude coordinate and returns a list of trends near that location
    """
    closest_loc = api.trends_closest(lat, long)
    trends = api.trends_place(closest_loc[0]['woeid'])

    trend_names_vol = {}
    for trend in trends[0]['trends']:
        if trend['tweet_volume'] is not None:
            trend_names_vol[trend['name']] = trend['tweet_volume']

    return trend_names_vol


def get_trends(count = 5):
    """
    Returns all available trends
    """
    available_loc = api.trends_available()


@app.route("/")
def display_map():
    url = gmaps_rest("Sapporo")
    cities = ["Seattle", "Portland", "Los Angeles", "San Francisco", "Las Vegas", "Salt Lake City", "New York City"]
    # cities = ["Seattle", "Los Angeles", "New York City"]
    coordinates = [get_lat_long(city) for city in cities]
    coordinates.append(get_center(coordinates))
    print(get_center(coordinates))
    return render_template("template.html", API_Key=_gmaps_key,
                           coords_list=coordinates, center=(39.8283, -98.5759))
    # return render_template("template.html", API_Key=_gmaps_key)
    # return render_template("template.html", url=url)


def main():
    print("Hello World")
    print(get_location_trends(*get_lat_long("United States")))
    # cities = ["Seattle", "Portland", "Los Angeles", "San Francisco", "Las Vegas", "Salt Lake City",
    #           "New York City"]
    cities = ["Seattle", "Los Angeles", "New York City"]
    coordinates = [get_lat_long(city) for city in cities]
    print(f"Coordinates List: {coordinates}")
    print(get_center(coordinates))


if __name__ == "__main__":
    main()
    app.run(port=3000, debug=True)

import json
import googlemaps
import urllib
"""
* Carol Lei & Kenny "Ackerson" Le 
* 11/19/20
* Twitter Trends
* Description: HCDE 310 Final Project
"""

with open("API_Keys.json") as json_file:
    file = json.load(json_file)
    _gmaps_key = file["Google Maps API"]
    gmaps = googlemaps.Client(key=_gmaps_key)


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
def gmaps_rest(mode="place", params={}):
    base_url = "https://www.google.com/maps/embed/v1/"
    key = f"key={_gmaps_key}"


def main():
    print("Hello World")


if __name__ == "__main__":
    main()

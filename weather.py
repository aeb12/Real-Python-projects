import argparse, json, sys
from configparser import ConfigParser
from urllib import error, parse, request
from pprint import pp

BASE_WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
PADDING = 20
REVERSE = "\033[;7m"
RESET = "\033[0m"

def read_user_cli_args():
    parser = argparse.ArgumentParser(
        description="gets weather and temperature information for a city"
    )
    parser.add_argument(
        "city", nargs="+", type=str, help="Enter the city name"
    )
    parser.add_argument(
        "-i",
        "--imperial",
        action="store_true",
        help="display the temperature in imperial untits"
        
    )
    return parser.parse_args()

def _get_api_key():
    config = ConfigParser()
    config.read("secrets.ini")
    return config["openweather"] ["api_key"] 

def build_weather_query(city_imput, imperial=False):
    api_key = _get_api_key()
    city_name = " ".join(city_imput)
    url_encoded_city_name = parse.quote_plus(city_name)
    units = 'imperial' if imperial else 'metric'
    url = (
        f"{BASE_WEATHER_API_URL}?q={url_encoded_city_name}"
        f"&units={units}&appid={api_key}"
    )
    return url

def get_weather_data(query_url):
    try:
        response = request.urlopen(query_url)
    except error.HTTPError as http_error:
        if http_error.code == 401:
            sys.exit("Access denied. Check your API key.")
        elif http_error.code == 404:  # 404 - Not Found
            sys.exit("Can't find weather data for this city.")
        else:
            sys.exit("Can't find weather data for this city.")
    data = response.read()
    try:
        return json.loads(data)
    except json.json.JSONDecodeError:
        sys.exit("Couldn't read the server response.")

def display_weather_info(weather_data, imperial=False):
    city = weather_data["name"]
    weather_description = weather_data["weather"][0]["description"]
    temperature = weather_data["main"]["temp"]

    print(f"{REVERSE}{city:^{PADDING}}{RESET}", end="")
    print(f"\t{weather_description.capitalize():^{PADDING}}", end=" ")
    print(f"({temperature}°{'F' if imperial else 'C'})")
    
if __name__ == "__main__":
    user_args=read_user_cli_args()
    #print(user_args.city, user_args.imperial)
    query_url = build_weather_query(user_args.city, user_args.imperial)
    weather_data = get_weather_data(query_url)
    #pp(weather_data)
    display_weather_info(weather_data, user_args.imperial)

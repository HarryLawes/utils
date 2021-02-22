# pylint: disable=missing-docstring

import sys
import requests

BASE_URI = "https://www.metaweather.com"


def search_city(query):
    url = BASE_URI + '/api/location/search/?query=' + query
    response = requests.get(url).json()
    if not response:
        city_details = None
    elif len(response) > 1:
        for index, name in enumerate(response):
            print(f'{index+1} - {name["title"]}')
        number = int(input('Choose which city you meant\n> '))
        city_details = response[number-1]
    else:
        city_details = response[0]
    return city_details


def weather_forecast(woeid):
    woeid = str(woeid)
    url = BASE_URI + '/api/location/' + woeid
    response = requests.get(url).json()
    return response['consolidated_weather']


def main():
    query = input("City?\n> ")
    city = search_city(query)
    if city is None:
        print('Sorry the city has not been recognised. Please try again')
    else:
        woeid = city['woeid']
        weather = weather_forecast(woeid)
        print(f"Here\'s the weather in {city['title'].title()}")
        for i in range(5):
            day = weather[i]
            print(f'''{day["applicable_date"]}:
            {day["weather_state_name"]} {round(day["max_temp"], 1)}°C''')


if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(0)

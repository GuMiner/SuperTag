from adafruit_datetime import datetime
import adafruit_imageload
import displayio
import json
import time
from secrets import secrets

import const
import conversion
import display_util
import network

# Weather assets
BACKGROUND_BMP = "/bmps/weather_bg.bmp"
ICONS_LARGE_FILE = "/bmps/weather_icons_70px.bmp"
ICONS_SMALL_FILE = "/bmps/weather_icons_20px.bmp"

# Map NOAA short forecasts to icons. These icon maps are indexed L->R, T->B
def get_weather_icon(short_forecast):
    lowercase_forecast = short_forecast.lower()
    if 'snow' in lowercase_forecast:
        return 7
    
    if 'thunder' in lowercase_forecast:
        return 6
    
    if 'rain' in lowercase_forecast or 'shower' in lowercase_forecast:
        if 'light' in lowercase_forecast or 'slight' in lowercase_forecast:
            return 5
        return 4
    
    if 'cloudy' in lowercase_forecast:
        if 'mostly' in lowercase_forecast:
            return 3
        if 'partly' in lowercase_forecast:
            return 2
    
    if 'sunny' in lowercase_forecast:
        if 'partly' in lowercase_forecast or 'mostly' in lowercase_forecast:
            return 1

    return 0 # Sunny

def get_weekday(time):
    weekday = datetime.fromisoformat(time).weekday() - 1
    return const.DAYS[weekday]

# Use the NOAA API to get the weather https://www.weather.gov/documentation/services-web-api
def get_forecast(magtag):
    # Location determined using https://api.weather.gov/points/LAT,LONG
    magtag.url = "https://api.weather.gov/gridpoints/{}/forecast".format(
        secrets["location"])
    magtag.json_path = None

    def parse_result(raw_data):
        result = json.loads(raw_data)
        return result["properties"]

    if const.SIMULATE_NETWORK:
        return json.loads(const.SIMULATED_RESPONSE)
    return network.fetch_with_retries(magtag, parse_result)


# Make a single future forecast info banner group.
def make_mini_banner(icons_small_bmp, icons_small_pal, x=0, y=0):
    day_of_week = display_util.make_label("DAY", (0, 10))

    image_offset = 20
    icon = displayio.TileGrid(
        icons_small_bmp,
        pixel_shader=icons_small_pal,
        x=image_offset, y=0,
        width=1, height=1,
        tile_width=20, tile_height=20)

    day_temp = display_util.make_label("100F -> 100F", (45, 10))

    return display_util.make_group([day_of_week, icon, day_temp], x, y)


def update_banner(banner, day_forecast, night_forecast):
    """Update supplied forecast banner with supplied data."""
    banner[0].text = get_weekday(night_forecast["endTime"])[:3]
    banner[1][0] = get_weather_icon(day_forecast["shortForecast"])
    banner[2].text = f"{day_forecast['temperature']}F->{night_forecast['temperature']}F"
    
    
def run(magtag):
    magtag.graphics.set_background(BACKGROUND_BMP)
    time.sleep(magtag.display.time_to_refresh)

    icons_large_bmp, icons_large_pal = adafruit_imageload.load(ICONS_LARGE_FILE)
    icons_small_bmp, icons_small_pal = adafruit_imageload.load(ICONS_SMALL_FILE)
    
    # == UI ==
    city_name = display_util.make_label(secrets["city"], (15, 19))
    today_date = display_util.make_label("?" * 30, (15, 32))
    
    today_icon = displayio.TileGrid(
        icons_large_bmp,
        pixel_shader=icons_small_pal,
        x=10, y=40,
        width=1, height=1,
        tile_width=70, tile_height=70)
    
    # Weather
    today_day_temp = display_util.make_label("100 F", (130, 64))
    today_night_temp = display_util.make_label("100 F", (160, 64))
    
    today_humidity = display_util.make_label("100%", (90, 70))
    today_wind = display_util.make_label("7 to 10 mph", (110, 85))
    
    today_details = display_util.make_label("Partly Cloudy -> Partly Cloudy", (90, 115))
    
    today_banner = displayio.Group(max_size=9)
    today_banner.append(today_date)
    today_banner.append(city_name)
    today_banner.append(today_icon)
    today_banner.append(today_day_temp)
    today_banner.append(today_night_temp)
    today_banner.append(today_humidity)
    today_banner.append(today_wind)
    today_banner.append(today_details)
    
    future_banners = [
        make_mini_banner(icons_small_bmp, icons_small_pal, x=195, y=18),
        make_mini_banner(icons_small_bmp, icons_small_pal, x=195, y=39),
        make_mini_banner(icons_small_bmp, icons_small_pal, x=195, y=60),
        make_mini_banner(icons_small_bmp, icons_small_pal, x=195, y=81),
        make_mini_banner(icons_small_bmp, icons_small_pal, x=195, y=102),
    ]

    magtag.splash.append(today_banner)
    for future_banner in future_banners:
        magtag.splash.append(future_banner)
    
    print("Fetching forecast...")
    forecast_data = get_forecast(magtag)
    
    print("Updating...")
    # Perform custom updates for the current day
    forecast_day = forecast_data["periods"][0]
    forecast_night = forecast_data["periods"][1]
    date_weekday = datetime.fromisoformat(forecast_night["endTime"])  # Hack to account for the time zone 
    date = datetime.fromisoformat(forecast_night["startTime"])

    today_date.text = "{} {}, {} ({})".format(
        const.MONTHS[date.month - 1], date.day, date.year, const.DAYS[date_weekday.weekday() - 1])
    today_icon[0] = get_weather_icon(forecast_day["shortForecast"])
    today_day_temp.text = f"{forecast_day['temperature']}F"
    today_night_temp.text = f"{forecast_night['temperature']}F"
    today_humidity.text = f"{forecast_day['relativeHumidity']['value']}%"
    today_wind.text = forecast_day["windSpeed"]
    today_details.text = f"{forecast_day['shortForecast']} -> {forecast_night['shortForecast']}"

    # Update all the future days in the right sidebar
    for i in range(len(future_banners)):
        # i + 1 to skip today + tonight
        day = (i + 1) * 2
        night = (i + 1) * 2 + 1
        update_banner(future_banners[i], forecast_data["periods"][day], forecast_data["periods"][night])
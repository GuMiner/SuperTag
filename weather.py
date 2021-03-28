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
ICON_MAP = ("01", "02", "03", "04", "09", "10", "11", "13", "50")


def get_latlon(magtag):
    """Use the Forecast5 API to determine lat/lon for given city."""
    magtag.url = "https://api.openweathermap.org/data/2.5/forecast?q={}&appid={}".format(
        secrets["openweather_location"], secrets["openweather_token"])
    magtag.json_path = ['city']
    def parse_result(result):
        return result["coord"]["lat"], result["coord"]["lon"]
    
    if const.SIMULATE_NETWORK:
        return '47.6129', '-122.2044'
    return network.fetch_with_retries(magtag, parse_result)

def get_forecast(magtag, location):
    """Use OneCall API to fetch forecast and timezone data."""
    magtag.url = "https://api.openweathermap.org/data/2.5/onecall?exclude=minutely,hourly,alerts&lat={}&lon={}&appid={}".format(
        location[0], location[1], secrets["openweather_token"])
    magtag.json_path = None 
    def parse_result(raw_data):
        result = json.loads(raw_data)
        return result["daily"], result["current"]["dt"], result["timezone_offset"]    

    if const.SIMULATE_NETWORK:
        simulated_daily = json.loads('[{}]'.format(
            (('{"sunset": 1613871593, "sunrise": 1613833526, "dt": 1613851200, "wind_speed": 4.57, "humidity": 100, ' + 
              '"weather":[{ "icon": "10d" }], "temp": { "night": 278.56, "day": 280.88, "morn": 274.92 }},') * 7)).strip(','))
        return simulated_daily, 1613431662, -28800 
    return network.fetch_with_retries(magtag, parse_result)

def make_banner(icons_small_bmp, icons_small_pal, x=0, y=0):
    """Make a single future forecast info banner group."""
    day_of_week = display_util.make_label("DAY", (0, 10))
    day_temp = display_util.make_label("+100F", (50, 10))

    icon = displayio.TileGrid(
        icons_small_bmp,
        pixel_shader=icons_small_pal,
        x=25, y=0,
        width=1, height=1,
        tile_width=20, tile_height=20)

    return display_util.make_group([day_of_week, icon, day_temp], x, y)


def temperature_text(tempK):
    if const.METRIC:
        return "{:3.0f}C".format(conversion.kelvin_to_celcius(tempK))
    else:
        return "{:3.0f}F".format(conversion.kelvin_to_fahrenheit(tempK))


def wind_text(speedms):
    if const.METRIC:
        return "{:3.0f}m/s".format(speedms)
    else:
        return "{:3.0f}mph".format(conversion.meters_per_second_to_miles_per_hour(speedms))


def update_banner(banner, data):
    """Update supplied forecast banner with supplied data."""
    banner[0].text = const.DAYS[time.localtime(data["dt"]).tm_wday][:3].upper() # day_of_week
    banner[1][0] = ICON_MAP.index(data["weather"][0]["icon"][:2]) # icon
    banner[2].text = temperature_text(data["temp"]["day"]) # day_temp
    
    
def run(magtag):
    magtag.graphics.set_background(BACKGROUND_BMP)
    time.sleep(magtag.display.time_to_refresh)

    icons_large_bmp, icons_large_pal = adafruit_imageload.load(ICONS_LARGE_FILE)
    icons_small_bmp, icons_small_pal = adafruit_imageload.load(ICONS_SMALL_FILE)
    
    # == UI ==
    city_name = display_util.make_label(secrets["openweather_location"], (15, 19))
    today_date = display_util.make_label("?" * 30, (15, 32))
    
    today_icon = displayio.TileGrid(
        icons_large_bmp,
        pixel_shader=icons_small_pal,
        x=10, y=40,
        width=1, height=1,
        tile_width=70, tile_height=70)
    
    # Weather
    today_morn_temp = display_util.make_label("+100F", (110, 64))
    today_day_temp = display_util.make_label("+100F", (139, 64))
    today_night_temp = display_util.make_label("+100F", (170, 64))
    
    today_humidity = display_util.make_label("100%", (120, 85))
    today_wind = display_util.make_label("99m/s", (157, 85))
    
    today_sunrise = display_util.make_label("12:00 PM", (130, 104))
    today_sunset = display_util.make_label("12:00 PM", (130, 117))
    
    today_banner = displayio.Group(max_size=10)
    today_banner.append(today_date)
    today_banner.append(city_name)
    today_banner.append(today_icon)
    today_banner.append(today_morn_temp)
    today_banner.append(today_day_temp)
    today_banner.append(today_night_temp)
    today_banner.append(today_humidity)
    today_banner.append(today_wind)
    today_banner.append(today_sunrise)
    today_banner.append(today_sunset)
    
    future_banners = [
        make_banner(icons_small_bmp, icons_small_pal, x=210, y=18),
        make_banner(icons_small_bmp, icons_small_pal, x=210, y=39),
        make_banner(icons_small_bmp, icons_small_pal, x=210, y=60),
        make_banner(icons_small_bmp, icons_small_pal, x=210, y=81),
        make_banner(icons_small_bmp, icons_small_pal, x=210, y=102),
    ]

    magtag.splash.append(today_banner)
    for future_banner in future_banners:
        magtag.splash.append(future_banner)
    
    print("Getting Lat/Lon...")
    latlon = get_latlon(magtag)
    print('Location: {}'.format(latlon))
    
    print("Fetching forecast...")
    forecast_data, utc_time, local_tz_offset = get_forecast(magtag, latlon)
    
    print("Updating...")
    date = time.localtime(forecast_data[0]["dt"])
    sunrise = time.localtime(forecast_data[0]["sunrise"] + local_tz_offset)
    sunset = time.localtime(forecast_data[0]["sunset"] + local_tz_offset)

    today_date.text = "{} {}, {} ({})".format(
        const.MONTHS[date.tm_mon - 1], date.tm_mday, date.tm_year, const.DAYS[date.tm_wday])
    today_icon[0] = ICON_MAP.index(forecast_data[0]["weather"][0]["icon"][:2])
    today_morn_temp.text = temperature_text(forecast_data[0]["temp"]["morn"])
    today_day_temp.text = temperature_text(forecast_data[0]["temp"]["day"])
    today_night_temp.text = temperature_text(forecast_data[0]["temp"]["night"])
    today_humidity.text = "{:3d}%".format(forecast_data[0]["humidity"])
    today_wind.text = wind_text(forecast_data[0]["wind_speed"])
    today_sunrise.text = "{:2d}:{:02d} AM".format(sunrise.tm_hour, sunrise.tm_min)
    today_sunset.text = "{:2d}:{:02d} PM".format(sunset.tm_hour - 12, sunset.tm_min)

    for day, forecast in enumerate(forecast_data[1:6]):
        update_banner(future_banners[day], forecast)
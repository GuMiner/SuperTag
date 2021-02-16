import alarm
import board
import displayio
import gc
import json
import time
import terminalio
import adafruit_imageload
from adafruit_display_text import label
from adafruit_magtag.magtag import MagTag
from secrets import secrets

# Free space at startup.
def print_free_mem():
    print('Free memory (kB): {}'.format(gc.mem_free() / 1024))
print_free_mem()

# Must be set earlier on before something else (unknown) grabs the pin.
# BUTTON_A/Time alarm -- no-cycle-reset. BUTTON_B -- cycle the display on reset.
pin_alarm_first_button = alarm.pin.PinAlarm(pin=board.BUTTON_A, value=False, pull=True)
pin_alarm_second_button = alarm.pin.PinAlarm(pin=board.BUTTON_B, value=False, pull=True)

# alarm.wake_alarm holds an equivalent alarm for what waked the device.
cycle_display = hasattr(alarm.wake_alarm, 'pin') and alarm.wake_alarm.pin == board.BUTTON_B
display_weather = True # False -- financials

if alarm.sleep_memory:
    display_weather = alarm.sleep_memory[0]

print('Cycle display: {}. Read saved settings {}'.format(cycle_display, alarm.sleep_memory == True)) # is True "is"

# --| USER CONFIG |--------------------------
METRIC = False  # set to True for metric units
SIMULATE_NETWORK = False

# -------------------------------------------

# ----------------------------
# Define various assets
# ----------------------------
BACKGROUND_BMP = "/bmps/weather_bg.bmp"
ICONS_LARGE_FILE = "/bmps/weather_icons_70px.bmp"
ICONS_SMALL_FILE = "/bmps/weather_icons_20px.bmp"
ICON_MAP = ("01", "02", "03", "04", "09", "10", "11", "13", "50")
DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
MONTHS = (
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
) 
magtag = MagTag()
print('Battery Voltage: {}'.format(magtag.peripherals.battery))

magtag.peripherals.neopixel_disable = True
magtag.peripherals.speaker_disable = True
print('Neopixels disabled? {}'.format(magtag.peripherals.neopixel_disable))
print('Speaker disabled? {}'.format(magtag.peripherals.speaker_disable))

# ----------------------------
# Backgrounnd bitmap
# ----------------------------
magtag.graphics.set_background(BACKGROUND_BMP)

# ----------------------------
# Weather icons sprite sheet
# ----------------------------
icons_large_bmp, icons_large_pal = adafruit_imageload.load(ICONS_LARGE_FILE)
icons_small_bmp, icons_small_pal = adafruit_imageload.load(ICONS_SMALL_FILE)

# /////////////////////////////////////////////////////////////////////////

def fetch_with_retries(action):
    succeeded = False
    while not succeeded:
        try:
            raw_data = magtag.fetch()
            return action(raw_data)
        except Exception as e:
            print ('Sleeping before retrying: {}'.format(str(e)))
            magtag.enter_light_sleep(5.0)

def get_latlon():
    """Use the Forecast5 API to determine lat/lon for given city."""
    magtag.url = "https://api.openweathermap.org/data/2.5/forecast?q={}&appid={}".format(
        secrets["openweather_location"], secrets["openweather_token"])
    magtag.json_path = ['city']
    def parse_result(result):
        return result["coord"]["lat"], result["coord"]["lon"]
    
    if SIMULATE_NETWORK:
        return '47.6129', '-122.2044'
    return fetch_with_retries(parse_result)

def get_forecast(location):
    """Use OneCall API to fetch forecast and timezone data."""
    magtag.url = "https://api.openweathermap.org/data/2.5/onecall?exclude=minutely,hourly,alerts&lat={}&lon={}&appid={}".format(
        location[0], location[1], secrets["openweather_token"])
    magtag.json_path = None 
    def parse_result(raw_data):
        result = json.loads(raw_data)
        return result["daily"], result["current"]["dt"], result["timezone_offset"]    

    if SIMULATE_NETWORK:
        simulated_daily = json.loads('[{}]'.format(
            (('{"sunset": 1613871593, "sunrise": 1613833526, "dt": 1613851200, "wind_speed": 2.57, "humidity": 42, ' + 
              '"weather":[{ "icon": "10d" }], "temp": { "night": 278.56, "day": 280.88, "morn": 274.92 }},') * 7)).strip(','))
        return simulated_daily, 1613431662, -28800 
    return fetch_with_retries(parse_result)

def make_banner(x=0, y=0):
    """Make a single future forecast info banner group."""
    day_of_week = label.Label(terminalio.FONT, text="DAY", color=0x000000)
    day_of_week.anchor_point = (0, 0.5)
    day_of_week.anchored_position = (0, 10)

    icon = displayio.TileGrid(
        icons_small_bmp,
        pixel_shader=icons_small_pal,
        x=25,
        y=0,
        width=1,
        height=1,
        tile_width=20,
        tile_height=20,
    )

    day_temp = label.Label(terminalio.FONT, text="+100F", color=0x000000)
    day_temp.anchor_point = (0, 0.5)
    day_temp.anchored_position = (50, 10)

    group = displayio.Group(max_size=3, x=x, y=y)
    group.append(day_of_week)
    group.append(icon)
    group.append(day_temp)

    return group


def temperature_text(tempK):
    if METRIC:
        return "{:3.0f}C".format(tempK - 273.15)
    else:
        return "{:3.0f}F".format(32.0 + 1.8 * (tempK - 273.15))


def wind_text(speedms):
    if METRIC:
        return "{:3.0f}m/s".format(speedms)
    else:
        return "{:3.0f}mph".format(2.23694 * speedms)


def update_banner(banner, data):
    """Update supplied forecast banner with supplied data."""
    banner[0].text = DAYS[time.localtime(data["dt"]).tm_wday][:3].upper()
    banner[1][0] = ICON_MAP.index(data["weather"][0]["icon"][:2])
    banner[2].text = temperature_text(data["temp"]["day"])


def update_today(data, tz_offset=0):
    """Update today info banner."""
    date = time.localtime(data["dt"])
    sunrise = time.localtime(data["sunrise"] + tz_offset)
    sunset = time.localtime(data["sunset"] + tz_offset)

    today_date.text = "{} {} {}, {}".format(
        DAYS[date.tm_wday].upper(),
        MONTHS[date.tm_mon - 1].upper(),
        date.tm_mday,
        date.tm_year,
    )
    today_icon[0] = ICON_MAP.index(data["weather"][0]["icon"][:2])
    today_morn_temp.text = temperature_text(data["temp"]["morn"])
    today_day_temp.text = temperature_text(data["temp"]["day"])
    today_night_temp.text = temperature_text(data["temp"]["night"])
    today_humidity.text = "{:3d}%".format(data["humidity"])
    today_wind.text = wind_text(data["wind_speed"])
    today_sunrise.text = "{:2d}:{:02d} AM".format(sunrise.tm_hour, sunrise.tm_min)
    today_sunset.text = "{:2d}:{:02d} PM".format(sunset.tm_hour - 12, sunset.tm_min)


def sleep_until_button_1():
    '''Does what it says, but it also awakes after 1 day too'''
    alarm.sleep_memory[0] = display_weather
    
    time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 3600 * 24)
    
    print("Sleeping for 1 day or until the leftmost button is pressed")
    alarm.exit_and_deep_sleep_until_alarms(time_alarm, pin_alarm_first_button, pin_alarm_second_button)


# ===========
# U I
# ===========
today_date = label.Label(terminalio.FONT, text="?" * 30, color=0x000000)
today_date.anchor_point = (0, 0)
today_date.anchored_position = (15, 13)

city_name = label.Label(
    terminalio.FONT, text=secrets["openweather_location"], color=0x000000
)
city_name.anchor_point = (0, 0)
city_name.anchored_position = (15, 24)

today_icon = displayio.TileGrid(
    icons_large_bmp,
    pixel_shader=icons_small_pal,
    x=10,
    y=40,
    width=1,
    height=1,
    tile_width=70,
    tile_height=70,
)

today_morn_temp = label.Label(terminalio.FONT, text="+100F", color=0x000000)
today_morn_temp.anchor_point = (0.5, 0)
today_morn_temp.anchored_position = (118, 59)

today_day_temp = label.Label(terminalio.FONT, text="+100F", color=0x000000)
today_day_temp.anchor_point = (0.5, 0)
today_day_temp.anchored_position = (149, 59)

today_night_temp = label.Label(terminalio.FONT, text="+100F", color=0x000000)
today_night_temp.anchor_point = (0.5, 0)
today_night_temp.anchored_position = (180, 59)

today_humidity = label.Label(terminalio.FONT, text="100%", color=0x000000)
today_humidity.anchor_point = (0, 0.5)
today_humidity.anchored_position = (105, 95)

today_wind = label.Label(terminalio.FONT, text="99m/s", color=0x000000)
today_wind.anchor_point = (0, 0.5)
today_wind.anchored_position = (155, 95)

today_sunrise = label.Label(terminalio.FONT, text="12:12 PM", color=0x000000)
today_sunrise.anchor_point = (0, 0.5)
today_sunrise.anchored_position = (45, 117)

today_sunset = label.Label(terminalio.FONT, text="12:12 PM", color=0x000000)
today_sunset.anchor_point = (0, 0.5)
today_sunset.anchored_position = (130, 117)

status_label = label.Label(terminalio.FONT, text="Status", color=0x222222)
status_label.anchor_point = (0, 0.5)
status_label.anchored_position = (180, 117)

today_banner = displayio.Group(max_size=11)
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
today_banner.append(status_label)

future_banners = [
    make_banner(x=210, y=18),
    make_banner(x=210, y=39),
    make_banner(x=210, y=60),
    make_banner(x=210, y=81),
    make_banner(x=210, y=102),
]

magtag.splash.append(today_banner)
for future_banner in future_banners:
    magtag.splash.append(future_banner)

# ===========
#  M A I N
# ===========

## Works, but is rather loud.
#magtag.peripherals.play_tone(880, 0.5)
#magtag.peripherals.play_tone(440, 0.25)
#magtag.peripherals.play_tone(880, 0.5)

print('Network on? {}'.format(magtag.network.enabled))


print("Getting Lat/Lon...")
latlon = get_latlon()
print('Location: {}'.format(latlon))

print("Fetching forecast...")
forecast_data, utc_time, local_tz_offset = get_forecast(latlon)

print("Updating...")
update_today(forecast_data[0], local_tz_offset)
for day, forecast in enumerate(forecast_data[1:6]):
    update_banner(future_banners[day], forecast)

print("Refreshing...")
time.sleep(magtag.display.time_to_refresh + 1)
magtag.display.refresh()
time.sleep(magtag.display.time_to_refresh + 1)

print("Lightly sleeping for two minutes before entering deep sleep...")
# TODO

# Free space at shutdown
print_free_mem()
print('Network on? {}'.format(magtag.network.enabled))

print("Sleeping...")
sleep_until_button_1()
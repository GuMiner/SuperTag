import json
import time
from adafruit_display_text import label
from adafruit_magtag.magtag import MagTag

# Utility packages
import conversion
import diagnostics
import display_util
import network
import state
import status

import financials
import weather

default_magtag_splash_length = None

def render_and_light_sleep(magtag):
    # Clear all UI
    while len(magtag.splash) > default_magtag_splash_length:
        magtag.splash.pop()
    magtag.graphics.set_background(0xFFFFFF)
    time.sleep(magtag.display.time_to_refresh)

    # Render page
    status.set(2, status.RED)
    weather.run(magtag)
    status.set(2, status.GREEN)
    
    # Render common UI.
    battery_label = display_util.make_label("?.??", (271, 6))
    battery_label.text = "{:.2f}".format(magtag.peripherals.battery)
    magtag.splash.append(battery_label)
    
    
    print("Refreshing...")
    time.sleep(magtag.display.time_to_refresh + 1)
    magtag.display.refresh()
    time.sleep(magtag.display.time_to_refresh + 1)
    status.set(2, status.BLUE)

    for i in range(20):
        status.set(2, status.YELLOW)
        time.sleep(0.5)
        status.set(2, status.BLUE)
        time.sleep(0.5)
    
    print("Lightly sleeping for one minute before entering deep sleep...")
    if state.light_sleep():
        render_and_light_sleep(magtag)


# Free space at startup.
diagnostics.print_free_mem()
state.load()

# Setup and run
magtag = MagTag()
default_magtag_splash_length = len(magtag.splash)
magtag.peripherals.speaker_disable = True
status.enable(magtag)

render_and_light_sleep(magtag)

# Free space at shutdown
diagnostics.print_free_mem()
print('Network on? {}'.format(magtag.network.enabled))

print("Sleeping for 1 day or until button A or B are pressed...")
magtag.peripherals.neopixel_disable = True
state.deep_sleep()
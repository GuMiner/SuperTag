import alarm
import board
import json
import time
import neopixel
from adafruit_display_text import label
from adafruit_magtag.magtag import MagTag

import conversion
import diagnostics
import display_util
import network
import weather

# Free space at startup.
diagnostics.print_free_mem()

# Must be set earlier on before something else (unknown) grabs the pin.
# BUTTON_A/Time alarm -- no-cycle-reset. BUTTON_B -- cycle the display on reset.
#pin_alarm_first_button = alarm.pin.PinAlarm(pin=board.BUTTON_A, value=False, pull=True)
#pin_alarm_second_button = alarm.pin.PinAlarm(pin=board.BUTTON_B, value=False, pull=True)

# alarm.wake_alarm holds an equivalent alarm for what waked the device.
cycle_display = alarm.wake_alarm is not None and hasattr(alarm.wake_alarm, 'pin') and alarm.wake_alarm.pin == board.BUTTON_B
print(hasattr(alarm.wake_alarm, 'pin'))
#print(alarm.wake_alarm.pin)
display_weather = False # False -- financials

if alarm.sleep_memory:
    display_weather = alarm.sleep_memory[0]

print('Cycle display: {}. Read saved settings {}'.format(cycle_display, alarm.sleep_memory == True)) # is True "is"

# --| USER CONFIG |--------------------------


magtag = MagTag()

# Enable neopixels
magtag.peripherals.neopixel_disable = False
external_pixels = magtag.peripherals.neopixels
external_pixels.brightness = 0.3
external_pixels.auto_write = False

magtag.peripherals.speaker_disable = True
print('Neopixels disabled? {}'.format(magtag.peripherals.neopixel_disable))
print('Speaker disabled? {}'.format(magtag.peripherals.speaker_disable))

# Grabbed from color cycle demo.
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(4):
            rc_index = (i * 256 // 4) + j
            external_pixels[i] = wheel(rc_index & 255)
        #external_pixels[2] = (0, 0, 0)
        external_pixels.show()
        time.sleep(wait)

# rainbow_cycle(0.01)
# time.sleep(0.2)

# Clear
external_pixels[1] = (0, 0, 0)
external_pixels[2] = (0, 0, 0)
external_pixels[3] = (0, 0, 0)

def set_status(status):
    external_pixels[0] = wheel(status)
    external_pixels.show()

set_status(1)

def sleep_until_button_1():
    '''Does what it says, but it also awakes after 1 day too'''
    alarm.sleep_memory[0] = display_weather
    
    time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 3600 * 24)
    
    print("Sleeping for 1 day or until the leftmost button is pressed")
    alarm.exit_and_deep_sleep_until_alarms(time_alarm) #, pin_alarm_second_button) #pin_alarm_first_button, pin_alarm_second_button)


# ===========
# U I
# ===========
weather.run(magtag)

# Common
#battery_label = display_util.make_label("?.??", (271, 6))

#today_banner.append(battery_label)

#battery_label.text = "{:.2f}".format(magtag.peripherals.battery)
# ===========
#  M A I N
# ===========

## Works, but is rather loud.
#magtag.peripherals.play_tone(880, 0.5)
#magtag.peripherals.play_tone(440, 0.25)
#magtag.peripherals.play_tone(880, 0.5)

print('Network on? {}'.format(magtag.network.enabled))

set_status(20)

set_status(140)
print("Refreshing...")
time.sleep(magtag.display.time_to_refresh + 1)
magtag.display.refresh()
time.sleep(magtag.display.time_to_refresh + 1)

set_status(180)
print("Lightly sleeping for two minutes before entering deep sleep...")
# TODO

# Free space at shutdown
diagnostics.print_free_mem()
print('Network on? {}'.format(magtag.network.enabled))

print("Sleeping...")
magtag.peripherals.neopixel_disable = True
sleep_until_button_1()
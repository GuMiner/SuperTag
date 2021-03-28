import alarm
import board
import time

# Must be set early on before something else (unknown) grabs the pin.
# BUTTON_A/Time alarm -- no-cycle-reset. BUTTON_B -- cycle the display on reset.
pin_alarm_first_button = alarm.pin.PinAlarm(pin=board.BUTTON_A, value=False, pull=True)
pin_alarm_second_button = alarm.pin.PinAlarm(pin=board.BUTTON_B, value=False, pull=True)

display_weather = True # False -- financials


def _cycle_display_if_requested():
    global display_weather
    
    if hasattr(alarm.wake_alarm, 'pin') and alarm.wake_alarm.pin == board.BUTTON_B:
        display_weather = False
        return True
    elif hasattr(alarm.wake_alarm, 'pin') and alarm.wake_alarm.pin == board.BUTTON_A:
        display_weather = True
        return True

    return False


def light_sleep():
    light_sleep_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 60)
    alarm.light_sleep_until_alarms(light_sleep_alarm, pin_alarm_first_button, pin_alarm_second_button)
    return _cycle_display_if_requested()


def deep_sleep():
    alarm.sleep_memory[0] = display_weather
    
    time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 3600 * 24)
    alarm.exit_and_deep_sleep_until_alarms(time_alarm, pin_alarm_first_button, pin_alarm_second_button)


def load():
    global display_weather
    
    # Load from sleep, if present
    if alarm.sleep_memory:
        display_weather = alarm.sleep_memory[0]
        
    # If the 'next' button was pressed, cycle the weather state.
    _cycle_display_if_requested()
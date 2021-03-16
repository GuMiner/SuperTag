import time

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

external_pixels = None


def _clear():
    external_pixels[0] = (0, 0, 0)
    external_pixels[1] = (0, 0, 0)
    external_pixels[2] = (0, 0, 0)
    external_pixels[3] = (0, 0, 0)


def enable(magtag):
    global external_pixels
    magtag.peripherals.neopixel_disable = False
    external_pixels = magtag.peripherals.neopixels

    external_pixels.brightness = 0.3
    external_pixels.auto_write = False
    _clear()


def set(pixel_id, color):
    external_pixels[pixel_id] = color
    external_pixels.show()

    time.sleep(0.05) # So colors actually appear for quick operations.

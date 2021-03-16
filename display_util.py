import displayio
import terminalio
from adafruit_display_text import label

def make_label(sample_text, position):
    lbl = label.Label(terminalio.FONT, text=sample_text, color=0x000000)
    lbl.anchor_point = (0, 0.5)
    lbl.anchored_position = position
    return lbl

def make_group(items, x, y):
    group = displayio.Group(max_size=len(items), x=x, y=y)
    for item in items:
        group.append(item)
    return group

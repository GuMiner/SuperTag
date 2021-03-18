from adafruit_display_shapes import rect
import displayio
from secrets import secrets

import const
import display_util

BACKGROUND_BMP = "/bmps/financials_bg.bmp"


def _render_stock_categories(stock_categories):
    stock_category_labels = displayio.Group(max_size=len(stock_categories))
    for i in range(0, len(stock_categories)):
        stock_category_labels.append(display_util.make_label(stock_categories[i], (10, 20 + i * 14)))
    return stock_category_labels


def _render_asset_allocations(stock_categories):
    asset_allocations = displayio.Group(max_size=2*len(stock_categories))
    if not const.SIMULATE_NETWORK:
        for i in range(0, len(stock_categories)):
            allocation = 99 - i * 15
            asset_allocations.append(display_util.make_label('{:.1f}%'.format(allocation), (110, 20 + i * 14)))
            asset_allocations.append(rect.Rect(145, int(15 + i * 14), int(allocation/2.0), 12, fill=0x888888, outline=0x000000, stroke=1))
    return asset_allocations

def run(magtag):
    magtag.graphics.set_background(BACKGROUND_BMP)
    
    stock_categories = secrets["stockCategories"]
    stock_category_labels = _render_stock_categories(stock_categories)
    asset_allocations = _render_asset_allocations(stock_categories)
    
    magtag.splash.append(stock_category_labels)
    magtag.splash.append(asset_allocations)

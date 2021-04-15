from adafruit_display_shapes import rect
import displayio
import json
import time
from secrets import secrets

import const
import display_util
import network

BACKGROUND_BMP = '/bmps/financials_bg.bmp'
ALLOCATION_SCALE = 1.5

def _get_financials(magtag):
    magtag.url = 'https://helium24.net/api/Finance/Status'
    magtag.json_path = None 
    if const.SIMULATE_NETWORK:
        return json.loads('{"allocations":{"Corporate Bonds":4.26088142,"Emerging Markets":12.1293392,"Foreign Stock":10.4879065,"Muncipal Bonds":4.05872,"Other":18.8859253,"Real Estate":5.290577,"US Dividend":27.33569,"US General":17.5509624},"performances":{"Corporate Bonds":14.1550779,"Emerging Markets":14.1830559,"Foreign Stock":12.3361588,"Muncipal Bonds":8.140934,"Other":69.59058,"Real Estate":-0.00867748,"US Dividend":23.8243217,"US General":7.89266825},"overalPerformance":21.5531578}')

    def parse_result(raw_data):
        result = json.loads(raw_data)
        return result

    return network.fetch_with_retries(magtag, parse_result)


def _render_stock_categories(stock_categories):
    stock_category_labels = displayio.Group(max_size=len(stock_categories))
    for i in range(0, len(stock_categories)):
        stock_category_labels.append(display_util.make_label(stock_categories[i], (10, 20 + i * 14)))
    return stock_category_labels
    

def _render_asset_allocations(stock_categories, data):    
    asset_allocations = displayio.Group(max_size=2*len(stock_categories))
    for i in range(0, len(stock_categories)):
        allocation = data['allocations'][stock_categories[i]]
        scaled_allocation = int(allocation * ALLOCATION_SCALE)
        scaled_allocation = 1 if scaled_allocation == 0 else scaled_allocation
        
        asset_allocations.append(display_util.make_label('{:.1f}%'.format(allocation), (110, 20 + i * 14)))
        asset_allocations.append(rect.Rect(145, int(15 + i * 14), scaled_allocation, 12, fill=0x888888, outline=0x000000, stroke=1))
    return asset_allocations


def _render_other_allocations(data):
    allocation = data['allocations']['Other']
    scaled_allocation = int(allocation * ALLOCATION_SCALE)
    scaled_allocation = 1 if scaled_allocation == 0 else scaled_allocation

    other = displayio.Group(max_size=3)
    other.append(display_util.make_label('{:.1f}%'.format(allocation), (110, 118)))
    other.append(rect.Rect(145, 113, scaled_allocation, 12, fill=0x888888, outline=0x000000, stroke=1))
    other.append(display_util.make_label(secrets['otherCategoryName'], (150, 118)))
    return other
    

def _render_asset_status(stock_categories, data):
    asset_status = displayio.Group(max_size=2*len(stock_categories))
    for i in range(0, len(stock_categories)):
        status = data['performances'][stock_categories[i]]
        scaled_status = int(status * ALLOCATION_SCALE)
        scaled_status = 1 if scaled_status == 0 else scaled_status

        offset_x = 230
        if scaled_status > 0:
            asset_status.append(rect.Rect(offset_x, int(15 + i * 14), scaled_status, 12, fill=0xCCCCCC, outline=0x000000, stroke=1))
            offset_x = offset_x + 7 # Make '-' align with '+' items
        else:
            asset_status.append(rect.Rect(offset_x + scaled_status, int(15 + i * 14), -scaled_status, 12, fill=0xCCCCCC, outline=0x000000, stroke=1))

        asset_status.append(display_util.make_label('{:.1f}%'.format(status), (offset_x - 20, 20 + i * 14)))
    return asset_status


def _render_sum_total(data):
    # At this point the typo is baked in until I need to update the server again.
    return display_util.make_label('{:.1f}%'.format(data['overalPerformance']), (228, 117))


def run(magtag):
    magtag.graphics.set_background(BACKGROUND_BMP)
    time.sleep(magtag.display.time_to_refresh)

    financial_data = _get_financials(magtag)
    
    stock_categories = secrets['stockCategories']
    stock_category_labels = _render_stock_categories(stock_categories)
    asset_allocations = _render_asset_allocations(stock_categories, financial_data)
    other = _render_other_allocations(financial_data)
    status = _render_asset_status(stock_categories, financial_data)
    sum_total = _render_sum_total(financial_data)
    
    magtag.splash.append(stock_category_labels)
    magtag.splash.append(asset_allocations)
    magtag.splash.append(other)
    magtag.splash.append(status)
    magtag.splash.append(sum_total)

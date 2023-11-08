# source: https://openai.com/_nuxt/GPTVPricingCalculator.99351142.js from https://openai.com/pricing
# (converted to python)
import math


def calculate_vision_cost(width, height, is_low_res=False):
    base_price = 85
    tile_price = 170
    high_resolution_multiplier = 1e-5

    # Determine the initial resize dimensions
    initial_resize_width = width
    initial_resize_height = height
    if width > 2048 or height > 2048:
        if width > height:
            initial_resize_width = 2048
            initial_resize_height = round(2048 * height / width)
        else:
            initial_resize_height = 2048
            initial_resize_width = round(2048 * width / height)

    # Determine if further resizing is needed
    further_resize_width = initial_resize_width
    further_resize_height = initial_resize_height
    if initial_resize_width > 768 or initial_resize_height > 768:
        if initial_resize_width < initial_resize_height:
            further_resize_width = min(768, initial_resize_width)
        else:
            further_resize_height = min(768, initial_resize_height)
            further_resize_width = round(
                further_resize_height * initial_resize_width / initial_resize_height
            )
            further_resize_height = round(
                further_resize_height * initial_resize_height / initial_resize_width
            )

    # Calculate the number of vertical and horizontal tiles
    vertical_tiles = (
        1 + math.ceil((further_resize_height - 512) / 512)
        if further_resize_height > 512
        else 1
    )
    horizontal_tiles = (
        1 + math.ceil((further_resize_width - 512) / 512)
        if further_resize_width > 512
        else 1
    )

    # Calculate the total number of tiles and tokens
    total_tiles = vertical_tiles * horizontal_tiles
    total_tokens = (
        base_price + total_tiles * tile_price if not is_low_res else base_price
    )

    # Calculate the total price
    total_price = total_tokens * high_resolution_multiplier

    # Round the total price as JavaScript does
    total_price = round(total_price * 100000) / 100000

    return total_price


import colorsys
import math


def dist(x1, y1, x2, y2):
    """Calculates the distance of two points"""
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def rgb_from_hue(hue):
    rgb_color = colorsys.hsv_to_rgb(hue, 1, 1)
    return tuple(int(value * 255) for value in rgb_color)

def interpolate_hue(h1, h2, t):
    shortest_angle = (h2 - h1) % 1
    step = (2 * shortest_angle % 1) - shortest_angle
    return ((step * t) + h1) % 1
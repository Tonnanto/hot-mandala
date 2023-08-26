
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

def interpolate_rgb(c1, c2, t):
    t = min(1, max(0, t))
    return (min(255, c1[0] + (t * (c2[0] - c1[0]))), min(255, c1[1] + (t * (c2[1] - c1[1]))), min(255, c1[2] + (t * (c2[2] - c1[2]))))

# def distance_to_line(m, b, x0, y0):
#     numerator = abs(m * x0 - y0 + b)
#     denominator = math.sqrt(m ** 2 + 1)
#     return numerator / denominator

# def angle_to_slope(angle_degrees):
#     angle_radians = math.radians(angle_degrees)
#     return math.tan(angle_radians)
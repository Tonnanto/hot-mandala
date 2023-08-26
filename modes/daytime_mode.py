
import time

import numpy as np
from modes.mode import Mode
from util import dist, interpolate_rgb

DAY_BG_COLOR = (96, 150, 222)
DAY_SUN_COLOR = (255, 207, 0)
SUNSET_BG_COLOR = (135, 164, 211)
SUNSET_SUN_COLOR = (244, 169, 68)
CIVIL_DAWN_BG_COLOR = (135, 164, 211)
NAUTICAL_DAWN_BG_COLOR = (71, 114, 186)
ASTRONOMICAL_DAWN_BG_COLOR = (39, 61, 104)
NIGHT_BG_COLOR = (21, 27, 55)

SUNSET_ANGLE = 12
CIVIL_DAWN_ANGLE = -6
NAUTICAL_DAWN_ANGLE = -12
ASTRONOMICAL_DAWN_ANGLE = -18

class DaytimeMode(Mode):

    def __init__(self):
        super().__init__()
        self.time = time.time()
        self.fast_forward = 1
        self.last_time_stamp = time.time()
        self.sun_angle = 0 # angle of sun above horizon
        self.sun_layers = 5

        
    def tick(self, mandala):
        if (self.fast_forward == 1):
            self.time = time.time()
        else:
            self.time += self.fast_forward * (time.time() - self.last_time_stamp)
        self.last_time_stamp = time.time()

        self.sun_angle = (abs(((self.time * 24) % 360) - 180) - 90) / 2

        if (self.sun_angle > SUNSET_ANGLE):
            return self.day(mandala)

        elif (self.sun_angle > 0):
            return self.sunset(mandala)
        
        elif (self.sun_angle > ASTRONOMICAL_DAWN_ANGLE):
            return self.dawn(mandala)
        
        else:
            return self.night(mandala)


    def day(self, mandala):
        colors = [DAY_BG_COLOR for _ in mandala.leds]

        for index, layer in enumerate(mandala.layers):
            if (index < self.sun_layers):
                for led in layer:
                    colors[led] = DAY_SUN_COLOR

        return colors
    
    def sunset(self, mandala):
        bg_color = interpolate_rgb(SUNSET_BG_COLOR, DAY_BG_COLOR, self.sun_angle / SUNSET_ANGLE)
        colors = [bg_color for _ in mandala.leds]

        sun_y = max(0, min(2, 2 - (self.sun_angle / (SUNSET_ANGLE / 2))))
        sun_diameter = 1.4

        ambient_alpha = np.interp(self.sun_angle, [0, SUNSET_ANGLE], [1, 0])
        self.add_ambient_color(mandala, colors, SUNSET_SUN_COLOR, 5, 5, ambient_alpha)

        for index, led in enumerate(mandala.leds):
            sun_distance = dist(led[0], led[1], 0, sun_y)
            if (sun_distance < sun_diameter / 2):
                colors[index] = interpolate_rgb(DAY_SUN_COLOR, SUNSET_SUN_COLOR, sun_y / 2)

        return colors
    
    def dawn(self, mandala):
        bg_color = None
        if (self.sun_angle > CIVIL_DAWN_ANGLE):
            bg_color = interpolate_rgb(NAUTICAL_DAWN_BG_COLOR, CIVIL_DAWN_BG_COLOR, (self.sun_angle - CIVIL_DAWN_ANGLE) / (0 - CIVIL_DAWN_ANGLE))
        elif (self.sun_angle > NAUTICAL_DAWN_ANGLE):
            bg_color = interpolate_rgb(ASTRONOMICAL_DAWN_BG_COLOR, NAUTICAL_DAWN_BG_COLOR, (self.sun_angle - NAUTICAL_DAWN_ANGLE) / (CIVIL_DAWN_ANGLE - NAUTICAL_DAWN_ANGLE))
        else:
            bg_color = interpolate_rgb(NIGHT_BG_COLOR, ASTRONOMICAL_DAWN_BG_COLOR, (self.sun_angle - ASTRONOMICAL_DAWN_ANGLE) / (NAUTICAL_DAWN_ANGLE - ASTRONOMICAL_DAWN_ANGLE))
        colors = [bg_color for _ in mandala.leds]

        dawn_alpha = np.interp(self.sun_angle, [ASTRONOMICAL_DAWN_ANGLE, CIVIL_DAWN_ANGLE], [0, 1])
        self.add_ambient_color(mandala, colors, SUNSET_SUN_COLOR, 5, 5, dawn_alpha)

        return colors
    
    def night(self, mandala):
        colors = [NIGHT_BG_COLOR for _ in mandala.leds]

        return colors
    
    def add_ambient_color(self, mandala, colors, ambient_color, center_y, radius, alpha):
        for index, led in enumerate(mandala.leds):
            dawn_distance = dist(led[0], led[1], 0, center_y)
            if (dawn_distance < radius):
                colors[index] = interpolate_rgb(colors[index], ambient_color, alpha * (1 - (dawn_distance - (radius - 1))))
        return colors
    

import time
import numpy as np
from modes.mode import Mode
from util import dist, interpolate_hue, rgb_from_hue



class RainbowMode(Mode):
    
    def __init__(self, variant):
        self.hue = 0
        self.variant = variant
        self.animation_speed = 0.01
        self.base_range = 0.3
        self.range = self.base_range
        self.alt_range = True # periodically increase and decrease the rainbow range
        self.alt_direction = True # periodically change the direction
        self.inverse = False
        super().__init__()

    def tick(self, leds):

        if (self.inverse):
            self.hue = (self.hue - self.animation_speed) % 1
        else:
            self.hue = (self.hue + self.animation_speed) % 1

        if (self.alt_direction):
            # switch direction every 30 seconds
            self.inverse = time.time() % 60 > 30
        if (self.alt_range):
            # alter rainbow range in a 24 second cycle
            self.range = 0.5 * self.base_range + (self.base_range * (abs(time.time() % 24 - 12) / 12))

        if (self.variant == 1):
            return self.single_color(leds)
        if (self.variant == 2):
            return self.circular(leds)
        if (self.variant == 3):
            return self.spiral(leds)
        if (self.variant == 4):
            return self.ring(leds)
    
    def single_color(self, leds):
        color = rgb_from_hue(self.hue)
        return list(map(lambda x: color, leds))
    
    def circular(self, leds):
        colors = []
        for led in leds:
            d = dist(led[0], led[1], 0, 0)
            hue = (self.hue - (d * self.range)) % 1
            colors.append(rgb_from_hue(hue))
        return colors
    
    def spiral(self, leds):
        colors = []
        for led in leds:
            angle = np.degrees(np.arctan2(led[1], led[0]))
            d = dist(led[0], led[1], 0, 0)
            twirl = (d * 0.6)
            hue = (self.hue - twirl - (angle / 360)) % 1
            hue = (self.hue + 0.5 * abs(hue - 0.5)) % 1
            # hue = interpolate_hue(self.hue, hue, 0.5)
            # hue = abs(2 * hue - 1)
            colors.append(rgb_from_hue(hue))
        return colors
    
    def ring(self, leds):
        colors = []
        for led in leds:
            d = dist(led[0], led[1], 0, 0)
            d = abs(d - 0.5) * 2
            hue = (self.hue + (d * self.range)) % 1
            colors.append(rgb_from_hue(hue))
        return colors


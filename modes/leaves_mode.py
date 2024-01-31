
import random
import numpy as np
from modes.mode import Mode
from util import rgb_from_hue


class LeavesMode(Mode):
    
    def __init__(self, mandala):
        self.layer_colors = list(map(lambda x: random.random(), mandala.layers))
        self.progress = 0
        self.animation_speed = 0.0045
        super().__init__()

    def tick(self, mandala):
        self.progress = self.progress + self.animation_speed

        colors = np.zeros((mandala.led_count, 3))
        for index, layer in enumerate(mandala.layers):
            layer_hue = self.layer_colors[index]
            layer_hue = layer_hue + abs((self.progress + index / 5 + (self.progress * index / 10)) % 1 - 0.5)
            for led in layer:
                colors[led] = rgb_from_hue(layer_hue)
        return colors

from modes.mode import Mode

class ColorMode(Mode):

    def __init__(self, color):
        self.color = color
        super().__init__()

    def tick(self, leds):
        return list(map(lambda x: self.color, leds))
    
    def refresh_rate(self):
        return 20
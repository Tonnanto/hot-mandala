
from modes.mode import Mode

class ColorMode(Mode):

    def __init__(self, color):
        self.color = color
        super().__init__()

    def tick(self, mandala):
        return [self.color for _ in mandala.leds]
    
    def refresh_rate(self):
        return 20
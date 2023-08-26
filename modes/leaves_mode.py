
from modes.mode import Mode


class LeavesMode(Mode):
    
    def __init__(self, ):
        super().__init__()

    def tick(self, leds):
        return list(map(lambda x: self.color, leds))
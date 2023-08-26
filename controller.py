import time

class Controller:

    def __init__(self, display, mandala):
        self.display = display
        self.mandala = mandala
        self.mode = None
        self.last_refresh = time.time()
        pass

    def __iter__(self):
        while self.mode is not None:
            if (time.time() > self.last_refresh + (1 / self.mode.refresh_rate())):
                self.last_refresh = time.time()
                led_colors = self.mode.tick(self.mandala)
                self.display.show(led_colors)
                yield

    def set_mode(self, mode):
        self.mode = mode

    def start(self):
        print('Controller started.')
        print(str(self.mandala.led_count) + ' leds registered.')
        return
    
    def stop(self):
        print('Controller stopped.')
        return
    

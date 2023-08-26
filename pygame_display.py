import os
import numpy as np
from display import Display
import pygame as pg

LED_SIZE = 4
BLUR_STEPS = 4
BLUR_RADIUS = 25

def circle_surf(radius, color):
    surf = pg.Surface((radius * 2, radius * 2))
    pg.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf

class PygameDisplay(Display):
    
    def __init__(self, width, height, mandala):
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"2560,0" # make sure window opens on second monitor
        pg.init()
        self.width = width
        self.height = height
        self.led_count = mandala.led_count
        self.leds = mandala.leds
        self.colors = self.create_initial_color_list()
        self.prev_colors = np.copy(self.colors)
        self.window = pg.display.set_mode((width, height), pg.DOUBLEBUF)
        self.mandala = pg.transform.scale(pg.image.load("mandala.png"), (1400, 1400))

    def __iter__(self):
        while True:

            if not np.array_equal(self.colors, self.prev_colors):
                background_color = (0, 0, 0)  # Black color
                self.window.fill(background_color)
                for i in range(self.led_count):
                    color = self.colors[i]
                    coords = self.leds[i]
                    coords = tuple(a * b for a, b in zip(coords, (700, 700)))
                    coords = tuple(a + b for a, b in zip(coords, (1280, 720)))
                    self.draw_led(coords, color)

                self.draw_mandala()
                pg.display.update()
            
            self.prev_colors = np.copy(self.colors)
            yield

    def draw_led(self, coords, color):
        # pg.draw.circle(self.window, color, coords, LED_SIZE / 2)
        for step in range(BLUR_STEPS):
            r = LED_SIZE * BLUR_RADIUS - step * (LED_SIZE * BLUR_RADIUS / BLUR_STEPS)
            alpha = 1.5 / BLUR_STEPS * ((step + 1) / BLUR_STEPS)
            alpha = min(1, alpha)
            blur_color = tuple(a * b for a, b in zip(color, (alpha, alpha, alpha)))
            self.window.blit(circle_surf(r, blur_color), (int(coords[0] - r), int(coords[1] - r)), special_flags=pg.BLEND_RGB_ADD)

    def draw_mandala(self):
        image_rect = self.mandala.get_rect()
        image_rect.center = (self.width * 0.5, self.height * 0.5)
        self.window.blit(self.mandala, image_rect)

    def create_initial_color_list(self) -> np.array:
        return np.zeros((self.led_count, 3))
    
    def show(self, colors: np.array):
        assert len(colors) == self.led_count
        self.prev_colors = np.copy(self.colors)
        self.colors = colors

    def stop(self):
        pg.quit()

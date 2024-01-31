
from modes.clock_mode import ClockMode
from modes.color_mode import ColorMode
from modes.daytime_mode import DaytimeMode
from modes.leaves_mode import LeavesMode
from modes.rainbow_mode import RainbowMode
from pygame_display import PygameDisplay
from controller import Controller
from mandala import pygame_mandala
import pygame as pg

# Constants
# fps = 30

# Variables
running = True

# Components
mandala = pygame_mandala
display = PygameDisplay(1920, 1080, mandala)
controller = Controller(display, mandala)

# mode = ColorMode((0, 0, 255))
mode = LeavesMode(mandala)
# mode = RainbowMode(3)
# mode = ClockMode()
# mode = DaytimeMode()

controller.start()
controller.set_mode(mode)

def mainloop():
    global running

    controller_iterator = iter(controller)
    display_iterator = iter(display)

    while running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            # if event.type == pg.MOUSEBUTTONDOWN:
            #     cursor_x, cursor_y = pg.mouse.get_pos()
            #     x = cursor_x
            #     y = cursor_y
            #     x -= 1280
            #     y -= 720
            #     x /= 700
            #     y /= 700
            #     print(f'({round(x, 3)}, {round(y, 3)}),')

        try:
            next(controller_iterator)
            next(display_iterator)
        except StopIteration:
            running = False

    if not running:
        controller.stop()
        display.stop()


mainloop()
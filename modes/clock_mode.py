
import datetime
import math
import numpy as np
from modes.mode import Mode
from util import dist, interpolate_rgb, rgb_from_hue


class ClockMode(Mode):

    def __init__(self):
        super().__init__()
        self.bg_color = (12, 5, 25)
        self.hour_color = (255, 0, 0)
        self.minute_color = (255, 140, 0)
        self.second_color = (255, 208, 0)
        self.hand_thickness = 0.12

    def tick(self, mandala):
        
        colors = list(map(lambda x: self.bg_color, mandala.leds))

        current_time = datetime.datetime.now()
        second = current_time.second + (current_time.microsecond / 1000000)
        minute = current_time.minute + (second / 60)
        hour = current_time.hour + (minute / 60)

        hour_angle = 30 * hour % 360
        minute_angle = 6 * minute % 360
        second_angle = 6 * second % 360

        for index, led in enumerate(mandala.leds):
            hour_dist = self.clock_hand_distance(hour_angle, led[0], led[1])
            minute_dist = self.clock_hand_distance(minute_angle, led[0], led[1])
            second_dist = self.clock_hand_distance(second_angle, led[0], led[1])

            if (hour_dist < self.hand_thickness):
                if (dist(led[0], led[1], 0, 0) < 0.8):
                    colors[index] = interpolate_rgb(self.bg_color, self.hour_color, 1 - hour_dist * (1 / self.hand_thickness))
            if (minute_dist < self.hand_thickness):
                colors[index] = interpolate_rgb(colors[index], self.minute_color, 1 - minute_dist * (1 / self.hand_thickness))
            if (second_dist < self.hand_thickness):
                colors[index] = interpolate_rgb(colors[index], self.second_color, 1 - second_dist * (1 / self.hand_thickness))

        return colors
    
    def clock_hand_distance(self, hand_angle, x, y):
        clock_hand_x = math.cos(math.radians(hand_angle))
        clock_hand_y = math.sin(math.radians(hand_angle))
        
        # prevent leds on opposite side of clock hand to light up
        point_angle = (math.degrees(math.atan2(y, x)) + 90) % 360
        angle_difference = abs(hand_angle - point_angle)
        if angle_difference > 90:
            return float('inf')

        distance = abs((clock_hand_x * x + clock_hand_y * y) /
                    math.sqrt(clock_hand_x**2 + clock_hand_y**2))
        return distance
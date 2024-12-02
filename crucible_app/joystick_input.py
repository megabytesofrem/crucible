import pygame
from gi.repository import GLib


class JoystickInput:
    def __init__(self):
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        else:
            self.joystick = None

    def poll_joystick(self):
        if self.joystick:
            pygame.event.pump()
            for event in pygame.event.get():
                match event.type:
                    case pygame.JOYHATMOTION:
                        print(f"D-Pad moved to {event.value}")
                    case pygame.JOYAXISMOTION:
                        print(f"Axis {event.axis} moved to {event.value:.2f}")
                    case pygame.JOYBUTTONDOWN:
                        print(f"Button down {event.button}")
                    case pygame.JOYBUTTONUP:
                        print(f"Button down {event.button}")
                    case _:
                        pass

        return True

    def add_event_loop(self):
        GLib.timeout_add(100, self.poll_joystick)

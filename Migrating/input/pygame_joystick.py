import pygame
from .input_source_base import InputSource

class PygameJoystickInput(InputSource):
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.js = None

        count = pygame.joystick.get_count()
        print(f"[Joystick] Found {count} joystick(s).")

        if count > 0:
            self.js = pygame.joystick.Joystick(0)
            self.js.init()
            print(f"[Joystick] Initialized: {self.js.get_name()}")
        else:
            print("[Joystick] No joystick detected.")

    def read(self):
        if not self.js:
            return {}
        pygame.event.pump()
        raw = {
            f"axis_{i}": self.js.get_axis(i) for i in range(self.js.get_numaxes())
        } | {
            f"button_{i}": self.js.get_button(i) for i in range(self.js.get_numbuttons())
        }
        #print(f"[Joystick Raw] {raw}")
        return raw
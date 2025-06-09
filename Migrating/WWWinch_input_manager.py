# input_manager.py
import math
import time

try:
    import pygame
    pygame.init()
    _pygame_ok = True
except ImportError:
    _pygame_ok = False

class Joystick:
    def __init__(self):
        self.js = None
        if _pygame_ok:
            pygame.joystick.init()
            count = pygame.joystick.get_count()
            print(f"[Joystick] Number of joysticks detected: {count}")
            if count > 0:
                self.js = pygame.joystick.Joystick(0)
                self.js.init()
                print(f"[Joystick] Initialized: {self.js.get_name()}")
            else:
                print("[Joystick] No joystick detected!")
        else:
            print("[Joystick] Pygame not available.")


    def read(self):
        if self.js:
            pygame.event.pump()
            return self.js.get_axis(1) * 10  # Scale to [-10, +10]
        else:
            return 0.0

class InputManager:
    def __init__(self):
        self.joystick = Joystick()

    def inject(self, props: dict):
        """,
        Injects current joystick values into props.
        This modifies `props` in place.
        """
        val = self.joystick.read()
        if "ActProp" not in props:
            props["ActProp"] = {}
        props["ActProp"]["SpeedSoll"] = val

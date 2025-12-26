class LedState:
    def __init__(self):
        self.green: int = 1
        self.red: int = 0

    def set_state(self, green: int, red: int) -> None:
        if green not in (0, 1) or red not in (0, 1):
            raise ValueError("LEDs state must be 0 or 1")
        self.green = green
        self.red = red

    def turn_green_on(self) -> None:
        self.set_state(1, 0)

    def turn_red_on(self) -> None:
        self.set_state(0, 1)

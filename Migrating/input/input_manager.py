class InputManager:
    def __init__(self, source):
        self.source = source

    def read_signals(self) -> dict:
        signals = self.source.read()
        #print(f"[InputManager] Raw signals: {signals}")
        return signals
class InputManager:
    def __init__(self, source, bindings: dict):
        self.source = source
        self.bindings = bindings

    def inject(self, props: dict):
        data = self.source.read()
        #print(f"[Joystick Raw] {data}")

        actprop = props.setdefault("ActProp", {})

        for target_field, mapping in self.bindings.items():
            source_key = mapping.get("source")
            scale = mapping.get("scale", 1.0)
            value = data.get(source_key)
            if value is not None:
                actprop[target_field] = value * scale if isinstance(value, (float, int)) else value

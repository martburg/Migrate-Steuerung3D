from WWWinch_properties import Properties
import math

class Codec:
    """
    This class handles the packing and unpacking and decoding of the wiredworks Winch properties.
    It is used to convert the properties to a format suitable for transmission and vice versa.
    """
    
    def __init__(self):

        props = Properties()
        self.ActProp = props.Axis.ActProp
        self.SetProp = props.Axis.SetProp
        self.Guide   = props.Axis.Guide
        self.EStop   = props.Axis.EStop

    
    def pack(self,data):
        """
        Encodes the properties.
        """
        Data = data.copy()  # Create a copy to avoid modifying the original data

        # Implement packing logic here

        return Data
    
    def unpack(self, data):
        """
        Decodes the dictionary and populates internal properties.
        """
        def update_fields(obj, values: dict):
            for key, val in values.items():
                if hasattr(obj, key):
                    setattr(obj, key, val)

        if "ActProp" in data:
            update_fields(self.ActProp, data["ActProp"])
        if "SetProp" in data:
            update_fields(self.SetProp, data["SetProp"])
        if "Guide" in data:
            if "ActProp" in data["Guide"]:
                update_fields(self.Guide.ActProp, data["Guide"]["ActProp"])
            if "SetProp" in data["Guide"]:
                update_fields(self.Guide.SetProp, data["Guide"]["SetProp"])
        if "EStop" in data:
            update_fields(self.EStop, data["EStop"])

        return data  # optionally return the decoded dict too

    def __decode(self, data):
        """
        Decodes the error codes.
        
        :param data: The byte array to decode.
        """
        # Implement decoding logic here
        pass

    def to_dict(self, data):
        return {
            "ActProp": vars(self.ActProp),
            "SetProp": vars(self.SetProp),
            "Guide": {
                "ActProp": vars(self.Guide.ActProp),
                "SetProp": vars(self.Guide.SetProp),
            },
            "EStop": vars(self.EStop),
        }


    def check_connect(self, step_count=0):
        """ Varies each property value to simulate activity for GUI binding testing. """
        
        delta = 0.1 * math.sin(step_count / 10.0)

        # Numeric helpers
        def vary(x): return x + delta if isinstance(x, (int, float)) else x
        def toggle(b): return not b if isinstance(b, bool) else b

        # AxisActProp
        for field in vars(self.ActProp):
            val = getattr(self.ActProp, field)
            if isinstance(val, (float, int)):
                setattr(self.ActProp, field, vary(val))
            elif isinstance(val, bool):
                if step_count % 20 == 0:
                    setattr(self.ActProp, field, toggle(val))

        # AxisSetProp
        for field in vars(self.SetProp):
            val = getattr(self.SetProp, field)
            if isinstance(val, (float, int)):
                setattr(self.SetProp, field, vary(val))

        # Guide properties
        for field in vars(self.Guide.ActProp):
            val = getattr(self.Guide.ActProp, field)
            if isinstance(val, (float, int)):
                setattr(self.Guide.ActProp, field, vary(val))

        for field in vars(self.Guide.SetProp):
            val = getattr(self.Guide.SetProp, field)
            if isinstance(val, (float, int)):
                setattr(self.Guide.SetProp, field, vary(val))

        # EStopProp
        for field in vars(self.EStop):
            val = getattr(self.EStop, field)
            if isinstance(val, bool) and step_count % 5 == 0:
                setattr(self.EStop, field, toggle(val))

    def check_connect_ui(self, ui):
        """
        Writes the name of each data property into its corresponding widget, assuming naming like txtAccMax <- 'AccMax'.
        """
        def map_field_names(obj):
            for field in vars(obj):
                widget_name = "txt" + field
                widget = getattr(ui, widget_name, None)
                if widget and hasattr(widget, 'setText'):
                    widget.setText(field)

        map_field_names(self.ActProp)
        map_field_names(self.SetProp)
        map_field_names(self.Guide.ActProp)
        map_field_names(self.Guide.SetProp)
        map_field_names(self.EStop)
    
    
    pass
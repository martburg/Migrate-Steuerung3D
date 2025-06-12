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

    
    def pack(self, data):
        """
        Serialize SetProp into a legacy-style semicolon-delimited message string,
        exactly as expected by the PLC.
        """

        def get(d, key, default="0"):
            return str(d.get(key, default))

        ActProp = data.get("ActProp", {})
        SetProp = data.get("SetProp", {})
        GuideSetProp = data.get("Guide", {}).get("SetProp", {})

        # Use Modus from ActProp
        s = ";".join([
            get(data, "LifeTick", "1"),
            get(ActProp, "Modus", "r"),            # ✅ now correct
            get(ActProp, "OwnPID", "0000"),
            get(ActProp, "ControlingPIDTx", "0000"),
            get(ActProp, "Intent", "False"),
            get(ActProp, "Enable", "0"),
            get(GuideSetProp, "Control", "0"),
            get(ActProp, "SpeedSoll", "0.0"),
            get(GuideSetProp, "SpeedSoll", "0.0"),
            get(ActProp, "PosSoll", "0.0"),
            get(ActProp, "EStopReset", "0"),
            get(ActProp, "ReSync", "0"),
            get(data.get("EStop", {}), "GUINotHalt", "0"),
        ])

        if get(ActProp, "Modus", "r") == "w":
            s += ";" + ";".join([
                get(SetProp, "AccMove"),
                get(SetProp, "DccMax"),
                get(SetProp, "HardMax"),
                get(SetProp, "UserMax"),
                get(SetProp, "UserMin"),
                get(SetProp, "HardMin"),
                get(SetProp, "VelMax"),
                get(SetProp, "AccMax"),
                get(SetProp, "DccMax"),
                get(SetProp, "MaxAmp"),
                get(SetProp, "FilterP"),
                get(SetProp, "FilterI"),
                get(SetProp, "FilterD"),
                get(SetProp, "FilterIL"),
                get(GuideSetProp, "GuidePitch"),
                get(GuideSetProp, "GuidePosMax"),
                get(GuideSetProp, "GuidePosMin"),
                get(SetProp, "VelOrPos", "0"),
                get(SetProp, "PosWin"),
                get(SetProp, "VelWin"),
                get(SetProp, "AccTot"),
            ])

        s += ";EOD\\;"
        return s.encode("utf-8")

def unpack(self, raw):
    """
    Parse the PLC response string from shared memory or UDP reply.
    Updates internal ActProp and Guide.ActProp dictionaries.
    """
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8", errors="ignore")

    if not isinstance(raw, str) or not raw:
        return

    # Remove EOD and trailing semicolon, then split
    raw = raw.replace("EOD\\", "").strip(";")
    fields = raw.split(";")

    # Defensive: Expected number of fields is at least 38
    if len(fields) < 38:
        print("[Codec.unpack] Warning: short packet")
        return

    # Assign into ActProp and Guide.ActProp as needed
    ap = self.ActProp
    gp = self.Guide.ActProp

    try:
        ap.ControlPID       = fields[0]
        ap.LifetickUItx     = float(fields[1])
        ap.Status           = int(fields[2])
        ap.GuideStatus      = int(fields[3])
        ap.PosIst           = float(fields[4])
        ap.SpeedIstUI       = float(fields[5])
        ap.MasterMomentUI   = float(fields[6])
        ap.CabTemperatureUI = float(fields[7])
        ap.Name             = fields[8]
        ap.GearToUI         = float(fields[9])
        ap.HardMax          = float(fields[10])
        ap.UserMax          = float(fields[11])
        ap.UserMin          = float(fields[12])
        ap.HardMin          = float(fields[13])
        ap.VelMax           = float(fields[14])
        ap.AccMax           = float(fields[15])
        ap.DccMax           = float(fields[16])
        ap.MaxAmp           = float(fields[17])
        ap.FilterP          = float(fields[18])
        ap.FilterI          = float(fields[19])
        ap.FilterD          = float(fields[20])
        ap.FilterIL         = float(fields[21])
        ap.RopeSWLL         = float(fields[22])
        ap.RopeDiameter     = float(fields[23])
        ap.RopeType         = fields[24]
        ap.RopeNumber       = fields[25]
        ap.RopeLength       = float(fields[26])
        gp.GuidePitch       = float(fields[27])
        gp.GuidePosMax      = float(fields[28])
        gp.GuidePosMin      = float(fields[29])
        gp.GuidePosIstUI    = float(fields[30])
        gp.GuideIstSpeedUI  = float(fields[31])
        ap.MotAuslastUI     = float(fields[32])
        ap.ActCurUI         = float(fields[33])
        ap.SpeedMaxforUI    = float(fields[34])
        ap.PosDiffForUI     = float(fields[35])
        ap.RampenformUI     = int(fields[36])
        ap.EStopStatus      = int(fields[37])
    except Exception as e:
        print(f"[Codec.unpack] Parse error: {e}")


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
class WiFiRadio:
    """Represents a simulated Wi-Fi radio."""

    def __init__(
        self,
        enable=True,
        status="Up",
        channel=36,
        operating_frequency_band="5GHz",
    ):
        self.enable = enable
        self.status = status
        self.channel = channel
        self.operating_frequency_band = operating_frequency_band

class WiFi:
    """Represents the Wi-Fi subsystem of the virtual CPE."""

    def __init__(self, radio=None):
        self.radio = radio or WiFiRadio()
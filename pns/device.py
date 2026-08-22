import time
from pns.device_info import DeviceInfo

class Device:
    """Represents the virtual CPE."""

    def __init__(
            self,
            device_info = None
        ):

        self.device_info = device_info or DeviceInfo()
        self.start_time = time.time()

    def uptime(self):
        """Return device uptime in seconds."""
        return int(time.time() - self.start_time)

    def reboot(self):
        """Reset the simulated device uptime."""
        self.start_time = time.time()
import time

class Device:
    """Represents the virtual CPE."""

    def __init__(
            self,
            manufacturer="PNS",
            model="PNS-V100",
            serial_number="PNS-CPE-001",
            software_version="1.0.0",
        ):

        self.manufacturer = manufacturer
        self.mdoel = model
        self.serial_number = serial_number
        self.software_version = software_version
        self.start_time = time.time()

    def uptime(self):
        """Return device uptime in seconds."""
        return int(time.time() - self.start_time)

    def reboot(self):
        """Reset the simulated device uptime."""
        self.start_time = time.time()
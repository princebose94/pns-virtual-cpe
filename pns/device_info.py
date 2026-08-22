class DeviceInfo:
    """Represents basic information about the virtual CPE."""

    def __init__(
        self,
        manufacturer="PNS",
        model="PNS-V100",
        serial_number="PNS-CPE-001",
        software_version="1.0.0",
    ):
        self.manufacturer = manufacturer
        self.model = model
        self.serial_number = serial_number
        self.software_version = software_version
class ParameterNotFound(Exception):
    """Raised when a requested device parameter does not exist."""


class DataStore:
    """Provides access to the virtual CPE data model."""

    def __init__(self, device):
        self.device = device

    def get(self, parameter):
        """Return the value of a device parameter."""

        parameters = {
            "Device.DeviceInfo.Manufacturer":
                self.device.device_info.manufacturer,
            "Device.DeviceInfo.ModelName":
                self.device.device_info.model,
            "Device.DeviceInfo.SerialNumber":
                self.device.device_info.serial_number,
            "Device.DeviceInfo.SoftwareVersion":
                self.device.device_info.software_version,
        }

        if parameter not in parameters:
            raise ParameterNotFound(
                f"Parameter not found: {parameter}"
            )

        return parameters[parameter]

    def set(self, parameter, value):
        """Set the value of a device parameter."""

        if parameter == "Device.DeviceInfo.Manufacturer":
            self.device.device_info.manufacturer = value
        elif parameter == "Device.DeviceInfo.ModelName":
            self.device.device_info.model = value
        elif parameter == "Device.DeviceInfo.SerialNumber":
            self.device.device_info.serial_number = value
        elif parameter == "Device.DeviceInfo.SoftwareVersion":
            self.device.device_info.software_version = value
        else:
            raise ParameterNotFound(
                f"Parameter not found: {parameter}"
            )
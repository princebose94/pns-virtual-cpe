import pytest

from pns.device import Device
from pns.datastore import DataStore, ParameterNotFound


def test_get_device_model():
    device = Device()
    datastore = DataStore(device)

    assert datastore.get(
        "Device.DeviceInfo.ModelName"
    ) == "PNS-V100"


def test_get_serial_number():
    device = Device()
    datastore = DataStore(device)

    assert datastore.get(
        "Device.DeviceInfo.SerialNumber"
    ) == "PNS-CPE-001"


def test_get_software_version():
    device = Device()
    datastore = DataStore(device)

    assert datastore.get(
        "Device.DeviceInfo.SoftwareVersion"
    ) == "1.0.0"


def test_unknown_parameter():
    device = Device()
    datastore = DataStore(device)

    with pytest.raises(ParameterNotFound):
        datastore.get("Device.Unknown.Parameter")

def test_set_device_model():
    device = Device()
    datastore = DataStore(device)

    datastore.set(
        "Device.DeviceInfo.ModelName",
        "PNS-V200"
    )

    assert datastore.get(
        "Device.DeviceInfo.ModelName"
    ) == "PNS-V200"
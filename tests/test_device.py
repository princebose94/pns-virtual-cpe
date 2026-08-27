from pns.device import Device
from pns.device_info import DeviceInfo

def test_default_device():
    device  = Device()
    assert device.device_info.manufacturer == "PNS"
    assert device.device_info.model == "PNS-V100"
    assert device.device_info.serial_number == "PNS-CPE-001"
    assert device.device_info.software_version == "1.0.0"

def test_tplink_device():
    device_info = DeviceInfo(
        manufacturer="TP-Link",
        model="Archer-v1",
        serial_number="TPS-001"
    )

    device = Device(device_info=device_info)

    assert device.device_info.manufacturer == "TP-Link"
    assert device.device_info.model == "Archer-v1"
    assert device.device_info.serial_number == "TPS-001"

def test_sgc_device():
    device_info = DeviceInfo(
        manufacturer="SGC",
        model="SGC-5000",
        serial_number="SGC-001",
    )

    device = Device(device_info=device_info)

    assert device.device_info.manufacturer == "SGC"
    assert device.device_info.model == "SGC-5000"
    assert device.device_info.serial_number == "SGC-001"


def test_devices_are_independent():
    tplink_info = DeviceInfo(
        manufacturer="TP-Link",
        model="Archer-v1",
        serial_number="TPS-001"
    )

    sgc_info = DeviceInfo(
        manufacturer="SGC",
        model="SGC-5000",
        serial_number="SGC-001"
    )

    tplink = Device(device_info=tplink_info)
    sgc = Device(device_info=sgc_info)

    assert tplink is not sgc
    assert tplink.device_info is not sgc.device_info

    assert tplink.device_info.model == "Archer-v1"
    assert sgc.device_info.model == "SGC-5000"

def test_device_uptime():
    device = Device()
    assert device.uptime() >=0


def test_device_reboot():
    
    device = Device()

    old_start_time = device.start_time
    device.reboot()

    assert device.start_time >= old_start_time


def test_device_has_default_wifi():
    device = Device()

    assert device.wifi.radio.channel == 36
    assert device.wifi.radio.enable is True
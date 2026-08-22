from pns.device import Device

def test_device_info():
    device = Device()

    assert device.manufacturer == "PNS"
    assert device.mdoel == "PNS-V100"
    assert device.serial_number == "PNS-CPE-001"
    assert device.software_version == "1.0.0"


def test_device_uptime():
    device = Device()
    assert device.uptime() >=0


def test_device_reboot():
    device = Device()

    old_start_time = device.start_time
    device.reboot()

    assert device.start_time >= old_start_time
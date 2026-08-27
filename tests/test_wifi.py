from pns.wifi import WiFiRadio, WiFi


def test_default_wifi_radio():
    radio = WiFiRadio()

    assert radio.enable is True
    assert radio.status == "Up"
    assert radio.channel == 36
    assert radio.operating_frequency_band == "5GHz"


def test_custom_wifi_radio():
    radio = WiFiRadio(
        enable=False,
        status="Down",
        channel=44,
        operating_frequency_band="5GHz",
    )

    assert radio.enable is False
    assert radio.status == "Down"
    assert radio.channel == 44
    assert radio.operating_frequency_band == "5GHz"


def test_wifi_radios_are_independent():
    radio1 = WiFiRadio(channel=36)
    radio2 = WiFiRadio(channel=44)

    radio1.channel = 48

    assert radio1.channel == 48
    assert radio2.channel == 44


def test_default_wifi():
    wifi = WiFi()

    assert isinstance(wifi.radio, WiFiRadio)
    assert wifi.radio.channel == 36


def test_wifi_with_custom_radio():
    radio = WiFiRadio(channel=44)
    wifi = WiFi(radio=radio)

    assert wifi.radio.channel == 44
    assert wifi.radio is radio
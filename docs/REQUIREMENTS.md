# PNS Virtual CPE — Requirements Specification

**Version:** 0.1
**Status:** MVP
**Project:** PNS (Python Network Simulator)

## 1. Purpose

PNS is a Python-based virtual network device designed to simulate a manageable CPE (Customer Premises Equipment) for network-device testing and automation.

The primary goal is to provide a realistic, locally runnable test target that can be used to develop and validate device-testing automation without requiring physical network hardware.

PNS will eventually be used as the System Under Test (SUT) for a separate Robot Framework automation project.

## 2. Goals

The MVP shall:

* Represent a network device using a structured Python data model.
* Expose basic device information and state.
* Simulate Ethernet and Wi-Fi interfaces.
* Provide a device-management CLI.
* Allow external clients to connect to the device over TCP.
* Support reading and modifying selected device parameters.
* Support device reboot simulation.
* Provide predictable behavior suitable for automated testing.
* Be runnable locally on a standard Linux/macOS system.
* Provide unit tests for the simulator components.

## 3. Non-Goals

The MVP will not attempt to implement a complete physical or commercial CPE.

The following are outside the MVP scope:

* Actual Wi-Fi radio transmission.
* Actual Ethernet packet forwarding.
* Full routing functionality.
* NAT.
* DHCP server implementation.
* Full TR-181 compliance.
* TR-069 implementation.
* USP implementation.
* Real hardware interaction.
* Full operating-system emulation.
* REST API.
* Multi-device orchestration.

These capabilities may be considered in future versions.

## 4. Functional Requirements

### FR-01 — Device Identity

The simulator shall maintain the following device information:

* Manufacturer
* Model name
* Serial number
* Software/firmware version

Example:

```text
Manufacturer: PNS
Model: PNS-V100
Serial Number: PNS-CPE-001
Software Version: 1.0.0
```

### FR-02 — Device Uptime

The simulator shall maintain device uptime.

Uptime shall start when the virtual device starts and shall increase while the device is running.

### FR-03 — Device Reboot

The simulator shall support a reboot operation.

A reboot shall reset the simulated device uptime.

The MVP does not require an actual process restart.

### FR-04 — Ethernet Interface

The simulator shall provide at least one virtual Ethernet interface.

The interface shall maintain:

* Interface name
* Administrative state
* Operational status
* IP address
* MAC address

Example:

```text
eth0
Status: UP
IP: 192.168.1.1
MAC: 02:00:00:00:00:01
```

### FR-05 — Wi-Fi Interface

The simulator shall provide at least one virtual Wi-Fi radio/interface.

The radio shall maintain:

* Enable state
* Operational status
* Channel
* Operating frequency band

Example:

```text
Radio: 1
Status: UP
Channel: 36
Band: 5GHz
```

### FR-06 — Device Data Model

The simulator shall expose device parameters through a hierarchical data model.

The initial model shall be inspired by the Broadband Forum TR-181 Device Data Model but shall not claim full TR-181 compliance.

The initial hierarchy shall include:

```text
Device.
├── DeviceInfo.
├── Ethernet.
│   └── Interface.1.
└── WiFi.
    └── Radio.1.
```

### FR-07 — Parameter Read

The simulator shall allow a client to retrieve the value of a device parameter.

Example:

```text
get Device.DeviceInfo.SerialNumber
```

Expected response:

```text
PNS-CPE-001
```

### FR-08 — Parameter Modification

The simulator shall allow supported parameters to be modified.

Example:

```text
set Device.WiFi.Radio.1.Channel 44
```

Expected response:

```text
OK
```

The new value shall remain available until the device is rebooted or otherwise reset.

### FR-09 — Command-Line Interface

The simulator shall provide an interactive management CLI.

The initial command set shall include:

```text
help
show device
show interface
get <parameter>
set <parameter> <value>
reboot
exit
```

### FR-10 — Remote Management Connection

The CLI shall be accessible through a TCP connection.

The MVP shall use a configurable TCP port.

The default port shall be:

```text
5000
```

### FR-11 — Multiple Client Connections

The simulator should support more than one client connection without crashing the device process.

Advanced concurrent-session behavior is outside the initial MVP.

### FR-12 — Invalid Commands

The simulator shall return a meaningful error when an unsupported command is received.

Example:

```text
PNS> foo
ERROR: Unknown command
```

### FR-13 — Invalid Parameters

The simulator shall return a meaningful error when a client attempts to access an unsupported parameter.

Example:

```text
PNS> get Device.Unknown.Parameter
ERROR: Parameter not found
```

### FR-14 — Invalid Parameter Values

The simulator shall reject invalid values for parameters that have defined constraints.

Example:

```text
PNS> set Device.WiFi.Radio.1.Channel abc
ERROR: Invalid value
```

### FR-15 — Configuration

Basic device configuration shall be loaded from a configuration file.

The configuration shall allow values such as:

* Device name
* Model
* Serial number
* Firmware version
* Management port

to be customized without modifying Python source code.

## 5. Non-Functional Requirements

### NFR-01 — Platform

The simulator should run on:

* macOS
* Linux

Windows support may be considered later.

### NFR-02 — Python

The simulator shall be implemented in Python.

The initial implementation should minimize external dependencies.

### NFR-03 — Testability

Simulator components shall be independently testable using pytest.

### NFR-04 — Deterministic Behavior

The simulator shall provide predictable responses for identical inputs.

This is important because the primary consumer of PNS will be automated test suites.

### NFR-05 — Logging

The simulator shall provide basic logging for:

* Device startup
* Client connections
* Commands received
* Configuration changes
* Reboot events
* Errors

### NFR-06 — Maintainability

The implementation shall separate:

* Device model
* Data model
* Command processing
* Network communication
* Configuration
* Logging

### NFR-07 — Documentation

The repository shall contain sufficient documentation for a new developer to:

1. Clone the repository.
2. Create the Python environment.
3. Start the simulator.
4. Connect to the simulator.
5. Execute basic commands.
6. Run the automated tests.

## 6. MVP Acceptance Criteria

PNS MVP shall be considered complete when a developer can:

1. Clone the public GitHub repository.
2. Install the required Python dependencies.
3. Start the virtual CPE locally.
4. Connect to the CPE using a TCP client.
5. Display device information.
6. Display interface information.
7. Read supported device parameters.
8. Modify supported parameters.
9. Reboot the simulated device.
10. Observe the uptime reset after reboot.
11. Receive meaningful errors for invalid commands and parameters.
12. Run the complete pytest suite successfully.

## 7. Future Requirements

Potential future versions may introduce:

* Dual-band Wi-Fi radios.
* Wi-Fi clients/stations.
* WAN/LAN interfaces.
* DHCP simulation.
* Routing table simulation.
* VLAN support.
* IPv4/IPv6 configuration.
* Packet counters.
* Traffic statistics.
* Fault injection.
* Deliberate command failures.
* REST API.
* NETCONF-like management.
* TR-069/USP-inspired management.
* Multiple virtual CPE instances.
* Containerized deployment.
* Remote test-lab deployment.

## 8. Relationship With Automation Project

PNS is intentionally designed as a separate System Under Test.

A separate repository will contain the automation framework:

```text
pns-virtual-cpe
        │
        │ TCP / management interface
        ▼
pns-robot-tests
```

The automation repository shall interact with PNS through its externally exposed interfaces rather than importing internal PNS implementation modules.

This separation is intended to mimic a real device-testing environment where the automation framework communicates with a device under test.

## 9. MVP Version

The first public release shall be identified as:

```text
v0.1.0
```

The focus of v0.1.0 is a small, reliable, remotely manageable virtual CPE that can serve as a target for automated device testing.

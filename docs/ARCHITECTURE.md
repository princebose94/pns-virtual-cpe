# PNS Virtual CPE — Architecture

**Version:** 0.1
**Status:** MVP

## 1. Overview

PNS is a Python-based virtual CPE designed to act as a System Under Test (SUT) for network-device automation.

The architecture separates the virtual device's internal state from the interfaces used to manage it.

The primary components are:

```text
                     PNS Virtual CPE
                           │
                  ┌────────▼────────┐
                  │   TCP Server    │
                  └────────┬────────┘
                           │
                  ┌────────▼────────┐
                  │   CLI Handler   │
                  └────────┬────────┘
                           │
                  ┌────────▼────────┐
                  │ Command Parser  │
                  └────────┬────────┘
                           │
                  ┌────────▼────────┐
                  │   Data Model    │
                  └────────┬────────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
         DeviceInfo    Ethernet       WiFi
```

## 2. Design Principles

### 2.1 Separation of Concerns

Each component shall have one primary responsibility.

```text
TCP Server
    ↓
network communication

CLI Handler
    ↓
session management

Command Parser
    ↓
interpret commands

Data Model
    ↓
represent device state

Device Components
    ↓
represent individual device subsystems
```

A network connection should not directly manipulate internal device attributes.

For example, the TCP server should not perform:

```python
device.wifi_radio["channel"] = 44
```

Instead, it should pass the requested operation to the data-model layer:

```text
set Device.WiFi.Radio.1.Channel 44
                    │
                    ▼
              Data Model
                    │
                    ▼
               WiFi Radio
```

This keeps the simulator modular.

## 3. Component Architecture

### 3.1 Device Model

The device model represents the overall virtual CPE.

Responsibilities:

* Maintain device identity.
* Maintain device state.
* Maintain uptime.
* Handle reboot.
* Provide access to device subsystems.

Conceptually:

```text
Device
│
├── DeviceInfo
├── Ethernet
└── WiFi
```

The `Device` object represents the virtual CPE as a whole.

## 4. Device Information

The Device Information component maintains static or semi-static device attributes.

```text
Device.DeviceInfo
├── Manufacturer
├── ModelName
├── SerialNumber
└── SoftwareVersion
```

Example:

```text
Manufacturer: PNS
ModelName: PNS-V100
SerialNumber: PNS-CPE-001
SoftwareVersion: 1.0.0
```

## 5. Ethernet Model

The Ethernet component represents virtual Ethernet interfaces.

```text
Device.Ethernet
└── Interface.1
    ├── Enable
    ├── Status
    ├── IPAddress
    └── MACAddress
```

The MVP does not perform real Ethernet packet processing.

The interface exists as a simulated device object that can be inspected and configured.

## 6. Wi-Fi Model

The Wi-Fi component represents virtual Wi-Fi radios.

```text
Device.WiFi
└── Radio.1
    ├── Enable
    ├── Status
    ├── Channel
    └── OperatingFrequencyBand
```

The MVP does not transmit real Wi-Fi frames.

The Wi-Fi subsystem exists to provide a realistic management and testing target.

## 7. Data Model

The data model provides a common interface for accessing device parameters.

The initial hierarchy is inspired by the Broadband Forum TR-181 Device Data Model.

PNS does not claim full TR-181 compliance.

Example parameter:

```text
Device.WiFi.Radio.1.Channel
```

The data model shall support:

```text
GET parameter
SET parameter value
```

Conceptually:

```text
get("Device.WiFi.Radio.1.Channel")
            │
            ▼
       Data Model
            │
            ▼
       WiFi.Radio.1
            │
            ▼
          36
```

And:

```text
set("Device.WiFi.Radio.1.Channel", 44)
            │
            ▼
       Data Model
            │
            ▼
       WiFi.Radio.1
            │
            ▼
        Channel = 44
```

## 8. Command Layer

The command layer converts textual CLI commands into operations on the data model.

Example:

```text
PNS> get Device.DeviceInfo.SerialNumber
```

Processing flow:

```text
CLI text
   │
   ▼
Command Parser
   │
   ▼
GET operation
   │
   ▼
Data Model
   │
   ▼
Device.DeviceInfo.SerialNumber
   │
   ▼
PNS-CPE-001
```

Supported MVP commands:

```text
help
show device
show interface
get <parameter>
set <parameter> <value>
reboot
exit
```

## 9. TCP Server

The TCP server provides remote access to the virtual CPE.

Default port:

```text
5000
```

Example:

```text
                 TCP
Test Client ───────────────► PNS
                              │
                              ▼
                         CLI Handler
```

A client should be able to connect using a standard TCP client.

For example:

```bash
telnet localhost 5000
```

The TCP server is responsible for:

* Accepting connections.
* Creating client sessions.
* Receiving commands.
* Passing commands to the CLI layer.
* Returning responses.
* Closing sessions.

The TCP server shall not contain device-management logic.

## 10. Client Session

Each TCP connection represents a management session.

Conceptually:

```text
Client
  │
  ▼
TCP Connection
  │
  ▼
Session
  │
  ├── receive command
  ├── process command
  └── return response
```

The MVP may initially process sessions sequentially. Concurrent client handling can be improved in a later version.

## 11. Error Handling

Errors shall be handled at the appropriate layer.

Examples:

```text
Unknown command
Unknown parameter
Invalid parameter value
Invalid command syntax
```

Example:

```text
PNS> get Device.Unknown.Parameter

ERROR: Parameter not found
```

The simulator should return predictable error messages because the automation framework will eventually validate them.

## 12. Configuration

Configuration will eventually be externalized from the Python source code.

Potential configuration:

```text
Device Name
Model
Serial Number
Software Version
Management Port
```

For the initial architecture, configuration is considered a separate concern from the device model.

## 13. Logging

Logging will be implemented as a separate component.

Potential events:

```text
Device started
Client connected
Client disconnected
Command received
Parameter changed
Device rebooted
Error occurred
```

Logging shall not be mixed with command-processing logic.

## 14. Proposed Python Structure

The architecture maps to the following project structure:

```text
pns-virtual-cpe/
│
├── README.md
├── requirements.txt
│
├── docs/
│   ├── REQUIREMENTS.md
│   └── ARCHITECTURE.md
│
├── pns/
│   ├── __init__.py
│   ├── device.py
│   ├── datastore.py
│   ├── cli.py
│   ├── server.py
│   └── logger.py
│
├── config/
│   └── device.json
│
├── scripts/
│   └── start_pns.py
│
└── tests/
    ├── test_device.py
    ├── test_datastore.py
    ├── test_cli.py
    └── test_server.py
```

The implementation may evolve as the project grows.

## 15. External Interface Boundary

The most important architectural boundary is between PNS and the automation framework.

```text
┌─────────────────────────┐
│   pns-robot-tests       │
│                         │
│ Robot Framework         │
│ Python libraries        │
└────────────┬────────────┘
             │
             │ TCP / CLI
             │
═════════════╪══════════════════  System boundary
             │
┌────────────▼────────────┐
│   pns-virtual-cpe       │
│                         │
│ TCP Server              │
│ CLI                     │
│ Data Model              │
│ Virtual Device          │
└─────────────────────────┘
```

The automation repository should communicate with PNS through its externally exposed interfaces.

It should not import:

```python
from pns.device import Device
```

This separation intentionally mimics real device testing, where the automation system communicates with a remote System Under Test.

## 16. Future Architecture

The architecture should allow additional management interfaces to be added without replacing the underlying device model.

Future possibilities:

```text
                       Device Model
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
        CLI                REST             NETCONF
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
                            ▼
                     Virtual CPE
```

Additional simulated subsystems may also be added:

```text
Device
│
├── DeviceInfo
├── Ethernet
├── WiFi
├── Routing
├── DHCP
├── VLAN
├── WAN
└── Statistics
```

These should be introduced incrementally rather than implemented as part of the MVP.

## 17. Architectural Goal

The final goal of PNS is not to emulate every aspect of a real router.

The goal is to provide a sufficiently realistic, deterministic and externally manageable virtual CPE that allows network-device test automation to be developed and executed without requiring physical CPE hardware.

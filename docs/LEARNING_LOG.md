# PNS Learning Log

## 22 August 2026

### What I worked on

Started implementing the PNS Virtual CPE after completing the initial requirements and architecture documentation.

### What I learned

#### Python OOP

Learned the difference between a class and an object.

- A class is a blueprint.
- An object is an instance created from that class.
- `self` refers to the current object.
- Attributes represent object state.
- Methods represent object behavior.

Implemented the initial `Device` class with:

- Manufacturer
- Model
- Serial number
- Software version
- Uptime
- Reboot

#### Encapsulation

Started understanding why state and behavior belonging to a device should be grouped together inside a `Device` object.

#### Composition

Refactored the device model to introduce `DeviceInfo`.

Instead of putting all device information directly inside `Device`:

```text
    Device
    ├── manufacturer
    ├── model
    └── serial number
```
the model now uses composition:

    Device
    └── DeviceInfo
        ├── manufacturer
        ├── model
        └── serial number

Learned the distinction between:

- "is-a" → inheritance
- "has-a" → composition

For the PNS device model, composition is more appropriate.

#### Multiple object instances

Created two different `Device` objects using the same `Device` class:

- TP-Link
- SGC

Each device has its own `DeviceInfo` and therefore its own state.

#### Python `or` expression

Learned how:

    self.device_info = device_info or DeviceInfo()

works.

It means:

> Use the supplied `DeviceInfo` object; otherwise create a default one.

Also learned about truthy/falsy values and short-circuit evaluation.

#### Python project structure

Encountered and fixed a package import problem while running pytest.

Learned about:

- `__init__.py`
- Python packages
- `pyproject.toml`
- editable installation using `pip install -e .`
- pytest configuration
- `.gitignore`
- generated `*.egg-info` directories

### Testing

Current test result:

    6 passed

### Current architecture

    Device
    └── DeviceInfo

### Next

Implement an Ethernet interface model and learn how multiple component objects can be composed inside the virtual CPE.
# pyAKMotorCtrl

Python library to control the AK60-6 motor via CAN in servo mode.

## Features

- Full servo mode support (duty cycle, current, velocity, position control)
- Type-safe API with comprehensive type hints
- Simple, minimal interface
- Tested with pytest

## Installation

This project uses [uv](https://docs.astral.sh/uv/) for dependency management. If you don't have uv installed:

```bash
# Install uv (Linux/macOS)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using pip
pip install uv
```

### Install the library

```bash
# Clone the repository
git clone https://github.com/Robotics-Technology/PyLSS.git
cd PyLSS

# Install dependencies
uv sync

# Or install in development mode with all dependencies
uv sync --all-groups
```

## Usage

### Basic Example

```python
import can
from pyakmotorctrl import AK60_6Motor

# Initialize CAN bus
bus = can.Bus(interface="socketcan", channel="can0", bitrate=1000000)

# Create motor instance (motor ID 0x68)
motor = AK60_6Motor(motor_id=0x68, bus=bus)

# Move to position
motor.set_position(180.0)  # Move to 180 degrees

# Read motor status
status = motor.read_status()
if status:
    print(f"Position: {status['position']:.1f}°")
    print(f"Speed: {status['speed']:.0f} ERPM")
    print(f"Current: {status['current']:.2f} A")
    print(f"Temperature: {status['temperature']}°C")

bus.shutdown()
```

## Running Examples

```bash
# Basic position control example
uv run examples/basic_position_control.py
```

## Testing

```bash
# Run all tests
uv run pytest

# Type checking
uv run ty check
```

## Development

```bash
# Install with dev dependencies
uv sync --group dev

# Run tests
uv run pytest

# Run type checker
uv run ty check

# Run linter
uv run ruff check
```

## License

LGPL-3.0-or-later

## Documentation Reference

Based on the CubeMars AK Series Module Product Manual V3.0.1.

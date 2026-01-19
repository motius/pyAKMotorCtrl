from enum import IntEnum
from typing import Optional
import struct
import can
from can import BusABC


class ServoMode(IntEnum):
    DUTY_CYCLE = 0
    CURRENT_LOOP = 1
    CURRENT_BRAKE = 2
    VELOCITY_LOOP = 3
    POSITION_LOOP = 4
    SET_ORIGIN = 5
    POSITION_VELOCITY_LOOP = 6


class AK60_6Motor:
    def __init__(self, motor_id: int, bus: BusABC):
        if not 0 <= motor_id <= 0xFF:
            raise ValueError("motor_id must be between 0 and 255")
        self.motor_id = motor_id
        self.bus = bus

    def _send_command(self, mode: ServoMode, data: bytes) -> None:
        arbitration_id = (mode << 8) | self.motor_id
        msg = can.Message(
            arbitration_id=arbitration_id,
            data=data,
            is_extended_id=True,
        )
        self.bus.send(msg)

    def set_duty_cycle(self, duty: float) -> None:
        if not -1.0 <= duty <= 1.0:
            raise ValueError("duty must be between -1.0 and 1.0")
        value = int(duty * 100000)
        data = struct.pack(">i", value)
        self._send_command(ServoMode.DUTY_CYCLE, data)

    def set_current(self, current: float) -> None:
        value = int(current * 1000)
        data = struct.pack(">i", value)
        self._send_command(ServoMode.CURRENT_LOOP, data)

    def set_brake_current(self, current: float) -> None:
        if current < 0:
            raise ValueError("brake current must be non-negative")
        value = int(current * 1000)
        data = struct.pack(">i", value)
        self._send_command(ServoMode.CURRENT_BRAKE, data)

    def set_velocity(self, rpm: float) -> None:
        value = int(rpm)
        data = struct.pack(">i", value)
        self._send_command(ServoMode.VELOCITY_LOOP, data)

    def set_position(self, degrees: float) -> None:
        if not -36000 <= degrees <= 36000:
            raise ValueError("position must be between -36000 and 36000 degrees")
        value = int(degrees * 10000)
        data = struct.pack(">i", value)
        self._send_command(ServoMode.POSITION_LOOP, data)

    def set_origin(self, permanent: bool = False) -> None:
        data = bytes([1 if permanent else 0])
        self._send_command(ServoMode.SET_ORIGIN, data)

    def set_position_velocity(
        self, degrees: float, rpm: int, acceleration: int
    ) -> None:
        if not -36000 <= degrees <= 36000:
            raise ValueError("position must be between -36000 and 36000 degrees")
        pos_value = int(degrees * 10000)
        spd_value = int(rpm / 10)
        acc_value = int(acceleration / 10)
        data = struct.pack(">ihh", pos_value, spd_value, acc_value)
        self._send_command(ServoMode.POSITION_VELOCITY_LOOP, data)

    def read_status(self, timeout: Optional[float] = 0.1) -> Optional[dict]:
        msg = self.bus.recv(timeout=timeout)
        if msg is None or len(msg.data) < 8:
            return None

        position = struct.unpack(">h", msg.data[0:2])[0] * 0.1
        speed = struct.unpack(">h", msg.data[2:4])[0] * 10.0
        current = struct.unpack(">h", msg.data[4:6])[0] * 0.01
        temperature = struct.unpack("b", msg.data[6:7])[0]
        error_code = msg.data[7]

        return {
            "position": position,
            "speed": speed,
            "current": current,
            "temperature": temperature,
            "error_code": error_code,
        }

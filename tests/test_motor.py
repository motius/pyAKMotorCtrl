import pytest
from unittest.mock import Mock
import struct
from pyakmotorctrl import AK60_6Motor, ServoMode


@pytest.fixture
def mock_bus():
    return Mock()


@pytest.fixture
def motor(mock_bus):
    return AK60_6Motor(motor_id=0x68, bus=mock_bus)


def test_motor_id_validation():
    mock_bus = Mock()
    with pytest.raises(ValueError):
        AK60_6Motor(motor_id=-1, bus=mock_bus)
    with pytest.raises(ValueError):
        AK60_6Motor(motor_id=256, bus=mock_bus)


def test_set_duty_cycle(motor, mock_bus):
    motor.set_duty_cycle(0.2)
    expected_data = struct.pack(">i", 20000)
    expected_id = (ServoMode.DUTY_CYCLE << 8) | 0x68
    mock_bus.send.assert_called_once()
    msg = mock_bus.send.call_args[0][0]
    assert msg.arbitration_id == expected_id
    assert msg.data == expected_data
    assert msg.is_extended_id is True


def test_set_duty_cycle_validation(motor):
    with pytest.raises(ValueError):
        motor.set_duty_cycle(1.5)
    with pytest.raises(ValueError):
        motor.set_duty_cycle(-1.5)


def test_set_current(motor, mock_bus):
    motor.set_current(5.0)
    expected_data = struct.pack(">i", 5000)
    expected_id = (ServoMode.CURRENT_LOOP << 8) | 0x68
    msg = mock_bus.send.call_args[0][0]
    assert msg.arbitration_id == expected_id
    assert msg.data == expected_data


def test_set_brake_current(motor, mock_bus):
    motor.set_brake_current(5.0)
    expected_data = struct.pack(">i", 5000)
    expected_id = (ServoMode.CURRENT_BRAKE << 8) | 0x68
    msg = mock_bus.send.call_args[0][0]
    assert msg.arbitration_id == expected_id
    assert msg.data == expected_data


def test_set_brake_current_validation(motor):
    with pytest.raises(ValueError):
        motor.set_brake_current(-1.0)


def test_set_velocity(motor, mock_bus):
    motor.set_velocity(1000.0)
    expected_data = struct.pack(">i", 1000)
    expected_id = (ServoMode.VELOCITY_LOOP << 8) | 0x68
    msg = mock_bus.send.call_args[0][0]
    assert msg.arbitration_id == expected_id
    assert msg.data == expected_data


def test_set_position(motor, mock_bus):
    motor.set_position(180.0)
    expected_data = struct.pack(">i", 1800000)
    expected_id = (ServoMode.POSITION_LOOP << 8) | 0x68
    msg = mock_bus.send.call_args[0][0]
    assert msg.arbitration_id == expected_id
    assert msg.data == expected_data


def test_set_position_validation(motor):
    with pytest.raises(ValueError):
        motor.set_position(40000)
    with pytest.raises(ValueError):
        motor.set_position(-40000)


def test_set_origin_temporary(motor, mock_bus):
    motor.set_origin(permanent=False)
    expected_id = (ServoMode.SET_ORIGIN << 8) | 0x68
    msg = mock_bus.send.call_args[0][0]
    assert msg.arbitration_id == expected_id
    assert msg.data == b"\x00"


def test_set_origin_permanent(motor, mock_bus):
    motor.set_origin(permanent=True)
    expected_id = (ServoMode.SET_ORIGIN << 8) | 0x68
    msg = mock_bus.send.call_args[0][0]
    assert msg.arbitration_id == expected_id
    assert msg.data == b"\x01"


def test_set_position_velocity(motor, mock_bus):
    motor.set_position_velocity(degrees=180.0, rpm=5000, acceleration=30000)
    expected_data = struct.pack(">ihh", 1800000, 500, 3000)
    expected_id = (ServoMode.POSITION_VELOCITY_LOOP << 8) | 0x68
    msg = mock_bus.send.call_args[0][0]
    assert msg.arbitration_id == expected_id
    assert msg.data == expected_data


def test_read_status(motor, mock_bus):
    test_data = struct.pack(">hhh", 1800, 1000, 500) + bytes([25, 0])
    mock_msg = Mock()
    mock_msg.data = test_data
    mock_bus.recv.return_value = mock_msg

    status = motor.read_status()
    assert status is not None
    assert status["position"] == pytest.approx(180.0)
    assert status["speed"] == pytest.approx(10000.0)
    assert status["current"] == pytest.approx(5.0)
    assert status["temperature"] == 25
    assert status["error_code"] == 0


def test_read_status_timeout(motor, mock_bus):
    mock_bus.recv.return_value = None
    status = motor.read_status()
    assert status is None

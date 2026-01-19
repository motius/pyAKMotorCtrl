import can
from pyakmotorctrl import AK60_6Motor


def main() -> None:
    bus = can.Bus(interface="socketcan", channel="can0", bitrate=1000000)
    motor = AK60_6Motor(motor_id=0x68, bus=bus)

    motor.set_position(180.0)
    status = motor.read_status()
    if status:
        print(f"Position: {status['position']:.1f}°")
        print(f"Speed: {status['speed']:.0f} ERPM")
        print(f"Current: {status['current']:.2f} A")
        print(f"Temperature: {status['temperature']}°C")

    bus.shutdown()


if __name__ == "__main__":
    main()

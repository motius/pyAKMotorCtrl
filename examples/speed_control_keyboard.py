import can
import sys
import tty
import termios
import select
from pyakmotorctrl import AK60_6Motor


def main() -> None:
    bus = can.Bus(interface="socketcan", channel="can1", bitrate=1000000)
    motor = AK60_6Motor(motor_id=1, bus=bus)

    current_speed = 0

    print("Speed Control Example")
    print("Up Arrow: Increase speed by 1 RPM")
    print("Down Arrow: Decrease speed by 1 RPM")
    print("q: Exit")
    print(f"\nCurrent speed: {current_speed} RPM")

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        running = True

        while running:
            motor.set_velocity(current_speed)

            if select.select([sys.stdin], [], [], 0.05)[0]:
                ch = sys.stdin.read(1)

                if ch == "\x1b":
                    ch2 = sys.stdin.read(2)
                    if ch2 == "[A":
                        current_speed += 10
                        print(
                            f"\rCurrent speed: {current_speed} RPM    ",
                            end="",
                            flush=True,
                        )
                    elif ch2 == "[B":
                        current_speed -= 10
                        print(
                            f"\rCurrent speed: {current_speed} RPM    ",
                            end="",
                            flush=True,
                        )
                elif ch == "q" or ch == "Q":
                    print("\n\n\rStopping motor...")
                    motor.set_velocity(0)
                    running = False

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    bus.shutdown()
    print("\rExited.")


if __name__ == "__main__":
    main()

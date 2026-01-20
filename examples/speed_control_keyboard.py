import can
from pyakmotorctrl import AK60_6Motor
from pynput import keyboard


def main() -> None:
    bus = can.Bus(interface="socketcan", channel="can1", bitrate=1000000)
    motor = AK60_6Motor(motor_id=1, bus=bus)

    current_speed = 0

    print("Speed Control Example")
    print("Up Arrow: Increase speed by 1 RPM")
    print("Down Arrow: Decrease speed by 1 RPM")
    print("ESC: Exit")
    print(f"\nCurrent speed: {current_speed} RPM")

    def on_press(key):
        nonlocal current_speed

        if key == keyboard.Key.up:
            current_speed += 1
            motor.set_velocity(current_speed)
            print(f"Current speed: {current_speed} RPM")

        elif key == keyboard.Key.down:
            current_speed -= 1
            motor.set_velocity(current_speed)
            print(f"Current speed: {current_speed} RPM")

        elif key == keyboard.Key.esc:
            print("\nStopping motor...")
            motor.set_velocity(0)
            return False

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    bus.shutdown()


if __name__ == "__main__":
    main()

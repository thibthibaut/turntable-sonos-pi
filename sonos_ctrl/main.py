import socket
import soco
import logging
from gpiozero import Button

logging.basicConfig(level=logging.INFO)

LOCAL_NETWORK = "192.168.1.1"
MAIN_SONOS_ZONE = "Dining Room"
STREAM_NAME = "turntable.mp3.m3u"
BUTTON = Button(26)


def get_local_ip():
    """
    Get local IP address to infer radio stream URL
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connect to a dummy IP to get the local IP address
        s.connect((LOCAL_NETWORK, 1))
        ip = s.getsockname()[0]
    except Exception:
        logging.error("Unable to get local IP")
        exit(1)
    finally:
        s.close()
    return ip


if __name__ == "__main__":
    local_ip = get_local_ip()
    turntable_uri = f"http://{local_ip}:8000/{STREAM_NAME}"
    logging.info(f"Turntable URI: {turntable_uri}")

    while True:
        BUTTON.wait_for_press()

        devices = {device.player_name: device for device in soco.discover()}

        logging.info(f"Devices: {devices}")

        devices[MAIN_SONOS_ZONE].partymode()
        devices[MAIN_SONOS_ZONE].play_uri(turntable_uri)

        for _device_name, device in devices.items():
            device.ramp_to_volume(30, ramp_type="AUTOPLAY_RAMP_TYPE")

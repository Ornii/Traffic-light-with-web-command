from pathlib import Path

from config.config import AppConfig
from led.state import LedState
from network.tcp import TcpClient

BASE_DIR = str(Path(__file__).parent.resolve())
CONFIG_PATH = BASE_DIR + r"\config.yaml"

def main():
    config = AppConfig.load_from_yaml(CONFIG_PATH)
    led_state = LedState()
    tcp_client = TcpClient(led_state)
    tcp_client.start_connection(config.tcp_server_addr, config.tcp_port)


if __name__ == "__main__":
    main()




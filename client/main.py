from config.config import AppConfig
from led.state import LedState
from network.tcp import TcpClient


def main():
    config = AppConfig.load_from_yaml("config.yaml")
    led_state = LedState()
    tcp_client = TcpClient(led_state, config.tcp_port)
    tcp_client.start_connection(config.tcp_server_addr, config.tcp_port)


if __name__ == "__main__":
    main()

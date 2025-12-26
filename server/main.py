import threading
import time

from api.routes import register_routes
from config.config import AppConfig
from led.state import LedState
from network.tcp import TcpServer

from flask import Flask


def main():
    config = AppConfig.load_from_yaml("config.yaml")
    led_state = LedState()
    tcp_server = TcpServer(led_state, config.tcp_port)

    threading.Thread(
        target=tcp_server.start_server, daemon=True, name="TCP-Server"
    ).start()

    while not tcp_server.is_client_connected:
        time.sleep(0.5)

    app = Flask(__name__)
    register_routes(app, led_state, tcp_server, config.hide_flask_logs)

    app.run(
        host=config.web_addr,
        port=config.web_port,
        debug=config.web_debug,
        use_reloader=False,
    )


if __name__ == "__main__":
    main()

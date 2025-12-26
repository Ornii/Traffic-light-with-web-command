import logging
import sys

import led.display
from led.state import LedState
from network.tcp import TcpServer

from flask import Flask, jsonify, render_template, request


def hide_flask_logs() -> None:
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)
    cli = sys.modules["flask.cli"]
    cli.show_server_banner = lambda *x: None


def register_routes(
    app: Flask, led_state: LedState, tcp_server: TcpServer, hide_logs: bool = True
) -> None:
    if hide_logs:
        hide_flask_logs()

    @app.route("/")
    def index():
        return render_template(r"index.html")

    @app.route("/api/define_state", methods=["POST"])
    def set_led_state():
        dictionary_received = request.get_json()
        # {"green_led_state": int_green_led_state,"red_led_state": int_red_led_state}

        green = dictionary_received["green_led_state"]
        red = dictionary_received["red_led_state"]

        if green not in [0, 1] or red not in [0, 1]:
            return jsonify({"error": "Invalid LED state"}), 400

        led_state.set_state(green, red)
        led.display.print_led_state(led_state)

        try:
            tcp_server.conn.sendall(tcp_server.encode_led_state())
        except ConnectionResetError:
            tcp_server.is_client_connected = False

        print("Green LED state (0/1): ")
        return jsonify(None)

    @app.route("/api/get_state", methods=["GET"])
    def get_led_state():
        return jsonify(
            {
                "green_led_state": led_state.green,
                "red_led_state": led_state.red,
            }
        )

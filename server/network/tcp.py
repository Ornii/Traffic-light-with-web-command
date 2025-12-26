import socket
import threading

from led.display import print_led_state
from led.state import LedState

PACKET_GREEN_RED = b"0111"
PACKET_GREEN_ONLY = b"0110"
PACKET_RED_ONLY = b"0011"
PACKET_ALL_OFF = b"0010"


class TcpServer:
    def __init__(self, led_state: LedState, server_port: int = 1234):
        self.led_state = led_state
        self.is_client_connected: bool = False
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("", server_port))
        self.socket.listen()

    def encode_led_state(self) -> bytes:
        if self.led_state.green == 1 and self.led_state.red == 1:
            return PACKET_GREEN_RED
        elif self.led_state.green == 0 and self.led_state.red == 1:
            return PACKET_RED_ONLY
        elif self.led_state.green == 0 and self.led_state.red == 0:
            return PACKET_ALL_OFF
        else:
            return PACKET_GREEN_ONLY

    def decode_led_state(self, packet: bytes) -> None:
        if packet == PACKET_GREEN_RED:
            self.led_state.set_state(1, 1)
        elif packet == PACKET_GREEN_ONLY:
            self.led_state.set_state(1, 0)
        elif packet == PACKET_RED_ONLY:
            self.led_state.set_state(0, 1)
        elif packet == PACKET_ALL_OFF:
            self.led_state.set_state(0, 0)

    def send_loop(self) -> None:
        try:
            while True:
                green_user_input = input("Green LED state (0/1): \n")
                if green_user_input not in ["0", "1"]:
                    print("Please enter 0 or 1")
                    continue
                if green_user_input == "1":
                    self.led_state.turn_green_on()
                else:
                    self.led_state.turn_red_on()

                print_led_state(self.led_state)
                self.conn.sendall(self.encode_led_state())

        except ConnectionResetError:
            self.is_client_connected = False

    def receive_loop(self) -> None:
        try:
            while True:
                packet = self.conn.recv(64)
                if len(packet) > 0:
                    self.decode_led_state(packet)
                    print_led_state(self.led_state)
                    print("Green LED state (0/1): ")
        except ConnectionResetError:
            self.is_client_connected = False

    def start_server(self) -> None:
        while True:
            if not self.is_client_connected:
                print("Waiting for TCP client...")
                self.conn, addr = self.socket.accept()
                self.is_client_connected = True
                print(f"\033[35mConnected with {addr[0]}\033[37m")

                threading.Thread(
                    target=self.send_loop,
                    daemon=True,
                    name="TCP-Sender",
                ).start()
                threading.Thread(
                    target=self.receive_loop,
                    daemon=True,
                    name="TCP-Receiver",
                ).start()

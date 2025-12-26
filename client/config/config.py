import yaml


class AppConfig:
    def __init__(self, tcp: dict):
        self.tcp_server_addr = tcp.get("server_address", "0.0.0.0")
        self.tcp_port = tcp.get("port", 1234)

    @classmethod
    def load_from_yaml(cls, file_name: str):
        with open(file_name, "r") as file:
            data_loaded = yaml.safe_load(file)

        tcp = data_loaded.get("tcp", {})

        return cls(tcp)

import yaml


class AppConfig:
    def __init__(self, tcp: dict, web: dict):
        self.tcp_server_addr = tcp.get("address", "0.0.0.0")
        self.tcp_port = tcp.get("port", 1234)

        self.web_addr = web.get("address", "0.0.0.0")
        self.web_port = web.get("port", 8080)
        self.web_debug = web.get("debug", True)
        self.hide_flask_logs = web.get("hide_flask_logs", True)

    @classmethod
    def load_from_yaml(cls, file_name: str):
        with open(file_name, "r") as file:
            data_loaded = yaml.safe_load(file)

        tcp = data_loaded.get("tcp", {})
        web = data_loaded.get("web", {})

        return cls(tcp, web)

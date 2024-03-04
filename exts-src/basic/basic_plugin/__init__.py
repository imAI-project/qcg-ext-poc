class PluginClass:

    name: str

    def __init__(self) -> None:
        self.name = "Basic Plugin Inner"

    def get_name(self) -> str:
        return self.name
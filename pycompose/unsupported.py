class UnsupportedConfiguration:

    def __init__(self, configuration_name, message, docs_url="", spec_url="", compose_path="/"):
        self.configuration_name = configuration_name
        self.message = message
        self.docs_url = docs_url
        self.spec_url = spec_url
        self.compose_path = compose_path

    def __str__(self) -> str:
        return f"{self.message} for {self.configuration_name} at {self.compose_path}"

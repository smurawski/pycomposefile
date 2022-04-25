from .service import Service


class ComposeFile:

    def __init__(self, deserialized_compose_file):
        version = deserialized_compose_file.pop("version", None)
        if version is not None:
            version = str(version)
        self.version = version
        self.services = {}
        self.compose_path = "services"
        for service in deserialized_compose_file["services"].keys():
            self.services[service] = Service.from_parsed_yaml(
                deserialized_compose_file["services"][service],
                service,
                self.compose_path
            )

from .service import Service
import yaml


class ComposeFile:

    def __init__(self, compose_file):
        deserialized_compose_file = yaml.load(compose_file, Loader=yaml.Loader)
        version = deserialized_compose_file.pop("version", None)
        if version is not None:
            version = str(version)
        self.version = version
        self.services = {}
        self.compose_path = "services"
        for service in deserialized_compose_file["services"].keys():
            self.services[service] = Service.from_parsed_yaml(
                service,
                deserialized_compose_file["services"][service],
                self.compose_path
            )

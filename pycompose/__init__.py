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
        for service in deserialized_compose_file["services"]:
            self.services[service] = Service(service, deserialized_compose_file["services"][service])

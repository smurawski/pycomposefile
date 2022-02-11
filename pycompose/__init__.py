from .version import Version
from .service import Service
import yaml

class ComposeFile:
    
    def __init__(self, compose_file):
        deserialized_compose_file = yaml.load(compose_file, Loader=yaml.Loader)
        self.version = Version(deserialized_compose_file)
        self.services = {}
        for service in deserialized_compose_file["services"]:
            self.services[service] = Service(service, deserialized_compose_file["services"][service])

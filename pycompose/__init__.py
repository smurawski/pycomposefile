from .version import Version
from .build import Build
import yaml

class ComposeFile:
    
    def __init__(self, compose_file):
        deserialized_compose_file = yaml.load(compose_file, Loader=yaml.Loader)
        self.version = Version(deserialized_compose_file)
        self.build = Build(deserialized_compose_file)
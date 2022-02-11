from ensurepip import version
import yaml

class Version:
    def __init__(self, deserialized_compose_file):
        if "version" in deserialized_compose_file:
            self.version_number = str(deserialized_compose_file["version"])
        else:
            self.version_number = None

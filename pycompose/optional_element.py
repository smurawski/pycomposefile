from sqlite3 import complete_statement
from .unsupported import UnsupportedConfiguration
import re
import os


class ComposeElement:
    supported_keys = {}
    unsupported_keys = {}
    environment_regex = re.compile("\$\w+")

    def __init__(self, config, compose_path=""):
        self.compose_path = compose_path
        for key in self.supported_keys.keys():
            value = config.pop(key, None)
            transform = self.supported_keys[key]
            if isinstance(value, dict):
                value = transform(key, value, compose_path)
            elif value is not None:
                value = str(value)
                environment_variables = self.environment_regex.findall(value)
                for match in environment_variables:
                    env_var = match.replace("$", "")
                    value = re.sub(f"\{match}", os.environ.get(env_var), value)
                value = transform(value)
            self.__setattr__(key, value)
        self.unsupported_elements = config

    @classmethod
    def from_parsed_yaml(cls, name, config, compose_path):
        if config is None:
            return None
        compose_path = f"{compose_path}/{name}"
        return cls(config, compose_path)

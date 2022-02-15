from .unsupported import UnsupportedConfiguration
import re
import os


class ComposeElement:
    supported_keys = {}
    unsupported_keys = {}

    def __init__(self, config, compose_path=""):
        self.compose_path = compose_path
        for key in self.supported_keys.keys():
            value = config.pop(key, None)
            transform = self.supported_keys[key]
            if isinstance(value, dict):
                value = transform(key, value, compose_path)
            elif value is not None:
                value = transform(self.replace_environment_variables(value))
            self.__setattr__(key, value)
        for key in self.unsupported_keys.keys():
            message, docs_url, spec_url = self.unsupported_keys[key]
            value = UnsupportedConfiguration(key, message, docs_url, spec_url, compose_path)
            self.__setattr__(key, value)
        for key in config.keys():
            if key not in self.unsupported_keys.keys():
                pass
                # raise Exception(f"Failed to map {key} in {compose_path}")

    def replace_environment_variables(self, value):
        environment_regex = re.compile(r"\${?\w+}?")
        value = str(value)
        environment_variables = environment_regex.findall(value)
        for match in environment_variables:
            env_var = match.replace("$", "").replace("{", "").replace("}", "")
            value = re.sub(f"\\{match}", os.environ.get(env_var), value)
        return value

    @classmethod
    def from_parsed_yaml(cls, name, config, compose_path):
        if config is None:
            return None
        compose_path = f"{compose_path}/{name}"
        return cls(config, compose_path)

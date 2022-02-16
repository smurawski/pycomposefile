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
                if type(transform) is tuple:
                    transform, valid_values = transform
                    value = self.transform_incoming_data(value, transform, valid_values)
                else:
                    value = self.transform_incoming_data(value, transform)
            self.__setattr__(key, value)
        for key in self.unsupported_keys.keys():
            message, docs_url, spec_url = self.unsupported_keys[key]
            value = UnsupportedConfiguration(key, message, docs_url, spec_url, compose_path)
            self.__setattr__(key, value)
        for key in config.keys():
            if key not in self.unsupported_keys.keys():
                pass
                # raise Exception(f"Failed to map {key} in {compose_path}")

    def transform_incoming_data(self, value, data_transformer, valid_values=[]):
        # TODO: if the data is an integer or decimal, should there be a "between" check?
        transformed = data_transformer(self.replace_environment_variables(value))
        if len(valid_values) > 0 and transformed not in valid_values:
            # TODO: Should this return None or should this raise?
            return None
        else:
            return transformed

    def replace_environment_variables(self, value):
        value = str(value)
        value = self.replace_environment_variables_with_empty_unset(value)
        value = self.replace_environment_variables_with_unset(value)
        value = self.replace_environment_variables_with_braces(value)
        value = self.replace_environment_variables_without_braces(value)

        return value

    def replace_environment_variables_with_empty_unset(self, value):
        capture = re.compile(r"\$\{(?P<variablename>\w+)\:-(?P<defaultvalue>\w+)\}")
        matches = capture.search(value)
        while matches:
            env_var = os.environ.get(matches.group("variablename"))
            default_value = matches.group("defaultvalue")
            if env_var is None or len(env_var) == 0:
                env_var = default_value
            value = re.sub(f"\\{matches[0]}", env_var, value)
            matches = capture.search(value)
        return value

    def replace_environment_variables_with_unset(self, value):
        capture = re.compile(r"\$\{(?P<variablename>\w+)-(?P<defaultvalue>\w+)\}")
        matches = capture.search(value)
        while matches:
            env_var = os.environ.get(matches.group("variablename"))
            default_value = matches.group("defaultvalue")
            if env_var is None:
                env_var = default_value
            value = re.sub(f"{matches[0]}", env_var, value)
            matches = capture.search(value)
        return value

    def replace_environment_variables_with_braces(self, value):
        capture = re.compile(r"\$\{(?P<variablename>\w+)\}")
        matches = capture.search(value)
        while matches:
            env_var = os.environ.get(matches.group("variablename"))
            value = re.sub(f"\\{matches[0]}", env_var, value)
            matches = capture.search(value)
        return value

    def replace_environment_variables_without_braces(self, value):
        capture = re.compile(r"\$(?P<variablename>\w+)")
        matches = capture.search(value)
        while matches:
            env_var = os.environ.get(matches.group("variablename"))
            value = re.sub(f"\\{matches[0]}", env_var, value)
            matches = capture.search(value)
        return value

    @classmethod
    def from_parsed_yaml(cls, name, config, compose_path):
        if config is None:
            return None
        compose_path = f"{compose_path}/{name}"
        return cls(config, compose_path)

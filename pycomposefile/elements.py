import re
import os


class Element():

    def __init__(self, element_name, transform, config_value, spec_url="", compose_path="/"):
        self.element_name = element_name
        self.spec_url = spec_url
        self.compose_path = compose_path
        self.transform = transform
        self.config_value = config_value
        self.transform_value()

    def __eq__(self, other):
        return self.__repr__().__eq__(other)

    def __str__(self) -> str:
        return self.resolved_value

    def __repr__(self):
        return self.resolved_value

    def __getattr__(self, name):
        return self.resolved_value.__getattribute__(name)

    def __getitem__(self, item):
        return self.resolved_value.__getitem__(item)

    def transform_value(self):
        if self.transform is None:
            self.resolved_value = None
            return
        if isinstance(self.config_value, dict):
            self.resolved_value = self.transform(self.element_name, self.config_value, self.compose_path)
        elif self.config_value is not None:
            self.resolved_value = self.transform_supported_data()
        else:
            self.resolved_value = None

    def transform_supported_data(self):
        if type(self.transform) is tuple:
            transform, valid_values = self.transform
            value = self.transform_and_validate_supported_data(self.config_value, transform, valid_values)
        else:
            value = self.transform(self.replace_environment_variables(self.config_value))
        return value

    def transform_and_validate_supported_data(self, value, data_transformer, valid_values):
        # TODO: if the data is an integer or decimal, should there be a "between" check?
        transformed = data_transformer(self.replace_environment_variables(value))
        if transformed not in valid_values:
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
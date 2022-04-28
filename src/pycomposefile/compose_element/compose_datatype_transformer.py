import re
import os


class ComposeDataTypeTransformer():
    def transform_supported_data(self, transform, value, valid_values=None):
        if valid_values is not None:
            value = self.transform_and_validate_supported_data(value, transform, valid_values)
        else:
            value = transform(self.replace_environment_variables(value))
        return value

    def transform_and_validate_supported_data(self, value, data_transformer, valid_values):
        # TODO: if the data is an integer or decimal, should there be a "between" check?
        transformed = data_transformer(self.replace_environment_variables(value))
        if isinstance(transformed, int) and valid_values[0] <= transformed <= valid_values[1]:
            return transformed
        elif transformed not in valid_values:
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

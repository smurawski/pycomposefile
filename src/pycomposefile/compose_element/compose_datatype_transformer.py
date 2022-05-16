import re
import os


class EmptyOrUnsetException(Exception):
    def __init__(self, variable_name, *args: object) -> None:
        self.variable_name = variable_name
        super().__init__(*args)

    def __str__(self) -> str:
        return f"Failed to evaluate mandatory variable {self.variable_name}"


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
        value = self.replace_environment_variables_with_braces(value)
        value = self.replace_environment_variables_without_braces(value)
        value = self.replace_environment_variables_with_empty_unset(value)
        value = self.replace_environment_variables_with_unset(value)
        value = self.replace_mandatory_variables_with_empty_or_unset(value)
        value = self.replace_mandatory_variables_with_unset(value)
        value = self.do_not_replace_variables(value)

        return value

    def replace_environment_variables_with_empty_unset(self, value):
        capture = re.compile(r"(\$+)\{(?P<variablename>\w+)\:-(?P<defaultvalue>.+)\}")
        matches = capture.search(value)
        if matches is not None and matches[1] == "$$":
            return value
        while matches:
            env_var = os.environ.get(matches.group("variablename"))
            default_value = matches.group("defaultvalue")
            if env_var is None or len(env_var) == 0:
                env_var = default_value
            value = re.sub(f"\\{matches[0]}", env_var, value)
            matches = capture.search(value)
        return value

    def replace_environment_variables_with_unset(self, value):
        capture = re.compile(r"(\$+)\{(?P<variablename>\w+)-(?P<defaultvalue>.+)\}")
        matches = capture.search(value)
        if matches is not None and matches[1] == "$$":
            return value
        while matches:
            env_var = os.environ.get(matches.group("variablename"))
            default_value = matches.group("defaultvalue")
            if env_var is None:
                env_var = default_value
            value = re.sub(f"{matches[0]}", env_var, value)
            matches = capture.search(value)
        return value

    def replace_mandatory_variables_with_empty_or_unset(self, value):
        capture = re.compile(r"(\$+)\{(?P<variablename>\w+)\:\?(err)\}")
        matches = capture.search(value)
        if matches is not None and matches[1] == "$$":
            return value
        while matches:
            env_var = os.environ.get(matches.group("variablename"))
            if env_var is None or len(env_var) == 0:
                raise EmptyOrUnsetException(matches.group("variablename"))
            to_be_replaced = r"\$\{" + matches.group('variablename') + r"\:\?err\}"
            value = re.sub(to_be_replaced, env_var, value)
            matches = capture.search(value)
        return value

    def replace_mandatory_variables_with_unset(self, value):
        capture = re.compile(r"(\$+)\{(?P<variablename>\w+)\?(err)\}")
        matches = capture.search(value)
        if matches is not None and matches[1] == "$$":
            return value
        while matches:
            env_var = os.environ.get(matches.group("variablename"))
            if env_var is None:
                raise EmptyOrUnsetException(matches.group("variablename"))
            to_be_replaced = r"\$\{" + matches.group('variablename') + r"\?err\}"
            value = re.sub(to_be_replaced, env_var, value)
            matches = capture.search(value)
        return value

    def replace_environment_variables_with_braces(self, value):
        capture = re.compile(r"\$\{(?P<variablename>\w+)\}")
        matches = capture.search(value)
        if matches is not None and matches[1] == "$$":
            return value
        while matches:
            env_var = os.environ.get(matches.group("variablename"))
            value = re.sub(f"\\{matches[0]}", env_var, value)
            matches = capture.search(value)
        return value

    def do_not_replace_variables(self, value):
        value = re.sub(r"\$\$", "$", value)
        return value

    def replace_environment_variables_without_braces(self, value):
        capture = re.compile(r"(\$+)(?P<variablename>\w+)")
        matches = capture.search(value)
        if matches is not None and matches[1] == "$$":
            return value
        while matches:
            env_var = os.environ.get(matches.group("variablename"))
            value = re.sub(f"\\{matches[0]}", env_var, value)
            matches = capture.search(value)
        return value

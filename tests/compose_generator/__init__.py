from pycomposefile import ComposeFile


class ComposeGenerator:

    @staticmethod
    def get_compose_with_string_value(variable_name):
        compose = """
services:
  frontend:
    image: awesome/${replace_me}
"""
        return ComposeFile(compose.format(replace_me=variable_name))

    @staticmethod
    def get_compose_with_decimal_value(variable_name):
        compose = """
services:
  frontend:
    image: awesome/website
    cpu_count: ${replace_me}
"""
        return ComposeFile(compose.format(replace_me=variable_name))

    @staticmethod
    def get_with_two_environment_variables_in_string_value(first_variable_name, second_variable_name):
        compose = """
services:
  frontend:
    image: awesome/website
    cpu_count: 1.5
    ports: "${replace_first}:${replace_second}"
"""
        return ComposeFile(compose.format(replace_first=first_variable_name, replace_second=second_variable_name))

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

    @staticmethod
    def get_compose_with_one_service_with_deploy():
        compose = """
services:
  frontend:
    image: awesome/webapp
    ports:
      - "8080:80"
    deploy:
      mode: replicated
      replicas: 2
      endpoint_mode: vip
      placement:
        constraints:
          - disktype=ssd
      resources:
        limits:
          cpus: '0.50'
          memory: 50M
          pids: 1
        reservations:
          cpus: '0.25'
          memory: 20M
      labels:
        com.example.description: "This label will appear on the web service"
        com.example.otherstuff: "random things"
      rollback_config:
        order: stop-first
      update_config:
        order: stop-first
"""
        return ComposeFile(compose)

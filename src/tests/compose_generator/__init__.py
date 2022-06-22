
from pycomposefile import ComposeFile
import yaml


class ComposeGenerator:

    @staticmethod
    def convert_yaml_to_compose_file(yaml_string):
        compose_yaml = yaml.load(yaml_string, Loader=yaml.Loader)
        return ComposeFile(compose_yaml)

    @staticmethod
    def get_compose_with_string_value(variable_name):
        compose = """
services:
  frontend:
    image: awesome/${replace_me}
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose.format(replace_me=variable_name))

    @staticmethod
    def get_compose_with_decimal_value(variable_name):
        compose = """
services:
  frontend:
    image: awesome/website
    cpu_count: ${replace_me}
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose.format(replace_me=variable_name))

    @staticmethod
    def get_with_two_environment_variables_in_string_value(first_variable_name, second_variable_name):
        compose = """
services:
  frontend:
    image: awesome/website
    cpu_count: 1.5
    ports: "${replace_first}:${replace_second}"
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose.format(replace_first=first_variable_name, replace_second=second_variable_name))

    @staticmethod
    def get_compose_with_one_service_with_deploy():
        compose = """
services:
  frontend:
    image: awesome/webapp
    ports:
      - "8080:80"
    expose: "3000"
    command: bundle exec thin -p 3000
    blkio_config:
      weight: 300
      weight_device:
        - path: /dev/sda
          weight: 400
      device_read_bps:
        - path: /dev/sdb
          rate: '12mb'
      device_read_iops:
        - path: /dev/sdb
          rate: 120
      device_write_bps:
        - path: /dev/sdb
          rate: '1024k'
      device_write_iops:
        - path: /dev/sdb
          rate: 30
    deploy:
      mode: replicated
      replicas: 2
      endpoint_mode: vip
      placement:
        constraints:
          - disktype=ssd
        preferences:
          datacenter=eastus
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
        monitor: 5m
      update_config:
        order: start-first
        failure_action: rollback
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_one_service_with_multiple_expose():
        compose = """
services:
  frontend:
    image: awesome/webapp
    ports:
      - "8080:80"
    expose:
      - 3000
      - "4000"
      - '5000'
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_command_list():
        compose = """
services:
  frontend:
    image: awesome/webapp
    ports:
      - "8080:80"
    expose: "3000"
    command:
      - bundle
      - exec
      - thin
      - -p
      - 3000
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_command_list_with_quotes():
        compose = """
services:
  frontend:
    image: awesome/webapp
    ports:
      - "8080:80"
    expose: "3000"
    command:
      - echo
      - "hello world"
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_structured_ports():
        compose = """
services:
  frontend:
    image: awesome/webapp
    ports:
      - target: 80
        host_ip: 127.0.0.1
        published: 8080
        protocol: tcp
        mode: host

      - target: 443
        host_ip: 192.168.1.11
        published: 8443
        protocol: tcp
        mode: host
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_structured_configs():
        compose = """
services:
  frontend:
    image: awesome/webapp
    configs:
      - source: my_config
        target: /redis_config
        uid: "103"
        gid: "103"
        mode: 0440

      - source: another_config
        target: /db_config
        uid: "105"
        gid: "105"
        mode: 0777
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_string_configs():
        compose = """
services:
  frontend:
    image: awesome/webapp
    configs:
      - source: my_config
      - source: another_config
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_entrypoint_no_command():
        compose = """
services:
  frontend:
    image: awesome/webapp
    entrypoint: /code/entrypoint.sh
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_entrypoint_as_list_no_command():
        compose = """
services:
  frontend:
    image: awesome/webapp
    entrypoint:
      - php
      - -d
      - zend_extension=/usr/local/lib/php/extensions/no-debug-non-zts-20100525/xdebug.so
      - -d
      - memory_limit=-1
      - vendor/bin/phpunit
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_entrypoint_and_command():
        compose = """
services:
  frontend:
    image: awesome/webapp
    ports:
      - "8080:80"
    expose: "3000"
    entrypoint: /code/entrypoint.sh
    command:
      - echo
      - "hello world"
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_file_credential_spec():
        compose = """
services:
  frontend:
    image: awesome/webapp
    credential_spec:
      file: my-credential-spec.json
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_registry_credential_spec():
        compose = """
services:
  frontend:
    image: awesome/webapp
    credential_spec:
      registry: my-credential-spec
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_config_credential_spec():
        compose = """
services:
  frontend:
    image: awesome/webapp
    credential_spec:
      config: my_credential_spec
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_service_dependencies():
        compose = """
services:
  frontend:
    image: awesome/webapp
    depends_on:
      - db
      - redis
  redis:
    image: redis
  db:
    image: postgres
  reporting:
    image: reporting
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_multiple_service_dependencies():
        compose = """
services:
  frontend:
    image: awesome/webapp
    depends_on:
      - db
      - redis
  db:
    image: postgres
    depends_on:
      - redis
  redis:
    image: redis
  reporting:
    image: reporting
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_circular_service_dependencies():
        compose = """
services:
  frontend:
    image: awesome/webapp
    depends_on:
      - db
      - redis
  db:
    image: postgres
    depends_on:
      - redis
  redis:
    image: redis
    depends_on:
      - reporting
  reporting:
    image: reporting
    depends_on:
      - db
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_service_dependencies_and_conditions():
        compose = """
services:
  frontend:
    image: awesome/webapp
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
  redis:
    image: redis
  db:
    image: postgres
  reporting:
    image: reporting
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_memory_reservation():
        compose = """
services:
  frontend:
    image: awesome/webapp
    mem_reservation: 1.5gb
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_environment_map():
        compose = """
services:
  frontend:
    image: awesome/webapp
    environment:
      RACK_ENV: development
      SHOW: "true"
      USER_INPUT:
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_environment_list():
        compose = """
services:
  frontend:
    image: awesome/webapp
    environment:
      - RACK_ENV=development
      - SHOW=true
      - USER_INPUT
      - USER_INPUT=
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_environment_file_single():
        compose = """
services:
  frontend:
    image: awesome/webapp
    env_file: ./sample/test.env
    environment:
      - RACK_ENV=development
      - SHOW=true
      - USER_INPUT
      - USER_INPUT=
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_environment_file_list():
        compose = """
services:
  frontend:
    image: awesome/webapp
    env_file:
      - ./sample/common.env
      - ./sample/apps/web.env
      - ./sample/opt/runtime_opts.env
    environment:
      - RACK_ENV=canary
      - SHOW=true
      - USER_INPUT
      - USER_INPUT=
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_os_environment_vars():
        compose = """
services:
  frontend:
    image: awesome/webapp
    environment:
      - RACK_ENV=${RACK_ENV}
      - URL=${DEPLOY_ENV:-${test}}
      - VERSION=${VERSION:-default}
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_mandatory_env_vars():
        compose = """
services:
  frontend:
    image: awesome/webapp
    environment:
      - URL=${URL:?err}
      - FOO=${BAR:?err}
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_double_dollar_sign_env_vars():
        compose = """
services:
  frontend:
    image: awesome/webapp
    environment:
      - ENVIRONMENT=$$ENVIRONMENT
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_mandatory_unset_env_vars():
        compose = """
services:
  frontend:
    image: awesome/webapp
    environment:
      - BAZ=${BAZ?err}
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_one_secret():
        compose = """
services:
  frontend:
    image: awesome/webapp
    secrets:
      - my_secret
secrets:
  my_secret:
    file: ./sample/my_secret.txt
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_external_secret():
        compose = """
services:
  frontend:
    image: awesome/webapp
    secrets:
      - my_other_secret
secrets:
  my_other_secret:
    external: true
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_long_syntax():
        compose = """
services:
  frontend:
    image: awesome/webapp
    secrets:
      - source: my_secret
        target: redis_secret
        uid: '103'
        gid: '103'
        mode: 0440
secrets:
  my_secret:
    file: ./sample/my_secret.txt
  my_other_secret:
    external: true
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_network():
        compose = """
version: '3'
services:
  grafana:
    image: grafana/grafana:6.4.4
    container_name: grafana
    restart: unless-stopped
    hostname: grafana
    network_mode: bridge
    ports:
      - 3000:3000/tcp
    volumes:
      - /var/lib/grafana:/var/lib/grafana
      - /var/log/grafana:/var/log/grafana
      - /etc/grafana/provisioning:/etc/grafana/provisioning
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_one_service_with_build_context():
        compose = """
services:
  frontend:
    image: awesome/webapp
    build: ./webapp
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_one_service_with_specific_build_context():
        compose = """
services:
  frontend:
    image: awesome/webapp
    build: 
      context: ./webapp
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

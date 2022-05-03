from ast import Str
from decimal import Decimal

from pycomposefile.service.service_blkio_config import BlkioConfig
from pycomposefile.service.service_deploy import Deploy
from pycomposefile.service.service_credential_spec import CredentialSpec
from pycomposefile.service.service_cap import Cap
from pycomposefile.service.service_configs import Configs
from pycomposefile.service.service_command import Command
from pycomposefile.service.service_environment import Environment, EnvFile
from pycomposefile.service.service_ports import Ports
from pycomposefile.compose_element import ComposeElement, ComposeStringOrListElement, ComposeByteValue


class Expose(ComposeStringOrListElement):
    def __init__(self, config, key=None, compose_path=None):
        self.transform = int
        super().__init__(config, key, compose_path)


class CpuSets(ComposeStringOrListElement):
    def __init__(self, config, key=None, compose_path=None):
        self.transform = str
        super().__init__(config, key, compose_path)


class Dependency(str):
    def __new__(cls, config, key=None, compose_path=None, ) -> None:
        condition = None
        if isinstance(config, Dependency):
            return config
        if isinstance(config, tuple):
            name, detail = config
            condition = detail["condition"]
        else:
            name = config
        ob = super(Dependency, cls).__new__(cls, name)
        ob.__setattr__('condition', condition)
        return ob


class DependsOn(ComposeStringOrListElement):
    def __init__(self, config, key=None, compose_path=None):
        self.transform = Dependency
        if isinstance(config, dict):
            config_to_list = []
            for key in config.keys():
                config_to_list.append((key, config[key]))
            config = config_to_list
        super().__init__(config, key, compose_path)


class Service(ComposeElement):
    element_keys = {
        "image": (str, ""),
        "container_name": (str, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#container_name"),
        "cpu_count": (Decimal, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cpu_count"),
        "entrypoint": (Command, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#entrypoint"),
        "command": (Command, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#command"),
        "deploy": (Deploy.from_parsed_yaml, "https://github.com/compose-spec/compose-spec/blob/master/deploy.md"),
        "expose": (Expose, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#expose"),
        "ports": (Ports, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#long-syntax-2"),
        "cpus": (Decimal, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cpus"),
        "credential_spec": (CredentialSpec.from_parsed_yaml, ""),
        "blkio_config": (BlkioConfig.from_parsed_yaml,
                         "https://github.com/compose-spec/compose-spec/blob/master/spec.md#blkio_config"),
        "cpu_percent": (Decimal,
                        "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cpu_percent"),
        "cpu_shares": (int,
                       "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cpu_shares"),
        "cpu_period": (str,
                       "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cpu_period"),
        "cpu_quota": (int,
                      "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cpu_quota"),
        "cpu_rt_runtime": (str,
                           "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cpu_rt_runtime"),
        "cpu_rt_period": (str,
                          "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cpu_rt_period"),
        "cpuset": (list,
                   "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cpuset"),
        "build": (None,
                  "https://github.com/compose-spec/compose-spec/blob/master/build.md"),
        "cap_add": (Cap,
                    "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cap_add"),
        "cap_drop": (Cap,
                     "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cap_add"),
        "cgroup_parent": (str,
                          "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cgroup_parent"),
        "configs": (Configs,
                    "https://github.com/compose-spec/compose-spec/blob/master/spec.md#configs"),
        "depends_on": (DependsOn, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#depends_on"),
        "env_file": (EnvFile, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#env_file"),
        "environment": (Environment, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#environment"),
        "mem_reservation": (ComposeByteValue, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#mem_reservation"),
    }

    def entrypoint_and_command(self):
        if self.command is None and self.entrypoint is None:
            return None
        else:
            container_entrypoint_and_command = ""
            if self.entrypoint is not None:
                container_entrypoint_and_command += self.entrypoint.command_string()
                container_entrypoint_and_command += " "
            if self.command is not None:
                container_entrypoint_and_command += self.command.command_string()
            return container_entrypoint_and_command

    def resolve_environment_hierarchy(self):
        if self.env_file is not None:
            env_file = self.env_file.readFile()
            env_file.update(self.environment)
            return env_file
        else:
            return self.environment

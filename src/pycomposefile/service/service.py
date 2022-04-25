from decimal import Decimal

from .service_blkio_config import BlkioConfig
from .service_deploy import Deploy
from .service_credential_spec import CredentialSpec
from .service_cap import Cap
from .service_configs import Configs
from .service_command import Command
from .service_ports import Ports
from ..compose_element import ComposeElement, ComposeStringOrListElement


class Expose(ComposeStringOrListElement):
    def __init__(self, config, key=None, compose_path=None):
        self.transform = int
        super().__init__(config, key, compose_path)


class CpuSets(ComposeStringOrListElement):
    def __init__(self, config, key=None, compose_path=None):
        self.transform = str
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
    }

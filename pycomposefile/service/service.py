from decimal import Decimal


from pycomposefile.service.service_misc import (Expose,
                                                DependsOn,
                                                StorageOpt,
                                                Ulimits)
from pycomposefile.service.service_blkio_config import BlkioConfig
from pycomposefile.service.service_build import Build
from pycomposefile.service.service_deploy import Deploy
from pycomposefile.service.service_credential_spec import CredentialSpec
from pycomposefile.service.service_cap import Cap
from pycomposefile.service.service_configs import (Configs, Secrets)
from pycomposefile.service.service_command import Command
from pycomposefile.service.service_environment import (Environment, EnvFile)
from pycomposefile.service.service_healthcheck import HealthCheck
from pycomposefile.service.service_logging import Logging
from pycomposefile.service.service_networks import Networks
from pycomposefile.service.service_ports import Ports
from pycomposefile.service.service_volumes import Volumes
from pycomposefile.compose_element import (ComposeElement,
                                           ComposeListOrMapElement,
                                           ComposeByteValue,
                                           ComposeStringOrListElement)


class Service(ComposeElement):
    # Keep element_keys for compatibility and reference, but will not be used for dynamic property creation
    element_keys = {
        "image": (str, ""),
        "build": (Build,
                  "https://github.com/compose-spec/compose-spec/blob/master/build.md"),
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
        "cpuset": (ComposeStringOrListElement,
                   "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cpuset"),

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
        "secrets": (Secrets, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#secrets"),
        "scale": (int, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#scale"),
        "device_cgroup_rules": (ComposeStringOrListElement, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#device_cgroup_rules"),
        "devices": (ComposeStringOrListElement, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#devices"),
        "dns": (ComposeStringOrListElement, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#dns"),
        "dns_opt": (ComposeStringOrListElement, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#dns_opt"),
        "dns_search": (ComposeStringOrListElement, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#dns_search"),
        "domainname": (str, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#domainname"),
        "external_links": (ComposeStringOrListElement, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#external_links"),
        "extra_hosts": (ComposeStringOrListElement, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#extra_hosts"),
        "group_add": (ComposeStringOrListElement, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#group_add"),
        "healthcheck": (HealthCheck.from_parsed_yaml, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#healthcheck"),
        "hostname": (str, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#hostname"),
        "init": (bool, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#init"),
        "ipc": (str, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#ipc"),
        "isolation": (str, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#isolation"),
        "labels": (ComposeListOrMapElement, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#labels"),
        "links": (ComposeStringOrListElement, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#links"),
        "logging": (Logging, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#logging"),
        "network_mode": (str, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#network_mode"),
        "networks": (Networks, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#networks"),
        "mac_address": (str, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#mac_address"),
        "mem_limit": (ComposeByteValue, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#mem_limit"),
        "mem_swappiness": ((int, [0, 100]), "https://github.com/compose-spec/compose-spec/blob/master/spec.md#mem_swappiness"),
        "memswap_limit": (ComposeByteValue, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#memswap_limit"),
        "oom_kill_disable": (bool, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#oom_kill_disable"),
        "oom_score_adj": ((int, [-1000, 1000]), "https://github.com/compose-spec/compose-spec/blob/master/spec.md#oom_score_adj"),
        "pid": (int, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#pid"),
        "pids_limit": (int, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#pids_limit"),
        "platform": (str, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#platform"),
        "privileged": (bool, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#privileged"),
        "profiles": (ComposeStringOrListElement, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#profiles"),
        "pull_policy": ((str, ["always", "never", "missing", "build"]), "https://github.com/compose-spec/compose-spec/blob/master/spec.md#pull_policy"),
        "read_only": (bool, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#read_only"),
        "restart": ((str, ["no", "always", "on-failure", "unless-stopped"]), "https://github.com/compose-spec/compose-spec/blob/master/spec.md#restart"),
        "runtime": (str, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#runtime"),
        "security_opt": (ComposeStringOrListElement, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#security_opt"),
        "shm_size": (ComposeByteValue, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#shm_size"),
        "stdin_open": (str, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#stdin_open"),
        "stop_grace_period": (str, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#stop_grace_period"),
        "stop_signal": (str, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#stop_signal"),
        "storage_opt": (StorageOpt.from_parsed_yaml, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#storage_opt"),
        "sysctls": (ComposeStringOrListElement, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#sysctls"),
        "tmpfs": (ComposeStringOrListElement, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#tmpfs"),
        "tty": (bool, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#tty"),
        "ulimits": (Ulimits.from_parsed_yaml, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#ulimits"),
        "user": (str, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#user"),
        "userns_mode": (str, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#userns_mode"),
        "volumes": (Volumes, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#volumes"),
        "volumes_from": (ComposeStringOrListElement, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#volumes_from"),
        "working_dir": (str, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#working_dir")

    }

    def __init__(self, config, compose_path=""):
        # Initialize the base class attributes but bypass its dynamic property creation
        self.compose_path = compose_path

        # Initialize all properties explicitly with None as default
        self.image = None
        self.build = None
        self.container_name = None
        self.cpu_count = None
        self.entrypoint = None
        self.command = None
        self.deploy = None
        self.expose = None
        self.ports = None
        self.cpus = None
        self.credential_spec = None
        self.blkio_config = None
        self.cpu_percent = None
        self.cpu_shares = None
        self.cpu_period = None
        self.cpu_quota = None
        self.cpu_rt_runtime = None
        self.cpu_rt_period = None
        self.cpuset = None
        self.cap_add = None
        self.cap_drop = None
        self.cgroup_parent = None
        self.configs = None
        self.depends_on = None
        self.env_file = None
        self.environment = None
        self.mem_reservation = None
        self.secrets = None
        self.scale = None
        self.device_cgroup_rules = None
        self.devices = None
        self.dns = None
        self.dns_opt = None
        self.dns_search = None
        self.domainname = None
        self.external_links = None
        self.extra_hosts = None
        self.group_add = None
        self.healthcheck = None
        self.hostname = None
        self.init = None
        self.ipc = None
        self.isolation = None
        self.labels = None
        self.links = None
        self.logging = None
        self.network_mode = None
        self.networks = None
        self.mac_address = None
        self.mem_limit = None
        self.mem_swappiness = None
        self.memswap_limit = None
        self.oom_kill_disable = None
        self.oom_score_adj = None
        self.pid = None
        self.pids_limit = None
        self.platform = None
        self.privileged = None
        self.profiles = None
        self.pull_policy = None
        self.read_only = None
        self.restart = None
        self.runtime = None
        self.security_opt = None
        self.shm_size = None
        self.stdin_open = None
        self.stop_grace_period = None
        self.stop_signal = None
        self.storage_opt = None
        self.sysctls = None
        self.tmpfs = None
        self.tty = None
        self.ulimits = None
        self.user = None
        self.userns_mode = None
        self.volumes = None
        self.volumes_from = None
        self.working_dir = None

        # Process config using the same logic as the parent class
        for key in self.element_keys.keys():
            config_element = config.pop(key, None)
            key_config = self.element_keys[key]
            self._set_property_from_config(key, key_config, config_element, compose_path)

        # Handle any remaining unprocessed config keys
        for key in config.keys():
            # raise Exception(f"Failed to map {key} in {compose_path}")
            pass

    def _set_property_from_config(self, key, key_config, value, compose_path):
        """Set a specific property from config, preserving the original transformation logic."""
        if type(key_config[0]) is tuple:
            transform, valid_values = key_config[0]
        else:
            transform = key_config[0]
            valid_values = None

        # Apply the same transformation logic as the original
        if transform is not None:
            if isinstance(value, dict):
                value = transform(value, key, compose_path)
            elif isinstance(value, list):
                value = transform(value, key, compose_path)
            elif value is not None:
                # Set up temporary transform context for data transformation
                original_transform = getattr(self, 'transform', None)
                original_valid_values = getattr(self, 'valid_values', None)

                self.transform = transform
                self.valid_values = valid_values

                value = self.transform_supported_data(value)

                # Restore original transform context
                self.transform = original_transform
                self.valid_values = original_valid_values
        else:
            # TODO: Logging message if value was not None
            value = None

        # Explicitly set the attribute instead of using dynamic setattr
        setattr(self, key, value)

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
            env_file.update(self.environment or [])
            return env_file
        else:
            return self.environment

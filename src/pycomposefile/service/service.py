from decimal import Decimal
import re

from .service_blkio_config import BlkioConfig
from .service_deploy import Deploy
from .service_credential_spec import CredentialSpec
from ..compose_element import ComposeElement, ComposeStringOrListElement

CAP_LIST = [
    "CAP_AUDIT_CONTROL",
    "CAP_AUDIT_READ",
    "CAP_AUDIT_WRITE",
    "CAP_BLOCK_SUSPEND",
    "CAP_BPF",
    "CAP_CHECKPOINT_RESTORE",
    "CAP_SYS_ADMIN",
    "CAP_CHOWN",
    "CAP_DAC_OVERRIDE",
    "CAP_DAC_READ_SEARCH",
    "CAP_FOWNER",
    "CAP_DAC_READ_SEARCH",
    "CAP_FSETID",
    "CAP_IPC_LOCK",
    "CAP_IPC_OWNER",
    "CAP_KILL",
    "CAP_LEASE",
    "CAP_LINUX_IMMUTABLE",
    "CAP_MAC_ADMIN",
    "CAP_MAC_OVERRIDE",
    "CAP_MKNOD",
    "CAP_NET_ADMIN",
    "CAP_NET_BIND_SERVICE",
    "CAP_NET_BROADCAST",
    "CAP_NET_RAW",
    "CAP_PERFMON",
    "CAP_SYS_ADMIN",
    "CAP_SETGID",
    "CAP_SETFCAP",
    "CAP_SETPCAP",
    "CAP_SETUID",
    "CAP_SYS_ADMIN",
    "CAP_BPF",
    "CAP_SYS_BOOT",
    "CAP_SYS_CHROOT",
    "CAP_SYS_MODULE",
    "CAP_SYS_NICE",
    "CAP_SYS_PACCT",
    "CAP_SYS_PTRACE",
    "CAP_SYS_RAWIO",
    "CAP_SYS_RESOURCE",
    "CAP_SYS_TIME",
    "CAP_SYS_TTY_CONFIG",
    "CAP_SYSLOG",
    "CAP_WAKE_ALARM",
]


class Expose(ComposeStringOrListElement):
    def __init__(self, config, key=None, compose_path=None):
        self.transform = int
        super().__init__(config, key, compose_path)


class Cap(ComposeStringOrListElement):
    def __init__(self, config, key=None, compose_path=None):
        self.transform = (str, CAP_LIST)
        super().__init__(config, key, compose_path)


class Port(ComposeElement):
    element_keys = {
        "target": (int, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#long-syntax-2"),
        "host_ip": (str, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#long-syntax-2"),
        "published": (int, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#long-syntax-2"),
        "protocol": ((str, ['tcp', 'udp']), "https://github.com/compose-spec/compose-spec/blob/master/spec.md#long-syntax-2"),
        "mode": ((str, ['host', 'ingress']), "https://github.com/compose-spec/compose-spec/blob/master/spec.md#long-syntax-2"),
    }

    def __init__(self, port_definition, key=None, compose_path=""):
        if isinstance(port_definition, str):
            self.parse_string(port_definition)
        else:
            super().__init__(port_definition, compose_path)

    def parse_string(self, port_definition):
        port_matcher = re.compile(r'(?P<HostIp>((\d+\.\d+\.\d+\.\d+:)|))(?P<HostPort>(\d+:)|)(?P<ContainerPort>\d+)(?P<Protocol>((/(tcp|udp))|))')
        matches = port_matcher.search(port_definition)
        host_ip = matches.group('HostIp')
        if host_ip == '':
            host_ip = None
        else:
            host_ip = host_ip.rstrip(":")
        host_port = matches.group('HostPort')
        if host_port == '':
            host_port = None
        else:
            host_port = host_port.rstrip(":")
        container_port = matches.group('ContainerPort')
        protocol = matches.group('Protocol')
        if protocol == '':
            protocol = 'tcp'

        self.__setattr__('host_ip', host_ip)
        self.__setattr__('published', host_port)
        self.__setattr__('target', container_port)
        self.__setattr__('protocol', protocol)
        self.__setattr__('mode', 'host')

    def __str__(self) -> str:
        port = ''
        if self.host_ip is not None:
            port += f"{self.host_ip}:"
        if self.published is not None:
            port += f"{self.published}:"
        port += f"{self.target}/{self.protocol}"
        return port


class Ports(ComposeStringOrListElement):
    def __init__(self, config, key=None, compose_path=None):
        self.transform = Port
        super().__init__(config, 'ports', compose_path)


class Command(ComposeStringOrListElement):
    def __init__(self, config, key=None, compose_path=None):
        self.transform = str
        super().__init__(config, key, compose_path)

    def command_string(self):
        capture = re.compile(r"\w+(\s\w+)+")
        string = ""
        for v in self:
            if len(self) > 1 and capture.match(v):
                string += f"\"{v}\""
            else:
                string += f"{v} "
        return string.lstrip().rstrip()


class Service(ComposeElement):
    element_keys = {
        "image": (str, ""),
        "container_name": (str, ""),
        "cpu_count": (Decimal, ""),
        "entrypoint": (Command, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#entrypoint"),
        "command": (Command, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#command"),
        "deploy": (Deploy.from_parsed_yaml, "https://github.com/compose-spec/compose-spec/blob/master/deploy.md"),
        "expose": (Expose, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#expose"),
        "ports": (Ports, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#long-syntax-2"),
        "cpus": (Decimal, ""),
        "credential_spec": (CredentialSpec.from_parsed_yaml, ""),
        "blkio_config": (BlkioConfig.from_parsed_yaml,
                         "https://github.com/compose-spec/compose-spec/blob/master/spec.md#blkio_config"),
        "cpu_percent": (None,
                        "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cpu_percent"),
        "cpu_shares": (int,
                       "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cpu_shares"),
        "cpu_period": (str,
                       "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cpu_period"),
        "cpu_quota": (None,
                      "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cpu_quota"),
        "cpu_rt_runtime": (None,
                           "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cpu_rt_runtime"),
        "cpu_rt_period": (None,
                          "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cpu_rt_period"),
        "cpuset": (list,
                   "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cpuset"),
        "build": (None,
                  "https://github.com/compose-spec/compose-spec/blob/master/build.md"),
        "cap_add": (None,
                    "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cap_add"),
        "cap_drop": (None,
                     "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cap_add"),
        "cgroup_parent": (None,
                          "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cgroup_parent"),
        "configs": (None,
                    "https://github.com/compose-spec/compose-spec/blob/master/spec.md#configs"),
    }

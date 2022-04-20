from decimal import Decimal
import re

from .service_blkio_config import BlkioConfig
from .service_deploy import Deploy
from .service_credential_spec import CredentialSpec
from .compose_element import ComposeElement, ComposeStringOrListElement

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
        self.data_type = int
        super().__init__(config, key, compose_path)


class Cap(ComposeStringOrListElement):
    def __init__(self, config, key=None, compose_path=None):
        self.data_type = str
        super().__init__(config, key, compose_path)


class Ports(ComposeStringOrListElement):
    def __init__(self, config, key=None, compose_path=None):
        self.data_type = str
        super().__init__(config, key, compose_path)


class Command(ComposeStringOrListElement):
    def __init__(self, config, key=None, compose_path=None):
        self.data_type = str
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
        "command": (Command, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#command"),
        "deploy": (Deploy.from_parsed_yaml, ""),
        "expose": (Expose, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#expose"),  # https://raw.githubusercontent.com/compose-spec/compose-spec/master/schema/compose-spec.json
        "ports": (Ports, ""),
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

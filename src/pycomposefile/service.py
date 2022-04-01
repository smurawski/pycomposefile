from decimal import Decimal
from .service_deploy import Deploy
from .service_credential_spec import CredentialSpec
from .compose_element import ComposeElement


class Expose(list):

    @classmethod
    def from_parsed_yaml(cls, value):
        return_value = None
        if type(value) is str:
            return_value = list()
            value = value.strip("[]").split(',')
            for v in value:
                return_value.append(int(v.rstrip().lstrip().strip("'")))
        return return_value


class Service(ComposeElement):
    element_keys = {
        "image": (str, ""),
        "container_name": (str, ""),
        "cpu_count": (Decimal, ""),
        "command": (str, ""),
        "deploy": (Deploy.from_parsed_yaml, ""),
        "expose": (Expose.from_parsed_yaml, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#expose"),  # https://raw.githubusercontent.com/compose-spec/compose-spec/master/schema/compose-spec.json
        "ports": (str, ""),
        "cpus": (Decimal, ""),
        "credential_spec": (CredentialSpec.from_parsed_yaml, ""),
        "blkio_config": (None,
                         "https://github.com/compose-spec/compose-spec/blob/master/spec.md#blkio_config"),
        "cpu_percent": (None,
                        "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cpu_percent"),
        "cpu_shares": (None,
                       "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cpu_shares"),
        "cpu_period": (None,
                       "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cpu_period"),
        "cpu_quota": (None,
                      "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cpu_quota"),
        "cpu_rt_runtime": (None,
                           "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cpu_rt_runtime"),
        "cpu_rt_period": (None,
                          "https://github.com/compose-spec/compose-spec/blob/master/spec.md#cpu_rt_period"),
        "cpuset": (None,
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

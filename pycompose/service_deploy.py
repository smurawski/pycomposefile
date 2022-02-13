from decimal import Decimal

from pycompose import unsupported

from .optional_element import ComposeElement


class ResourceDetails(ComposeElement):
    supported_keys = {"cpus": Decimal, "memory": str}
    unsupported_keys = {
        "pids": ("Unable to configure PID limits",
                 "",
                 "https://github.com/compose-spec/compose-spec/blob/master/deploy.md#pids"),
        "devices": ("Device configuration is unavailable in Azure ContainerApps",
                    "",
                    "https://github.com/compose-spec/compose-spec/blob/master/deploy.md#devices"),
    }


class Resources(ComposeElement):
    supported_keys = {
        "limits": ResourceDetails.from_parsed_yaml,
        "reservations": ResourceDetails.from_parsed_yaml
    }


class Labels(dict):
    compose_path = ""

    @classmethod
    def from_parsed_yaml(cls, name, value, compose_path):
        instance = cls()
        instance.compose_path = f"{compose_path}/{name}"
        instance.update(value)
        return instance


class Deploy(ComposeElement):
    supported_keys = {
        "endpoint_mode": str,
        "labels": Labels.from_parsed_yaml,
        "mode": str,
        "replicas": int,
        "resources": Resources.from_parsed_yaml
    }

    unsupported_keys = {
        "placement": ("Unable to specify placement constraints or preferences",
                      "https://docs.microsoft.com/azure/container-apps/containers",
                      "https://github.com/compose-spec/compose-spec/blob/master/deploy.md#placement")
    }

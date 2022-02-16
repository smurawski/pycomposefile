from decimal import Decimal
from .compose_element import ComposeElement
import re


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


class DeployTimespan(str):

    @classmethod
    def from_parsed_str(cls, value):
        timespan_validator = re.compile(r"\d+(ns|us|ms|s|m|h)")
        if not timespan_validator.match(value):
            value = "0s"
        return cls(value)


class UpdateConfig(ComposeElement):
    supported_keys = {
        "parallelism": int,
        "delay": DeployTimespan.from_parsed_str,
        "failure_action": str,
        "monitor": DeployTimespan.from_parsed_str,
        "max_failure_ratio": str,
        "order": str
    }


class Deploy(ComposeElement):
    supported_keys = {
        "endpoint_mode": str,
        "labels": Labels.from_parsed_yaml,
        "mode": str,
        "replicas": int,
        "resources": Resources.from_parsed_yaml,
        "rollback_config": UpdateConfig.from_parsed_yaml,
        "update_config": UpdateConfig.from_parsed_yaml
    }

    unsupported_keys = {
        "placement": ("Unable to specify placement constraints or preferences",
                      "https://docs.microsoft.com/azure/container-apps/containers",
                      "https://github.com/compose-spec/compose-spec/blob/master/deploy.md#placement"),
        "restart_policy": ("Restart conditions are not configurable",
                           "https://docs.microsoft.com/azure/container-apps/containers",
                           "https://github.com/compose-spec/compose-spec/blob/master/deploy.md#restart_policy")
    }

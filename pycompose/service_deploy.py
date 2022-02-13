from decimal import Decimal
from .optional_element import ComposeElement


class ResourceDetails(ComposeElement):
    supported_keys = {"cpus": Decimal, "memory": str}


class Resources(ComposeElement):
    supported_keys = {
        "limits": ResourceDetails.from_parsed_yaml,
        "reservations": ResourceDetails.from_parsed_yaml
    }


class Deploy(ComposeElement):
    supported_keys = {
        "endpoint_mode": str,
        "labels": str,
        "mode": str,
        "replicas": str,
        "resources": Resources.from_parsed_yaml
    }

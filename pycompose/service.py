from decimal import Decimal
from .unsupported import UnsupportedConfiguration
from .service_deploy import Deploy
from .optional_element import ComposeElement


class Service(ComposeElement):
    supported_keys = {
        "image": str,
        "container_name": str,
        "cpu_count": Decimal,
        "command": str,
        "deploy": Deploy.from_parsed_yaml
    }

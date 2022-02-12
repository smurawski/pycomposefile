from .unsupported import UnsupportedConfiguration
from .service_deploy import Deploy
from .optional_element import ComposeElement


class Service(ComposeElement):
    supported_keys = ["cpu_count", "command"]

    def __init__(self, container_name, service_config):
        self.image = service_config.pop("image", None)
        if self.image == None:
            raise ValueError("An image is required for the conversion to ContainerApps.")
        self.container_name = service_config.pop("container_name", container_name)
        self.deploy = Deploy.from_parsed_yaml(service_config.pop("deploy", None))

        super().__init__(service_config)

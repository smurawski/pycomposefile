from .unsupported import UnsupportedConfiguration


class Service:
    def __init__(self, container_name, service_entry):
        self.image = service_entry.pop("image", None)
        if self.image == None:
            raise ValueError("An image is required for the conversion to ContainerApps.")
        self.container_name = service_entry.pop("container_name", container_name)
        self.cpu_count = service_entry.pop("cpu_count", 0.5)

        self.command = service_entry.pop("command", None)

        # TODO replace with actionale reporting
        self.unsupported_keys = list(service_entry.keys())

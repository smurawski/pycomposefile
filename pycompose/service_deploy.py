from .optional_element import ComposeElement


class ResourceDetails(ComposeElement):
    supported_keys = ["cpus", "memory"]

    def __init__(self, config):
        super().__init__(config)


class Resources(ComposeElement):
    def __init__(self, config):
        self.limits = ResourceDetails.from_parsed_yaml(config.pop("limits", None))
        self.reservations = ResourceDetails.from_parsed_yaml(config.pop("reservations", None))
        super().__init__(config)


class Deploy(ComposeElement):
    supported_keys = ["endpoint_mode", "labels", "mode", "replicas"]

    def __init__(self, config):
        self.resources = Resources.from_parsed_yaml(config.pop("resources", None))
        super().__init__(config)

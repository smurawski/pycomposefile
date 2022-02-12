from .unsupported import UnsupportedConfiguration


class ComposeElement:
    supported_keys = []
    unsupported_keys = {}

    def __init__(self, config):
        for key in self.supported_keys:
            self.__setattr__(key, config.pop(key, None))
        self.unsupported_elements = config

    @classmethod
    def from_parsed_yaml(cls, config):
        if config is None:
            return None
        return cls(config)

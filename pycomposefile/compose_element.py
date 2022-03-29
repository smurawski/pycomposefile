from .elements import Element


class ComposeElement:
    elements = {}

    def __init__(self, config, compose_path=""):
        self.compose_path = compose_path
        for key in self.elements.keys():
            transform, spec_url = self.elements[key]
            config_value = config.pop(key, None)
            element = Element(key, transform, config_value, spec_url, self.compose_path)
            self.__setattr__(key, element)
        for key in config.keys():
            # raise Exception(f"Failed to map {key} in {compose_path}")
            pass

    @classmethod
    def from_parsed_yaml(cls, name, config, compose_path):
        if config is None:
            return None
        compose_path = f"{compose_path}/{name}"
        return cls(config, compose_path)

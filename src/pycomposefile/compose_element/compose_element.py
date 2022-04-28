from .compose_datatype_transformer import ComposeDataTypeTransformer


class ComposeElement(ComposeDataTypeTransformer):
    element_keys = {}

    def __init__(self, config, compose_path=""):
        self.compose_path = compose_path
        for key in self.element_keys.keys():
            config_element = config.pop(key, None)
            key_config = self.element_keys[key]
            self.set_supported_property_from_config(key, key_config, config_element, compose_path)
        for key in config.keys():
            # raise Exception(f"Failed to map {key} in {compose_path}")
            pass

    def set_supported_property_from_config(self, key, key_config, value, compose_path):
        valid_values = None
        if type(key_config[0]) is tuple:
            transform, valid_values = key_config[0]
        else:
            transform = key_config[0]

        if transform is not None:
            if isinstance(value, dict):
                value = transform(value, key, compose_path)
            elif isinstance(value, list):
                value = transform(value, key, compose_path)
            elif value is not None:
                value = self.transform_supported_data(transform, value, valid_values)
        else:
            # TODO: Logging message if value was not None
            value = None
        self.__setattr__(key, value)

    @classmethod
    def from_parsed_yaml(cls, config, name, compose_path):
        if config is None:
            return None
        compose_path = f"{compose_path}/{name}"
        return cls(config, compose_path)

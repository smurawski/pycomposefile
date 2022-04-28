from .compose_datatype_transformer import ComposeDataTypeTransformer


class ComposeListOrMapElement(ComposeDataTypeTransformer, dict):
    def __init__(self, config, key=None, compose_path=None,):
        if compose_path is not None:
            self.compose_path = f"{compose_path}/{key}"

        if config is None:
            pass
        elif isinstance(config, dict):
            for key in config.keys():
                value = self.replace_environment_variables(config[key])
                key = self.replace_environment_variables(key)
                self[key] = value
        elif isinstance(config, list):
            for line in config:
                line = self.replace_environment_variables(line)
                key, value = line.split("=")
                self[key] = value
        elif isinstance(config, str):
            config = self.replace_environment_variables(config)
            key, value = config.split("=")
            self[key] = value

    # def __init__(self, config, key=None, compose_path=None,):
    #     if isinstance(config, dict):
    #         for key in config.keys():
    #             value = self.replace_environment_variables(config[key])
    #             key = self.replace_environment_variables(key)
    #             self[key] = value
    #     elif isinstance(config, list):
    #         pass
    #     elif isinstance(config, str):
    #         pass
    #     else:
    #         pass

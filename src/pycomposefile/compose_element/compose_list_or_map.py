from .compose_datatype_transformer import ComposeDataTypeTransformer


class ComposeListOrMapElement(ComposeDataTypeTransformer, dict):
    def isValueEmpty(self, line):
        line = line.rstrip("=")
        if "=" not in line:
            return True
        else:
            return False

    def __init__(self, config, key=None, compose_path=None,):
        if compose_path is not None:
            self.compose_path = f"{compose_path}/{key}"

        if config is None:
            pass
        elif isinstance(config, dict):
            for key in config.keys():
                if config[key] is None:
                    value = None
                else:
                    value = self.replace_environment_variables(config[key])
                key = self.replace_environment_variables(key)
                self[key] = value
        elif isinstance(config, list):
            for line in config:
                line = self.replace_environment_variables(line)
                if self.isValueEmpty(line):
                    value = None
                    key = line.rstrip("=")
                else:
                    key, value = line.split("=")
                self[key] = value
        elif isinstance(config, str):
            config = self.replace_environment_variables(config)
            if self.isValueEmpty(config):
                value = None
                key = config.rstrip("=")
            else:
                key, value = config.split("=")
            self[key] = value

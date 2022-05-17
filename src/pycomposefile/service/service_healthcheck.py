from pycomposefile.compose_element import ComposeElement, ComposeStringOrListElement


class Test(ComposeStringOrListElement):
    pass


class HealthCheck(ComposeElement):
    element_keys = {
        "test": (Test, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#healthcheck"),
        "interval": (str, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#healthcheck"),
        "timeout": (str, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#healthcheck"),
        "retries": (int, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#healthcheck"),
        "start_period": (str, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#healthcheck"),
    }

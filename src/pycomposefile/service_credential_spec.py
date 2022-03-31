from .compose_element import ComposeElement


class CredentialSpec(ComposeElement):
    element_keys = {
        "file": (str, ""),
        "registry": (None,
                     "https://github.com/compose-spec/compose-spec/blob/master/spec.md#credential_spec"),
        "config": (None,
                   "https://github.com/compose-spec/compose-spec/blob/master/spec.md#credential_spec")
    }

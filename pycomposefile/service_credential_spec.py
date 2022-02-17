from .compose_element import ComposeElement


class CredentialSpec(ComposeElement):
    supported_keys = {
        "file": str,
    }

    unsupported_keys = {
        "registry": ("Windows containers are not supported by Azure ContainersApps",
                     "https://docs.microsoft.com/azure/container-apps/containers#limitations",
                     "https://github.com/compose-spec/compose-spec/blob/master/spec.md#credential_spec"),
        "config": ("gMSAs are not supported by Azure ContainerApps",
                   "https://docs.microsoft.com/azure/container-apps/containers#limitations",
                   "https://github.com/compose-spec/compose-spec/blob/master/spec.md#credential_spec")
    }

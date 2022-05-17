from pycomposefile.compose_element import ComposeListOrMapElement, ComposeStringOrListElement, ComposeElement


class Aliases(ComposeStringOrListElement):
    pass


class LinkLocalIps(ComposeStringOrListElement):
    pass


class Network(ComposeElement):
    element_keys = {
        "aliases": (Aliases, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#aliases"),
        "ipv4_address": (str, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#ipv4_address-ipv6_address"),
        "ipv6_address": (str, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#ipv4_address-ipv6_address"),
        "link_local_ips": (LinkLocalIps, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#link_local_ips"),
        "priority": (int, "https://github.com/compose-spec/compose-spec/blob/master/spec.md#priority"),
    }


class Networks(ComposeListOrMapElement):
    transform = Network.from_parsed_yaml

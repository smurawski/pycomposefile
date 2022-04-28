from collections import OrderedDict
from pycomposefile.service import Service


class ComposeFile:
    ordered_services = OrderedDict()

    def __init__(self, deserialized_compose_file):
        version = deserialized_compose_file.pop("version", None)
        if version is not None:
            version = str(version)
        self.version = version
        self.services = OrderedDict()
        self.compose_path = "services"
        for service in deserialized_compose_file["services"].keys():
            self.services[service] = Service.from_parsed_yaml(
                deserialized_compose_file["services"][service],
                service,
                self.compose_path
            )
        for service_name in self.services.keys():
            self._append_ordered_service(service_name)

    def _append_ordered_service(self, service_name):
        service = self.services[service_name]
        if service.depends_on is None:
            self.ordered_services[service_name] = service
        else:
            for required_service in service.depends_on:
                if required_service not in self.ordered_services.keys():
                    self._append_ordered_service(required_service)
            self.ordered_services[service_name] = service

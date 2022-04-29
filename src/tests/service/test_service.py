import unittest
from ..compose_generator import ComposeGenerator


class TestComposeServices(unittest.TestCase):
    compose_with_no_services = """
version: 3.9
volumes:
  db-data:
    driver: flocker
    driver_opts:
      size: "10GiB"
"""

    compose_with_one_service = """
services:
  frontend:
    image: awesome/webapp
"""

    compose_with_one_service_complex = """
services:
  frontend:
    image: awesome/webapp
    container_name: myfrontend
    cpu_count: 1.5
"""

    compose_with_two_services = """
services:
  frontend:
    image: awesome/webapp
  backend:
    image: awesome/backend
"""

    def test_empty_services_throws_error(self):
        with self.assertRaises(KeyError):
            ComposeGenerator.convert_yaml_to_compose_file(self.compose_with_no_services)

    def test_name_matches_with_one_service(self):
        compose_file = ComposeGenerator.convert_yaml_to_compose_file(self.compose_with_one_service)
        self.assertIsNotNone(compose_file.services["frontend"])

    def test_compose_path_matches_name_with_one_service(self):
        compose_file = ComposeGenerator.convert_yaml_to_compose_file(self.compose_with_one_service)
        self.assertEqual(compose_file.services["frontend"].compose_path, 'services/frontend')

    def test_names_match_with_two_services(self):
        compose_file = ComposeGenerator.convert_yaml_to_compose_file(self.compose_with_two_services)
        self.assertEqual(list(compose_file.services.keys()), ["frontend", "backend"])

    def test_compose_paths_matches_name_with_two_services(self):
        compose_file = ComposeGenerator.convert_yaml_to_compose_file(self.compose_with_two_services)
        self.assertEqual(compose_file.services["frontend"].compose_path, 'services/frontend')
        self.assertEqual(compose_file.services["backend"].compose_path, 'services/backend')

    def test_container_name_assigned_from_service(self):
        compose_file = ComposeGenerator.convert_yaml_to_compose_file(self.compose_with_one_service_complex)
        self.assertEqual(compose_file.services["frontend"].container_name, "myfrontend")

    def test_cpu_count_assigned_from_service(self):
        compose_file = ComposeGenerator.convert_yaml_to_compose_file(self.compose_with_one_service_complex)
        self.assertEqual(compose_file.services["frontend"].cpu_count, 1.5)

    def test_expose_from_service(self):
        compose_file = ComposeGenerator.get_compose_with_one_service_with_deploy()
        self.assertIs(type(compose_file.services["frontend"].expose[0]), int)
        self.assertIn(3000, compose_file.services["frontend"].expose)

    def test_multiple_expose_from_service(self):
        compose_file = ComposeGenerator.get_compose_with_one_service_with_multiple_expose()
        self.assertEqual(compose_file.services["frontend"].expose, [3000, 4000, 5000])

    def test_command_string_from_service(self):
        compose_file = ComposeGenerator.get_compose_with_one_service_with_deploy()
        self.assertEqual(compose_file.services["frontend"].command.command_string(), "bundle exec thin -p 3000")

    def test_command_list_from_service(self):
        compose_file = ComposeGenerator.get_compose_with_command_list()
        self.assertEqual("bundle exec thin -p 3000", compose_file.services["frontend"].command.command_string())

    def test_command_list_with_quotes_from_service(self):
        compose_file = ComposeGenerator.get_compose_with_command_list_with_quotes()
        self.assertEqual('echo "hello world"', compose_file.services["frontend"].command.command_string())

    def test_structured_ports_from_service(self):
        compose_file = ComposeGenerator.get_compose_with_structured_ports()
        self.assertEqual(80, compose_file.services["frontend"].ports[0].target)
        self.assertEqual(8443, compose_file.services["frontend"].ports[1].published)
        self.assertEqual("192.168.1.11", compose_file.services["frontend"].ports[1].host_ip)

    def test_entrypoint_from_service(self):
        compose_file = ComposeGenerator.get_compose_with_entrypoint_no_command()
        self.assertEqual("/code/entrypoint.sh", compose_file.services["frontend"].entrypoint.command_string())

    def test_entrypoint_list_from_service(self):
        entrypoint = "php -d zend_extension=/usr/local/lib/php/extensions/no-debug-non-zts-20100525/xdebug.so"
        entrypoint += " -d memory_limit=-1 vendor/bin/phpunit"
        compose_file = ComposeGenerator.get_compose_with_entrypoint_as_list_no_command()
        self.assertEqual(entrypoint, compose_file.services["frontend"].entrypoint.command_string())

    def test_entrypoint_and_command_from_service(self):
        compose_file = ComposeGenerator.get_compose_with_entrypoint_and_command()
        self.assertEqual('/code/entrypoint.sh echo "hello world"', compose_file.services["frontend"].entrypoint_and_command())

    def test_mem_reservation_from_service(self):
        compose_file = ComposeGenerator.get_compose_with_memory_reservation()
        self.assertEqual(1610612736, compose_file.services["frontend"].mem_reservation.value)
        self.assertEqual(1.5, compose_file.services["frontend"].mem_reservation.as_gigabytes())


if __name__ == '__main__':
    unittest.main()

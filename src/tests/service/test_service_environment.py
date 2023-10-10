from unittest import TestCase

from pycomposefile import compose_file

from ..compose_generator import ComposeGenerator


class TestComposeServiceEnvironment(TestCase):
    def test_service_with_environment_map(self):
        compose_file = ComposeGenerator.get_compose_with_environment_map()

        self.assertEqual(compose_file.services["frontend"].environment["RACK_ENV"], "development")
        self.assertEqual(compose_file.services["frontend"].environment["SHOW"], "true")
        self.assertIsNone(compose_file.services["frontend"].environment["USER_INPUT"])

    def test_service_with_environment_list(self):
        compose_file = ComposeGenerator.get_compose_with_environment_list()

        self.assertEqual(compose_file.services["frontend"].environment["RACK_ENV"], "development")
        self.assertEqual(compose_file.services["frontend"].environment["SHOW"], "true")
        self.assertIsNone(compose_file.services["frontend"].environment["USER_INPUT"])

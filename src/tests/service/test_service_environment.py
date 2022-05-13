from unittest import TestCase, mock
import os

from src.pycomposefile import compose_file

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

    @mock.patch.dict(os.environ, {"RACK_ENV": "test"})
    @mock.patch.dict(os.environ, {"test": "https://127.0.0.1"})
    @mock.patch.dict(os.environ, {"VERSION": "release"})
    def test_service_with_os_environment_vars(self):
        compose_file = ComposeGenerator.get_compose_with_os_environment_vars()

        self.assertEqual(compose_file.services["frontend"].environment["RACK_ENV"], "test")
        self.assertEqual(compose_file.services["frontend"].environment["URL"], "https://127.0.0.1")
        self.assertEqual(compose_file.services["frontend"].environment["VERSION"], "release")

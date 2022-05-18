import unittest

from ..compose_generator import ComposeGenerator


class TestComposeServiceEnvironmentFile(unittest.TestCase):
    def test_service_with_single_environment_file(self):
        compose_file = ComposeGenerator.get_compose_with_network()

        self.assertEqual(compose_file.services["grafana"].network_mode, "bridge")

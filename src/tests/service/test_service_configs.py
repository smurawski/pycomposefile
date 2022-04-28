import unittest
from ..compose_generator import ComposeGenerator


class TestServiceConfig(unittest.TestCase):

    def test_service_config_from_string(self):
        compose_file = ComposeGenerator.get_compose_with_string_configs()
        self.assertEqual(compose_file.services["frontend"].configs[0].source, 'my_config')

    def test_service_config_from_dict(self):
        compose_file = ComposeGenerator.get_compose_with_structured_configs()
        self.assertEqual(compose_file.services["frontend"].configs[1].source, 'another_config')
        self.assertEqual(compose_file.services["frontend"].configs[1].target, '/db_config')

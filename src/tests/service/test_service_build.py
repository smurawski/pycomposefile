import unittest
from ..compose_generator import ComposeGenerator


class TestComposeServices(unittest.TestCase):

    def test_build_context_from_service(self):
        compose_file = ComposeGenerator.get_compose_with_one_service_with_build_context()
        self.assertEqual(compose_file.services["frontend"].build.context, './webapp')

    def test_specific_build_context_from_service(self):
        compose_file = ComposeGenerator.get_compose_with_one_service_with_specific_build_context()
        self.assertEqual(compose_file.services["frontend"].build.context, './webapp')

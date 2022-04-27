import unittest
from ..compose_generator import ComposeGenerator


class TestServiceCredentialSpec(unittest.TestCase):

    def test_service_credential_spec_with_file_path(self):
        compose_file = ComposeGenerator.get_compose_with_file_credential_spec()
        self.assertEqual(compose_file.services["frontend"].credential_spec.file, "my-credential-spec.json")

    def test_service_credential_spec_with_registry_path(self):
        compose_file = ComposeGenerator.get_compose_with_registry_credential_spec()
        self.assertEqual(compose_file.services["frontend"].credential_spec.registry, "my-credential-spec")

    def test_service_credential_spec_with_config_path(self):
        compose_file = ComposeGenerator.get_compose_with_config_credential_spec()
        self.assertEqual(compose_file.services["frontend"].credential_spec.config, "my_credential_spec")

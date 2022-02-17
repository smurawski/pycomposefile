import unittest
from pycomposefile import ComposeFile
from pycomposefile.unsupported import UnsupportedConfiguration
from compose_generator import ComposeGenerator
from tests import compose_generator


class TestComposeServiceDeploy(unittest.TestCase):
    compose_with_no_deploy = """
services:
  frontend:
    image: awesome/webapp
"""

    def test_service_with_no_deploy(self):
        compose_file = ComposeFile(self.compose_with_no_deploy)
        self.assertIsNone(compose_file.services["frontend"].deploy)

    def test_service_with_deploy(self):
        compose_file = ComposeGenerator.get_compose_with_one_service_with_deploy()
        deploy = compose_file.services["frontend"].deploy
        self.assertIsNotNone(deploy)
        self.assertEqual(deploy.endpoint_mode, "vip")

    def test_service_with_deploy_labels(self):
        compose_file = ComposeGenerator.get_compose_with_one_service_with_deploy()
        deploy = compose_file.services["frontend"].deploy
        expected = {
            "com.example.description": "This label will appear on the web service",
            "com.example.otherstuff": "random things"
        }
        self.assertDictEqual(deploy.labels, expected)

    def test_service_with_unsupported_configuration_in_deploy(self):
        compose_file = ComposeGenerator.get_compose_with_one_service_with_deploy()
        deploy = compose_file.services["frontend"].deploy
        self.assertIsInstance(deploy.placement, UnsupportedConfiguration)
        self.assertEqual(str(deploy.placement),
                         "Unable to specify placement constraints or preferences for placement at services/frontend/deploy")

    def test_service_with_deploy_resources(self):
        compose_file = ComposeGenerator.get_compose_with_one_service_with_deploy()
        deploy = compose_file.services["frontend"].deploy
        self.assertIsNotNone(deploy)
        self.assertEqual(deploy.resources.limits.cpus, 0.50)

    def test_compose_path_for_service_with_deploy(self):
        compose_file = ComposeGenerator.get_compose_with_one_service_with_deploy()
        deploy = compose_file.services["frontend"].deploy
        self.assertEqual(deploy.compose_path, "services/frontend/deploy")

    def test_service_with_deploy_update_config(self):
        compose_file = ComposeGenerator.get_compose_with_one_service_with_deploy()
        deploy = compose_file.services["frontend"].deploy
        self.assertIsNotNone(deploy.update_config)

    def test_service_with_deploy_rollback_config(self):
        compose_file = ComposeGenerator.get_compose_with_one_service_with_deploy()
        deploy = compose_file.services["frontend"].deploy
        self.assertIsNotNone(deploy.rollback_config)
        self.assertEqual(deploy.rollback_config.monitor, "5m")


if __name__ == '__main__':
    unittest.main()

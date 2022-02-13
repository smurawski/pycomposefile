import unittest
from pycompose import ComposeFile
from pycompose.unsupported import UnsupportedConfiguration


class TestComposeServiceDeploy(unittest.TestCase):
    compose_with_no_deploy = """
services:
  frontend:
    image: awesome/webapp
"""

    compose_with_deploy = """
services:
  frontend:
    image: awesome/webapp
    ports:
      - "8080:80"
    deploy:
      mode: replicated
      replicas: 2
      endpoint_mode: vip
      placement:
        constraints:
          - disktype=ssd
      labels:
        com.example.description: "This label will appear on the web service"
        com.example.otherstuff: "random things"
"""

    compose_with_deploy_resources = """
services:
  frontend:
    image: awesome/webapp
    ports:
      - "8080:80"
    deploy:
      mode: replicated
      replicas: 2
      endpoint_mode: vip
      resources:
        limits:
          cpus: '0.50'
          memory: 50M
          pids: 1
        reservations:
          cpus: '0.25'
          memory: 20M
"""

    def test_service_with_no_deploy(self):
        compose_file = ComposeFile(self.compose_with_no_deploy)
        self.assertIsNone(compose_file.services["frontend"].deploy)

    def test_service_with_deploy(self):
        compose_file = ComposeFile(self.compose_with_deploy)
        deploy = compose_file.services["frontend"].deploy
        self.assertIsNotNone(deploy)
        self.assertEqual(deploy.endpoint_mode, "vip")

    def test_service_with_deploy_labels(self):
        compose_file = ComposeFile(self.compose_with_deploy)
        deploy = compose_file.services["frontend"].deploy
        expected = {
            "com.example.description": "This label will appear on the web service",
            "com.example.otherstuff": "random things"
        }
        self.assertDictEqual(deploy.labels, expected)

    def test_service_with_unsupported_configuration_in_deploy(self):
        compose_file = ComposeFile(self.compose_with_deploy)
        deploy = compose_file.services["frontend"].deploy
        self.assertIsInstance(deploy.placement, UnsupportedConfiguration)
        self.assertEqual(str(deploy.placement),
                         "Unable to specify placement constraints or preferences for placement at services/frontend/deploy")

    def test_service_with_deploy_resources(self):
        compose_file = ComposeFile(self.compose_with_deploy_resources)
        deploy = compose_file.services["frontend"].deploy
        self.assertIsNotNone(deploy)
        self.assertEqual(deploy.resources.limits.cpus, 0.50)

    def test_compose_path_for_service_with_deploy(self):
        compose_file = ComposeFile(self.compose_with_deploy)
        deploy = compose_file.services["frontend"].deploy
        self.assertEqual(deploy.compose_path, "services/frontend/deploy")


if __name__ == '__main__':
    unittest.main()

import unittest
from pycompose import ComposeFile


class TestComposeVersion(unittest.TestCase):
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

    def test_service_with_deploy_resources(self):
        compose_file = ComposeFile(self.compose_with_deploy_resources)
        deploy = compose_file.services["frontend"].deploy
        self.assertIsNotNone(deploy)
        self.assertEqual(deploy.resources.limits.cpus, "0.50")


if __name__ == '__main__':
    unittest.main()

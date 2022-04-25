import unittest
from ..compose_generator import ComposeGenerator


class TestComposeVersion(unittest.TestCase):
    compose_with_no_version = """
services:
  frontend:
    image: awesome/webapp
    ports:
      - "443:8043"
    networks:
      - front-tier
      - back-tier
    configs:
      - httpd-config
    secrets:
      - server-certificate
"""

    compose_with_version_2 = """
version: 2.7
services:
  frontend:
    image: awesome/webapp
    ports:
      - "443:8043"
    networks:
      - front-tier
      - back-tier
    configs:
      - httpd-config
    secrets:
      - server-certificate
"""

    compose_with_version_3 = """
version: 3.8
services:
  frontend:
    image: awesome/webapp
    ports:
      - "443:8043"
    networks:
      - front-tier
      - back-tier
    configs:
      - httpd-config
    secrets:
      - server-certificate
"""

    compose_with_unknown_version = """
version: 100.1.alpha
services:
  frontend:
    image: awesome/webapp
    ports:
      - "443:8043"
    networks:
      - front-tier
      - back-tier
    configs:
      - httpd-config
    secrets:
      - server-certificate
"""

    def test_no_version_present(self):
        compose_file = ComposeGenerator.convert_yaml_to_compose_file(self.compose_with_no_version)
        self.assertIsNone(compose_file.version)

    def test_v2_version_present(self):
        compose_file = ComposeGenerator.convert_yaml_to_compose_file(self.compose_with_version_2)
        self.assertEqual(compose_file.version, "2.7")

    def test_v3_version_present(self):
        compose_file = ComposeGenerator.convert_yaml_to_compose_file(self.compose_with_version_3)
        self.assertEqual(compose_file.version, "3.8")

    def test_unknown_version_present(self):
        compose_file = ComposeGenerator.convert_yaml_to_compose_file(self.compose_with_unknown_version)
        self.assertEqual(compose_file.version, "100.1.alpha")


if __name__ == '__main__':
    unittest.main()

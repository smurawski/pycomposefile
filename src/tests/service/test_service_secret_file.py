import unittest

from ..compose_generator import ComposeGenerator


class TestComposeServiceSecretsFile(unittest.TestCase):
    def test_service_with_single_secret(self):
        secret_value = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n"

        compose_file = ComposeGenerator.get_compose_with_one_secret()
        secret_from_file = compose_file.secrets["my_secret"].file.readFile()

        self.assertEqual(compose_file.services["frontend"].secrets[0].source, "my_secret")
        self.assertEqual(compose_file.secrets["my_secret"].file, "./sample/my_secret.txt")
        self.assertEqual(secret_from_file, secret_value)

    def test_service_with_external_secret(self):
        compose_file = ComposeGenerator.get_compose_with_external_secret()

        self.assertEqual(compose_file.services["frontend"].secrets[0].source, "my_other_secret")
        self.assertEqual(compose_file.secrets["my_other_secret"].external, True)

    def test_service_with_long_syntax(self):
        secret_value = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n"

        compose_file = ComposeGenerator.get_compose_with_long_syntax()
        secret_from_file = compose_file.secrets["my_secret"].file.readFile()

        self.assertEqual(compose_file.services["frontend"].secrets[0].source, "my_secret")
        self.assertEqual(compose_file.services["frontend"].secrets[0].target, "redis_secret")
        self.assertEqual(compose_file.services["frontend"].secrets[0].uid, 103)
        self.assertEqual(compose_file.services["frontend"].secrets[0].gid, 103)
        self.assertEqual(compose_file.secrets["my_secret"].file, "./sample/my_secret.txt")
        self.assertEqual(secret_from_file, secret_value)

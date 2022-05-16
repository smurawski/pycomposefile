from unittest import TestCase
import os
from ..compose_generator import ComposeGenerator


class TestNoBraceNoUnderscoreNoDigitEnvironmentVariable(TestCase):

    def test_uppercase_in_string_value(self):
        env_var = "TESTNAME"
        os.environ[env_var] = "fred"
        compose_file = ComposeGenerator.get_compose_with_string_value(env_var)
        self.assertEqual(compose_file.services["frontend"].image, "awesome/fred")

    def test_uppercase_in_decimal_value(self):
        env_var = "TESTCPUCOUNT"
        os.environ[env_var] = "1.5"
        compose_file = ComposeGenerator.get_compose_with_decimal_value(env_var)
        self.assertEqual(compose_file.services["frontend"].cpu_count, 1.5)

    def test_uppercase_two_variables_in_string_value(self):
        first_env_var = "HOSTPORT"
        second_env_var = "CONTAINERPORT"
        os.environ[first_env_var] = "8080"
        os.environ[second_env_var] = "80"
        compose_file = ComposeGenerator.get_with_two_environment_variables_in_string_value(first_env_var, second_env_var)
        self.assertEqual(f"{compose_file.services['frontend'].ports[0]}", "8080:80/tcp")
        self.assertEqual(compose_file.services["frontend"].ports[0].published, "8080")
        self.assertEqual(compose_file.services["frontend"].ports[0].target, "80")

    def test_lowercase_in_string_value(self):
        env_var = "testname"
        os.environ[env_var] = "fred"
        compose_file = ComposeGenerator.get_compose_with_string_value(env_var)
        self.assertEqual(compose_file.services["frontend"].image, "awesome/fred")

    def test_lowercase_in_decimal_value(self):
        env_var = "testcpucount"
        os.environ[env_var] = "1.5"
        compose_file = ComposeGenerator.get_compose_with_decimal_value(env_var)
        self.assertEqual(compose_file.services["frontend"].cpu_count, 1.5)

    def test_lowercase_two_variables_in_string_value(self):
        first_env_var = "hostport"
        second_env_var = "containerport"
        os.environ[first_env_var] = "8080"
        os.environ[second_env_var] = "80"
        compose_file = ComposeGenerator.get_with_two_environment_variables_in_string_value(first_env_var, second_env_var)
        self.assertEqual(f"{compose_file.services['frontend'].ports[0]}", "8080:80/tcp")
        self.assertEqual(compose_file.services["frontend"].ports[0].published, "8080")
        self.assertEqual(compose_file.services["frontend"].ports[0].target, "80")

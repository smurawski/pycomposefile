import unittest
import os
from ..compose_generator import ComposeGenerator


class TestBracesNoUnderscoreNoDigitVariableInterpolation(unittest.TestCase):

    def test_uppercase_in_string_value(self):
        env_var = "TESTNAME"
        os.environ[env_var] = "fred"
        braced_env_var = "{" + env_var + "}"
        compose_file = ComposeGenerator.get_compose_with_string_value(braced_env_var)
        self.assertEqual(compose_file.services["frontend"].image, "awesome/fred")

    def test_uppercase_with_default_when_unset_in_string_value(self):
        env_var = "DEFAULTUNSET"
        os.unsetenv(env_var)
        braced_env_with_default_unset = "{" + env_var + ":-bob}"
        compose_file = ComposeGenerator.get_compose_with_string_value(braced_env_with_default_unset)
        self.assertEqual(compose_file.services["frontend"].image, "awesome/bob")

    def test_uppercase_in_decimal_value(self):
        env_var = "TESTCPUCOUNT"
        os.environ[env_var] = "1.5"
        braced_env_var = "{" + env_var + "}"
        compose_file = ComposeGenerator.get_compose_with_decimal_value(braced_env_var)
        self.assertEqual(compose_file.services["frontend"].cpu_count, 1.5)

    def test_uppercase_two_variables_in_string_value(self):
        first_env_var = "HOSTPORT"
        second_env_var = "CONTAINERPORT"
        os.environ[first_env_var] = "8080"
        os.environ[second_env_var] = "80"
        braced_first_env_var = "{" + first_env_var + "}"
        braced_second_env_var = "{" + second_env_var + "}"
        compose_file = ComposeGenerator.get_with_two_environment_variables_in_string_value(braced_first_env_var, braced_second_env_var)
        self.assertEqual(f"{compose_file.services['frontend'].ports[0]}", "8080:80/tcp")
        self.assertEqual(compose_file.services['frontend'].ports[0].published, "8080")
        self.assertEqual(compose_file.services['frontend'].ports[0].target, "80")

    def test_lowercase_in_string_value(self):
        env_var = "testname"
        os.environ[env_var] = "fred"
        braced_env_var = "{" + env_var + "}"
        compose_file = ComposeGenerator.get_compose_with_string_value(braced_env_var)
        self.assertEqual(compose_file.services["frontend"].image, "awesome/fred")

    def test_lowercase_with_default_when_unset_in_string_value(self):
        env_var = "defaultunset"
        os.unsetenv(env_var)
        braced_env_with_default_unset = "{" + env_var + ":-bob}"
        compose_file = ComposeGenerator.get_compose_with_string_value(braced_env_with_default_unset)
        self.assertEqual(compose_file.services["frontend"].image, "awesome/bob")

    def test_lowercase_in_decimal_value(self):
        env_var = "testcpucount"
        os.environ[env_var] = "1.5"
        braced_env_var = "{" + env_var + "}"
        compose_file = ComposeGenerator.get_compose_with_decimal_value(braced_env_var)
        self.assertEqual(compose_file.services["frontend"].cpu_count, 1.5)

    def test_lowercase_two_variables_in_string_value(self):
        first_env_var = "hostport"
        second_env_var = "containerport"
        os.environ[first_env_var] = "8080"
        os.environ[second_env_var] = "80"
        braced_first_env_var = "{" + first_env_var + "}"
        braced_second_env_var = "{" + second_env_var + "}"
        compose_file = ComposeGenerator.get_with_two_environment_variables_in_string_value(braced_first_env_var, braced_second_env_var)
        self.assertEqual(f"{compose_file.services['frontend'].ports[0]}", "8080:80/tcp")
        self.assertEqual(compose_file.services["frontend"].ports[0].published, "8080")
        self.assertEqual(compose_file.services["frontend"].ports[0].target, "80")


if __name__ == '__main__':
    unittest.main()

from unittest import TestCase, mock
import os
from ..compose_generator import ComposeGenerator
from pycomposefile.compose_element import EmptyOrUnsetException


class TestBracesNoUnderscoreNoDigitVariableInterpolation(TestCase):

    @mock.patch.dict(os.environ, {"TESTNAME": "fred"})
    def test_uppercase_in_string_value(self):
        braced_env_var = "{TESTNAME}"
        compose_file = ComposeGenerator.get_compose_with_string_value(braced_env_var)
        self.assertEqual(compose_file.services["frontend"].image, "awesome/fred")

    def test_uppercase_with_default_when_unset_in_string_value(self):
        env_var = "DEFAULTUNSET"
        os.unsetenv(env_var)
        braced_env_with_default_unset = "{" + env_var + ":-bob}"
        compose_file = ComposeGenerator.get_compose_with_string_value(braced_env_with_default_unset)
        self.assertEqual(compose_file.services["frontend"].image, "awesome/bob")

    @mock.patch.dict(os.environ, {"TESTCPUCOUNT": "1.5"})
    def test_uppercase_in_decimal_value(self):
        braced_env_var = "{TESTCPUCOUNT}"
        compose_file = ComposeGenerator.get_compose_with_decimal_value(braced_env_var)
        self.assertEqual(compose_file.services["frontend"].cpu_count, 1.5)

    @mock.patch.dict(os.environ, {"HOSTPORT": "8080"})
    @mock.patch.dict(os.environ, {"CONTAINERPORT": "80"})
    def test_uppercase_two_variables_in_string_value(self):
        braced_first_env_var = "{HOSTPORT}"
        braced_second_env_var = "{CONTAINERPORT}"
        compose_file = ComposeGenerator.get_with_two_environment_variables_in_string_value(braced_first_env_var, braced_second_env_var)
        self.assertEqual(f"{compose_file.services['frontend'].ports[0]}", "8080:80/tcp")
        self.assertEqual(compose_file.services['frontend'].ports[0].published, "8080")
        self.assertEqual(compose_file.services['frontend'].ports[0].target, "80")

    @mock.patch.dict(os.environ, {"testname": "fred"})
    def test_lowercase_in_string_value(self):
        braced_env_var = "{testname}"
        compose_file = ComposeGenerator.get_compose_with_string_value(braced_env_var)
        self.assertEqual(compose_file.services["frontend"].image, "awesome/fred")

    def test_lowercase_with_default_when_unset_in_string_value(self):
        env_var = "defaultunset"
        os.unsetenv(env_var)
        braced_env_with_default_unset = "{" + env_var + ":-bob}"
        compose_file = ComposeGenerator.get_compose_with_string_value(braced_env_with_default_unset)
        self.assertEqual(compose_file.services["frontend"].image, "awesome/bob")

    @mock.patch.dict(os.environ, {"testcpucount": "1.5"})
    def test_lowercase_in_decimal_value(self):
        braced_env_var = "{testcpucount}"
        compose_file = ComposeGenerator.get_compose_with_decimal_value(braced_env_var)
        self.assertEqual(compose_file.services["frontend"].cpu_count, 1.5)

    @mock.patch.dict(os.environ, {"hostport": "8080"})
    @mock.patch.dict(os.environ, {"containerport": "80"})
    def test_lowercase_two_variables_in_string_value(self):
        braced_first_env_var = "{hostport}"
        braced_second_env_var = "{containerport}"
        compose_file = ComposeGenerator.get_with_two_environment_variables_in_string_value(braced_first_env_var, braced_second_env_var)
        self.assertEqual(f"{compose_file.services['frontend'].ports[0]}", "8080:80/tcp")
        self.assertEqual(compose_file.services["frontend"].ports[0].published, "8080")
        self.assertEqual(compose_file.services["frontend"].ports[0].target, "80")

    @mock.patch.dict(os.environ, {"RACK_ENV": "test"})
    @mock.patch.dict(os.environ, {"test": "https://127.0.0.1"})
    @mock.patch.dict(os.environ, {"VERSION": "release"})
    def test_service_with_os_environment_vars(self):
        compose_file = ComposeGenerator.get_compose_with_os_environment_vars()

        self.assertEqual(compose_file.services["frontend"].environment["RACK_ENV"], "test")
        self.assertEqual(compose_file.services["frontend"].environment["URL"], "https://127.0.0.1")
        self.assertEqual(compose_file.services["frontend"].environment["VERSION"], "release")

    @mock.patch.dict(os.environ, {"URL": "https://127.0.0.1"})
    def test_service_with_mandatory_env_vars(self):
        with self.assertRaises(EmptyOrUnsetException):
            ComposeGenerator.get_compose_with_mandatory_env_vars()

    def test_service_with_mandatory_unset_env_vars(self):
        with self.assertRaises(EmptyOrUnsetException):
            ComposeGenerator.get_compose_with_mandatory_unset_env_vars()

    @mock.patch.dict(os.environ, {"ENVIRONMENT": "local"})
    def test_service_with_double_dollar_sign_env_vars(self):
        compose_file = ComposeGenerator.get_compose_with_double_dollar_sign_env_vars()

        self.assertEqual(compose_file.services["frontend"].environment["ENVIRONMENT"], "$ENVIRONMENT")

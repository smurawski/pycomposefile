import unittest
from pycomposefile import ComposeFile
import os


class TestNoBraceNoUnderscoreNoDigitVariableInterpolation(unittest.TestCase):
    compose_with_uppercase_environment_variable_in_string_value = """
services:
  frontend:
    image: awesome/$TESTNAME
"""

    compose_with_uppercase_environment_variable_in_decimal_value = """
services:
  frontend:
    image: awesome/website
    cpu_count: $TESTCPUCOUNT
"""

    compose_with_lowercase_environment_variable_in_string_value = """
services:
  frontend:
    image: awesome/$testname
"""

    compose_with_lowercase_environment_variable_in_decimal_value = """
services:
  frontend:
    image: awesome/website
    cpu_count: $testcpucount
"""

    compose_with_two_uppercase_environment_variables_in_string_value = """
services:
  frontend:
    image: awesome/website
    cpu_count: 1.5
    ports: "$HOSTPORT:$CONTAINERPORT"
"""

    def test_uppercase_in_string_value(self):
        os.environ["TESTNAME"] = "fred"
        compose_file = ComposeFile(self.compose_with_uppercase_environment_variable_in_string_value)
        self.assertEqual(compose_file.services["frontend"].image, "awesome/fred")

    def test_uppercase_in_decimal_value(self):
        os.environ["TESTCPUCOUNT"] = "1.5"
        compose_file = ComposeFile(self.compose_with_uppercase_environment_variable_in_decimal_value)
        self.assertEqual(compose_file.services["frontend"].cpu_count, 1.5)

    def test_two_variables_uppercase_in_string_value(self):
        os.environ["HOSTPORT"] = "8080"
        os.environ["CONTAINERPORT"] = "80"
        compose_file = ComposeFile(self.compose_with_two_uppercase_environment_variables_in_string_value)
        self.assertEqual(compose_file.services["frontend"].ports, "8080:80")

    def test_lowercase_in_string_value(self):
        os.environ["testname"] = "fred"
        compose_file = ComposeFile(self.compose_with_lowercase_environment_variable_in_string_value)
        self.assertEqual(compose_file.services["frontend"].image, "awesome/fred")

    def test_lowercase_in_decimal_value(self):
        os.environ["testcpucount"] = "1.5"
        compose_file = ComposeFile(self.compose_with_lowercase_environment_variable_in_decimal_value)
        self.assertEqual(compose_file.services["frontend"].cpu_count, 1.5)


class TestBracesNoUnderscoreNoDigitVariableInterpolation(unittest.TestCase):
    compose_with_uppercase_environment_variable_in_string_value = """
services:
  frontend:
    image: awesome/${TESTNAME}
"""

    compose_with_uppercase_with_default_if_unset_environment_variable_in_string_value = """
services:
  frontend:
    image: awesome/${DEFAULTUNSET:-bob}
"""

    compose_with_uppercase_environment_variable_in_decimal_value = """
services:
  frontend:
    image: awesome/website
    cpu_count: ${TESTCPUCOUNT}
"""

    compose_with_lowercase_environment_variable_in_string_value = """
services:
  frontend:
    image: awesome/${testname}
"""

    compose_with_lowercase_environment_variable_in_decimal_value = """
services:
  frontend:
    image: awesome/website
    cpu_count: ${testcpucount}
"""

    compose_with_two_uppercase_environment_variables_in_string_value = """
services:
  frontend:
    image: awesome/website
    cpu_count: 1.5
    ports: "${HOSTPORT}:${CONTAINERPORT}"
"""

    def test_uppercase_in_string_value(self):
        os.environ["TESTNAME"] = "fred"
        compose_file = ComposeFile(self.compose_with_uppercase_environment_variable_in_string_value)
        self.assertEqual(compose_file.services["frontend"].image, "awesome/fred")

    def test_uppercase_with_default_when_unset_in_string_value(self):
        os.environ.unsetenv("DEFAULTUNSET")
        compose_file = ComposeFile(self.compose_with_uppercase_with_default_if_unset_environment_variable_in_string_value)
        self.assertEqual(compose_file.services["frontend"].image, "awesome/bob")

    def test_uppercase_in_decimal_value(self):
        os.environ["TESTCPUCOUNT"] = "1.5"
        compose_file = ComposeFile(self.compose_with_uppercase_environment_variable_in_decimal_value)
        self.assertEqual(compose_file.services["frontend"].cpu_count, 1.5)

    def test_two_variables_uppercase_in_string_value(self):
        os.environ["HOSTPORT"] = "8080"
        os.environ["CONTAINERPORT"] = "80"
        compose_file = ComposeFile(self.compose_with_two_uppercase_environment_variables_in_string_value)
        self.assertEqual(compose_file.services["frontend"].ports, "8080:80")

    def test_lowercase_in_string_value(self):
        os.environ["testname"] = "fred"
        compose_file = ComposeFile(self.compose_with_lowercase_environment_variable_in_string_value)
        self.assertEqual(compose_file.services["frontend"].image, "awesome/fred")

    def test_lowercase_in_decimal_value(self):
        os.environ["testcpucount"] = "1.5"
        compose_file = ComposeFile(self.compose_with_lowercase_environment_variable_in_decimal_value)
        self.assertEqual(compose_file.services["frontend"].cpu_count, 1.5)

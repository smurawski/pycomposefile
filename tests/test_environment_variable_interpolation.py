import unittest
from pycompose import ComposeFile
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

    def test_uppercase_in_string_value(self):
        os.environ["TESTNAME"] = "fred"
        compose_file = ComposeFile(self.compose_with_uppercase_environment_variable_in_string_value)
        self.assertEqual(compose_file.services["frontend"].image, "awesome/fred")

    def test_uppercase_in_decimal_value(self):
        os.environ["TESTCPUCOUNT"] = "1.5"
        compose_file = ComposeFile(self.compose_with_uppercase_environment_variable_in_decimal_value)
        self.assertEqual(compose_file.services["frontend"].cpu_count, 1.5)

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

    def test_uppercase_in_string_value(self):
        os.environ["TESTNAME"] = "fred"
        compose_file = ComposeFile(self.compose_with_uppercase_environment_variable_in_string_value)
        self.assertEqual(compose_file.services["frontend"].image, "awesome/fred")

    def test_uppercase_in_decimal_value(self):
        os.environ["TESTCPUCOUNT"] = "1.5"
        compose_file = ComposeFile(self.compose_with_uppercase_environment_variable_in_decimal_value)
        self.assertEqual(compose_file.services["frontend"].cpu_count, 1.5)

    def test_lowercase_in_string_value(self):
        os.environ["testname"] = "fred"
        compose_file = ComposeFile(self.compose_with_lowercase_environment_variable_in_string_value)
        self.assertEqual(compose_file.services["frontend"].image, "awesome/fred")

    def test_lowercase_in_decimal_value(self):
        os.environ["testcpucount"] = "1.5"
        compose_file = ComposeFile(self.compose_with_lowercase_environment_variable_in_decimal_value)
        self.assertEqual(compose_file.services["frontend"].cpu_count, 1.5)

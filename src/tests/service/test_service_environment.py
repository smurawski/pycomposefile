from unittest import TestCase

from pycomposefile import compose_file
from pycomposefile.compose_element.compose_list_or_map import ComposeListOrMapElement

from ..compose_generator import ComposeGenerator


class TestComposeServiceEnvironment(TestCase):
    def test_service_with_environment_map(self):
        compose_file = ComposeGenerator.get_compose_with_environment_map()

        self.assertEqual(compose_file.services["frontend"].environment["RACK_ENV"], "development")
        self.assertEqual(compose_file.services["frontend"].environment["SHOW"], "true")
        self.assertIsNone(compose_file.services["frontend"].environment["USER_INPUT"])

    def test_service_with_environment_list(self):
        compose_file = ComposeGenerator.get_compose_with_environment_list()

        self.assertEqual(compose_file.services["frontend"].environment["RACK_ENV"], "development")
        self.assertEqual(compose_file.services["frontend"].environment["SHOW"], "true")
        self.assertIsNone(compose_file.services["frontend"].environment["USER_INPUT"])

    def test_kvp_with_multiple_equals_issue_35(self):
        """Test for issue #35: KVP strings with multiple '=' should split on first '=' only"""
        # Test the exact scenario from the issue
        element = ComposeListOrMapElement("JAVA_OPTS=foo=bar&&baz=buzz")
        self.assertEqual(element["JAVA_OPTS"], "foo=bar&&baz=buzz")

    def test_kvp_splitting_edge_cases(self):
        """Test various edge cases for KVP splitting to prevent regression"""
        test_cases = [
            # (input_string, expected_key, expected_value)
            ("KEY=value", "KEY", "value"),
            ("KEY=value=extra", "KEY", "value=extra"),
            ("KEY=a=b=c=d", "KEY", "a=b=c=d"),
            ("URL=http://example.com:8080/path?param=value", "URL", "http://example.com:8080/path?param=value"),
            ("CONFIG=key1=val1,key2=val2", "CONFIG", "key1=val1,key2=val2"),
            ("COMPLEX=a=b&c=d&e=f", "COMPLEX", "a=b&c=d&e=f"),
            ("NO_VALUE", "NO_VALUE", None),
        ]

        for input_string, expected_key, expected_value in test_cases:
            with self.subTest(input=input_string):
                element = ComposeListOrMapElement(input_string)
                self.assertEqual(element[expected_key], expected_value)

    def test_empty_value_handling(self):
        """Test handling of empty values - this is existing behavior that should be preserved"""
        # EMPTY= should result in None (existing behavior)
        element = ComposeListOrMapElement("EMPTY=")
        self.assertIsNone(element["EMPTY"])

        # Test the isValueEmpty method directly
        element_test = ComposeListOrMapElement(None)
        self.assertTrue(element_test.isValueEmpty("KEY="))
        self.assertFalse(element_test.isValueEmpty("KEY=value"))

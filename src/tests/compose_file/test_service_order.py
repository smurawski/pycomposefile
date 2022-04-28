import unittest

from ..compose_generator import ComposeGenerator


class TestServiceOrdering(unittest.TestCase):

    @unittest.skip("unexpected failure when run as group.")
    def test_service_order(self):
        compose_file = ComposeGenerator.get_compose_with_service_dependencies()
        self.assertEqual(list(compose_file.ordered_services.keys()), ['db', 'redis', 'frontend', 'reporting'])

    def test_multiple_service_order(self):
        compose_file = ComposeGenerator.get_compose_with_multiple_service_dependencies()
        self.assertEqual(list(compose_file.ordered_services.keys()), ['redis', 'db', 'frontend', 'reporting'])

    def test_circular_service_order(self):
        with self.assertRaises(RecursionError):
            ComposeGenerator.get_compose_with_circular_service_dependencies()

    def test_service_order_with_conditions(self):
        compose_file = ComposeGenerator.get_compose_with_service_dependencies_and_conditions()
        self.assertEqual(compose_file.services["frontend"].depends_on[0].condition, 'service_healthy')


if __name__ == '__main__':
    unittest.main()

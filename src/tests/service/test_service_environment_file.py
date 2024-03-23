import unittest

from ..compose_generator import ComposeGenerator


class TestComposeServiceEnvironmentFile(unittest.TestCase):
    def test_service_with_single_environment_file(self):
        compose_file = ComposeGenerator.get_compose_with_environment_file_single()
        environment_from_file = compose_file.services["frontend"].env_file.readFile()

        self.assertEqual(compose_file.services["frontend"].env_file[0], "./sample/test.env")
        self.assertEqual(environment_from_file["RACK_ENV"], "development")
        self.assertEqual(environment_from_file["VAR"], '"quoted"')
        self.assertEqual(environment_from_file["SOME_VAR"], '"value with equals=sign"')

    def test_service_with_list_environment_file(self):
        compose_file = ComposeGenerator.get_compose_with_environment_file_list()
        environment_from_file = compose_file.services["frontend"].env_file.readFile()

        self.assertEqual(compose_file.services["frontend"].env_file, ['./sample/common.env', './sample/apps/web.env', './sample/opt/runtime_opts.env'])
        self.assertEqual(environment_from_file["RACK_ENV"], "development")
        self.assertEqual(environment_from_file["VAR"], '"quoted"')
        self.assertEqual(environment_from_file["BAR"], "faz")
        self.assertEqual(environment_from_file["FOO"], '"bar"')
        self.assertEqual(environment_from_file["BAZ"], "snafu")
        self.assertEqual(environment_from_file["STAGE"], "dev")
        self.assertEqual(environment_from_file["SHOW"], "false")

    def test_service_with_resolved_environment_variables(self):
        compose_file = ComposeGenerator.get_compose_with_environment_file_list()
        environment_from_file = compose_file.services["frontend"].resolve_environment_hierarchy()

        self.assertEqual(environment_from_file["RACK_ENV"], "canary")
        self.assertEqual(environment_from_file["VAR"], '"quoted"')
        self.assertEqual(environment_from_file["BAR"], "faz")
        self.assertEqual(environment_from_file["FOO"], '"bar"')
        self.assertEqual(environment_from_file["BAZ"], "snafu")
        self.assertEqual(environment_from_file["STAGE"], "dev")
        self.assertEqual(environment_from_file["SHOW"], "true")
        self.assertIsNone(environment_from_file["USER_INPUT"])

import unittest
from ..compose_generator import ComposeGenerator


class TestComposeServices(unittest.TestCase):

    def test_blkio_from_service(self):
        compose_file = ComposeGenerator.get_compose_with_one_service_with_deploy()
        self.assertEqual(compose_file.services["frontend"].blkio_config.weight, 300)
        self.assertEqual(compose_file.services["frontend"].blkio_config.weight_device[0].weight, 400)
        self.assertEqual(compose_file.services["frontend"].blkio_config.device_read_bps[0].path, "/dev/sdb")
        self.assertEqual(compose_file.services["frontend"].blkio_config.device_write_iops[0].rate, "30")


if __name__ == '__main__':
    unittest.main()

import re
from ..compose_element import ComposeStringOrListElement


class Command(ComposeStringOrListElement):
    def __init__(self, config, key=None, compose_path=None):
        self.transform = str
        super().__init__(config, key, compose_path)

    def command_string(self):
        capture = re.compile(r"\w+(\s\w+)+")
        string = ""
        for v in self:
            if len(self) > 1 and capture.match(v):
                string += f"\"{v}\""
            else:
                string += f"{v} "
        return string.lstrip().rstrip()
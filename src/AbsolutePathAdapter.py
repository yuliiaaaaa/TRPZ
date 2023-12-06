import os
from src.RelativePath import RelativePath
class AbsolutePathAdapter:
    def __init__(self, relative_path):
        self.relative_path = relative_path

    def get_absolute_path(self):
        if os.path.isabs(self.relative_path.get_relative_path()):
            return self.relative_path.get_relative_path()

        return os.path.abspath(self.relative_path.get_relative_path())

def convert_to_absolute_path(repo_name):
    relative_path = RelativePath(repo_name)
    path_adapter = AbsolutePathAdapter(relative_path)
    return path_adapter.get_absolute_path()
from abc import ABC, abstractmethod
from datetime import date

class IVersionControlSystem(ABC):
    @abstractmethod
    def commit(self, path, file_name, message):
        pass

    @abstractmethod
    def watch_history(self, repo_name):
        pass

    @abstractmethod
    def initialize_repository(self, repo_directory,vcs_type):
        pass
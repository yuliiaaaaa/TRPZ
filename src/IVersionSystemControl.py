from abc import ABC, abstractmethod
from datetime import date

class IVersionControlSystem(ABC):
    @abstractmethod
    def commit(self, repo_name, file_name, repo_id, message, commit_date: date):
        pass

    @abstractmethod
    def watch_history(self, repo_name):
        pass

    @abstractmethod
    def initialize_repository(self, repo_directory,vcs_type):
        pass

    # @abstractmethod
    # def watch_repository(self, type_iterator):
    #     pass

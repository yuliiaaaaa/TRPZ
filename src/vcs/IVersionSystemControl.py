from abc import ABC, abstractmethod
from datetime import date

class IVersionControlSystem(ABC):

    def accept(self, visitor):
        pass

    @abstractmethod
    def commit(self, path, file_name, message):
        pass

    @abstractmethod
    def watch_history(self, repo_name):
        pass

    @abstractmethod
    def initialize_repository(self, repo_directory,vcs_type):
        pass

    @abstractmethod
    def show_repositories(self):
        pass

    @abstractmethod
    def visualization(self,repo_path):
        pass

    @abstractmethod
    def push(self, repo_path,remote_name,branch_name,remote_url):
        pass

    @abstractmethod
    def update(self, repo_directory):
        pass

    @abstractmethod
    def pull(self,repo_path):
        pass

    @abstractmethod
    def fetch(self, repo_path):
        pass

    @abstractmethod
    def list_branches(self, repo_directory):
        pass

    @abstractmethod
    def add(self,repo_path,file_name):
        pass
    @abstractmethod
    def create_branch(self, repo_path, branch_name):
        pass

    @abstractmethod
    def merge_branch(self, repo_path, source_branch, destination_branch):
        pass

    @abstractmethod
    def tag(self, repo_path, tag_name, tag_message=''):
        pass

    def status(self,repo_path):
        pass
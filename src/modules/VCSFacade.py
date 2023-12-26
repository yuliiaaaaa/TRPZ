from src.DB.DatabaseConnection import connection
from src.modules.MyVCSVisitor import MyVCSVisitor
from src.modules.VCSFactory import VersionControlFactory


class VCSFacade:
    def __init__(self, connection):
        self.connection = connection

    def initialize_repository(self, version_control, vcs_type, repo_directory):
        return version_control.initialize_repository(repo_directory, vcs_type)

    def commit_changes(self, version_control, repo_name, file_name, message):
        return version_control.commit(repo_name, file_name, message)

    def watch_history(self, version_control, repo_name):
        return version_control.watch_history(repo_name)

    def show_repositories(self, version_control):
        return version_control.accept(MyVCSVisitor())

    def visualization(self, version_control, repo_name):
        return version_control.visualization(repo_name)

    def push(self, version_control, repo_path,remote_name,branch_name,remote_url):
        return version_control.push(repo_path,remote_name,branch_name,remote_url)

    def update(self, version_control, repo_directory,branch_name):
        return version_control.update(repo_directory,branch_name)

    def pull(self, version_control, repo_path,branch_name):
        return version_control.pull(repo_path,branch_name)

    def fetch(self, version_control, repo_path):
        return version_control.fetch(repo_path)

    def list(self, version_control, repo_directory):
        return version_control.list_branches(repo_directory)

    def add(self, version_control, repo_path, file_name):
        return version_control.add(repo_path, file_name)

    def branch(self, version_control, repo_path, branch_name):
        return version_control.create_branch(repo_path, branch_name)

    def merge(self, version_control, repo_path, source_branch, destination_branch):
        return version_control.merge_branch(repo_path, source_branch, destination_branch)

    def tag(self, version_control, repo_path, tag_name, tag_message=''):
        return version_control.tag(repo_path,tag_name,tag_message)


    def status(self,version_control,repo_path):
        return version_control.status(repo_path)
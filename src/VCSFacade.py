import os
from colorama import Fore
from DatabaseConnection import connection
from src.AbsolutePathAdapter import AbsolutePathAdapter, convert_to_absolute_path
from src.GitIterator import GitRepositoryIterator
from src.MercurialIterator import MercurialRepositoryIterator
from src.MyVCSVisitor import MyVCSVisitor
from src.Repository import Repository
from src.SVNIterator import SVNRepositoryIterator
from src.VCSFactory import VersionControlFactory

class VCSFacade:
    def __init__(self, connection):
        self.connection = connection

    def initialize_repository(self, vcs_type, repo_directory):
        version_control = VersionControlFactory.create_version_control_system(connection, vcs_type)
        version_control.initialize_repository(repo_directory, vcs_type)

    def commit_changes(self, version_control, repo_name, file_name, message):
        version_control.commit(repo_name, file_name, message)

    def watch_history(self, version_control, repo_name):
        version_control.watch_history(repo_name)

    def show_repositories(self, version_control):
        version_control.accept(MyVCSVisitor())


import os

import git
from git import Repo, GitCommandError
from colorama import Fore, Style

from IVersionSystemControl import IVersionControlSystem
from Repository import Repository
from RepositoryDTO import RepositoryDTO


class GitVersionControl(IVersionControlSystem):
    def __init__(self, connection):
        self.connection = connection
        self.repo = None  # Initialize the repository variable

    def initialize_repository(self, repo_directory, vcs_type):
        git_dir = os.path.join(repo_directory, ".git")
        repo_name = os.path.basename(repo_directory)
        if os.path.exists(git_dir) and os.path.isdir(git_dir):
            print(f"Git repository already exists in: {repo_directory}")
            self.repo = Repo(repo_directory)  # Initialize the Git repository
        else:
            try:
                self.repo = Repo.init(repo_directory)  # Initialize the Git repository
                print(f"Git repository initialized successfully in: {repo_directory}")
                # Insert repository details into the database using the existing Repository class
                repository = Repository(self.connection)
                repository.create(RepositoryDTO(None, repo_name, vcs_type, repo_directory))
            except Exception as e:
                print(f"Error initializing Git repository: {e}")

    def commit(self, repo_path, file_name, message):
        try:
            repo = git.Repo(repo_path, search_parent_directories=True)
            if not repo.bare:
                index = repo.index
                if index.diff(None):
                    index.commit(message)
                    print("Git: Changes committed successfully.")
                else:
                    print("Git: No changes to commit.")
            else:
                print("Git: Not in a Git repository.")
        except git.exc.NoSuchPathError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error committing changes: {e}")

    def watch_history(self, repo_path):
        repo = git.Repo(repo_path, search_parent_directories=True)
        if not repo.bare:
            commit_history = list(repo.iter_commits())

            print("Commit History:")
            for i, commit in enumerate(commit_history):
                print(f"Commit {i + 1}:")
                print(f"Author: {commit.author.name} <{commit.author.email}>")
                print(f"Date: {commit.authored_datetime}")
                print(f"Message: {commit.message}")
                print()

        else:
            print("Git: Not in a Git repository.")


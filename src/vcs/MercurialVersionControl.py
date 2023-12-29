import os
import subprocess

import hglib
from colorama import Fore
from graphviz import Digraph
from mercurial import hg, ui, commands
from datetime import date

from CustomErrors import VCS_Error
from src.Entities.RepositoryDTO import RepositoryDTO
from src.Iterators.MercurialIterator import MercurialRepositoryIterator
from src.Repository.Repository import Repository
from src.shared.config import encoding, username
from src.vcs.IVersionSystemControl import IVersionControlSystem


class MercurialVersionControl(IVersionControlSystem):
    def __init__(self, connection):
        self.connection = connection
        self.ui = ui.ui()

    def accept(self, visitor):
        return visitor.visit_mercurial(self)

    def initialize_repository(self, repo_directory, vcs_type):
        try:
            repo = hglib.init(repo_directory)
            if repo:
                # Insert repository details into the database using the existing Repository class
                repo_name = os.path.basename(repo_directory)
                repository = Repository(self.connection)
                repository.create(RepositoryDTO(None, repo_name, vcs_type, repo_directory))
                return f"Mercurial repository initialized successfully in: {repo_directory}"
        except Exception as e:
            raise VCS_Error(f"Error initializing Mercurial repository: {e}")

    def show_repositories(self):
        repositories = Repository(self.connection).find_all()
        iterator = MercurialRepositoryIterator(repositories)

        repository_info = "\nRepositories for Mercurial:\n"
        for repository in iterator:
            repository_info += (
                    Fore.BLUE + f"Name: {repository.name}, VCS Type: {repository.vcs_type}, URL: {repository.url}" + Fore.GREEN + "\n"
            )
        return repository_info
    def status(self, repo_path):
        try:
            client = hglib.open(repo_path)
            status = client.status()

            if not status:
                return "No changes or untracked files in the repository."

            return status

        except hglib.error.CommandError as e:
            raise VCS_Error(f"Error getting repository status: {e}")
        except Exception as e:
            raise VCS_Error(f"Error during status check: {e}")

    def tag(self, repo_path, tag_name, tag_message=''):
        try:
            client = hglib.open(repo_path)
            # Ensure there is at least one commit in the repository before tagging
            if len(client.log()) > 0:
                client.tag(tag_name.encode('utf-8'),user=username)
                return f"Tag '{tag_name}' created successfully."
            else:
                return "Error: No commits found in the repository. Please commit changes before creating a tag."

        except hglib.error.CommandError as e:
            raise VCS_Error(f"Error creating tag: {e}")
        except Exception as e:
            raise VCS_Error(f"Error during tag creation: {e}")

    def merge_branch(self, repo_path, source_branch, destination_branch='default'):
        try:
            client = hglib.open(repo_path)

            # Update the working directory to the destination branch
            client.update(rev=destination_branch)

            # Merge changes from the source branch into the destination branch
            client.merge(branch=source_branch)

            return f"Merged changes from '{source_branch}' into '{destination_branch}' successfully."

        except hglib.error.CommandError as e:
            raise VCS_Error(f"Error during merge: {e}")
        except Exception as e:
            raise VCS_Error(f"Error occurred: {e}")

    def list_branches(self, repo_path):
        try:
            client = hglib.open(repo_path)
            branches = client.branches()

            if isinstance(branches, bytes):
                # Handle case where only one branch is returned as bytes
                branch_names = [branches.decode('utf-8')]
            else:
                # Handle case where multiple branches are returned as a list of tuples
                branch_names = [branch[0].decode('utf-8') for branch in branches]

            return branch_names
        except hglib.error.CommandError as e:
            raise RuntimeError(f"Error listing branches: {e}")
        except Exception as e:
            raise RuntimeError(f"Error during listing branches: {e}")

    def fetch(self, repo_path):
        try:
            client = hglib.open(repo_path)
            client.pull()
            return "Fetch successful: fetched changes from the default branch of the remote repository."

        except hglib.error.CommandError as e:
            raise VCS_Error(f"Error fetching changes: {e}")
        except Exception as e:
            raise VCS_Error(f"Error during fetch: {e}")

    def pull(self, repo_path,branch_name):
            try:
                client = hglib.open(repo_path)
                client.pull(rev=branch_name)
                return f"Fetch successful: fetched changes from the '{branch_name}' branch of the remote repository."

            except hglib.error.CommandError as e:
                raise VCS_Error(f"Error during pull: {e}")
            except Exception as e:
                raise VCS_Error(f"Error fetching changes: {e}")

    def update(self, repo_path,branch_name):
        try:
            client = hglib.open(repo_path)
            client.update()
            return f"Update successful"
        except hglib.error.CommandError as e:
            raise VCS_Error(f"Error updating repository: {e}")
        except Exception as e:
            raise VCS_Error(f"Error during update: {e}")

    def watch_history(self, repo_path):
        try:
            client = hglib.open(repo_path)
            log = client.log()

            commit_log = []
            for commit in log:
                commit_info = {
                    'commit_id': commit.node,
                    'author': commit.author,
                    'email': '',  # Hg library does not provide email directly
                    'message': commit.desc.strip(),
                    'timestamp': '',  # Hg library does not provide timestamp directly
                }
                commit_log.append(commit_info)

            return commit_log

        except hglib.error.CommandError as e:
            raise VCS_Error(f"Error getting commit log: {e}")
        except Exception as e:
            raise VCS_Error(f"Error occurred: {e}")

    def add(self,repo_path, file_name):
        try:
            client = hglib.open(repo_path)
            abs_file_path = os.path.join(repo_path, file_name)  # Get absolute file path

            if abs_file_path not in client.status(unknown=True):
                client.add(abs_file_path.encode('utf-8'))  # Add the file to Mercurial tracking

            return f"File '{file_name}' added to Mercurial."
        except hglib.error.CommandError as e:
            raise VCS_Error(f"Error adding file to Mercurial: {e}")
        except Exception as e:
            raise VCS_Error(f"An unexpected error occurred while adding file to Mercurial: {e}")

    def commit(self,repo_path, file_name, message):
        try:
            client = hglib.open(repo_path)
            abs_file_path = os.path.join(repo_path, file_name)  # Get absolute file path

            if abs_file_path in client.status(unknown=True):
                client.commit(message.encode('utf-8'), user=username)
                return f"Changes to file '{file_name}' committed successfully."
            else:
                return f"File '{file_name}' is not yet added to Mercurial. Please add it before committing."
        except hglib.error.CommandError as e:
            raise VCS_Error(f"Error committing changes to Mercurial: {e}")
        except Exception as e:
            raise VCS_Error(f"An unexpected error occurred while committing changes to Mercurial: {e}")

    def visualization(self,repo_path):
        try:
            client = hglib.open(repo_path)
            commit_history = client.log()

            graph = Digraph(comment='Commit History', format='pdf')

            for commit in commit_history:
                commit_desc = commit.desc.decode('utf-8') if isinstance(commit.desc, bytes) else commit.desc
                commit_author = commit.author.decode('utf-8') if isinstance(commit.author, bytes) else commit.author

                label = f"{commit.node[:7]}\n{commit_author}\n{commit_desc.splitlines()[0]}"

                graph.node(commit.node[:7], label)

                for parent in commit.parents:
                    parent_str = parent.decode('utf-8') if isinstance(parent, bytes) else parent
                    graph.edge(parent_str[:7], commit.node[:7])

            graph.render(filename='commit_history_graph', view=True)

            return "Commit history graph created: commit_history_graph.pdf"

        except hglib.error.CommandError as e:
            raise VCS_Error(f"Error accessing repository: {e}")
        except Exception as e:
            raise VCS_Error(f"Error creating commit history graph: {e}")
    def create_branch(self, repo_path, branch_name):
        try:
            client = hglib.open(repo_path)
            client.branch(branch_name.encode('utf-8'))
            return f"Branch '{branch_name}' created successfully."

        except hglib.error.CommandError as e:
            raise VCS_Error(f"Error creating branch: {e}")
        except Exception as e:
            raise VCS_Error(f"Error during branch creation: {e}")

    def list_patches(self,repo_path):
        try:
            # Fetch revision IDs using hg log
            output = subprocess.run(['hg', 'log', '--template', '{node}\n'],
                                    cwd=repo_path, capture_output=True, text=True, check=True)
            patches = output.stdout.splitlines()
            return patches
        except subprocess.CalledProcessError as e:
            raise VCS_Error(f"Error during listing patches: {e}")
        except Exception as ex:
            raise VCS_Error(f"An unexpected error occurred: {ex}")

    def log(self, repo_path):
        try:
            client = hglib.open(repo_path)
            commits = []

            # Retrieve log information from the repository
            log_info = client.log()

            for entry in log_info:
                commit_info = {
                    'rev': entry.rev,
                    'node': entry.node.decode(),
                    'author': entry.author.decode(),
                    'date': entry.date.decode(),
                    'message': entry.desc.decode()
                }
                commits.append(commit_info)

            return commits

        except hglib.error.CommandError as e:
            raise VCS_Error(f"Error getting log information: {e}")
        except Exception as e:
            raise VCS_Error(f"Error during log retrieval: {e}")

    def push(self, repo_path, remote_name='default', branch_name='default', remote_url=None):
        try:
            client = hglib.open(repo_path)

            if remote_url is not None:
                # If a remote URL is provided, attempt to add the remote
                client.addremotepath(remote_name, remote_url)

            client.push(remote_name)
            return f"Changes pushed to '{remote_name}/{branch_name}'."

        except hglib.error.CommandError as e:
            raise VCS_Error(f"Error pushing changes: {e}")
        except Exception as e:
            raise VCS_Error(f"Error during push: {e}")
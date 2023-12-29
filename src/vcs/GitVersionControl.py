import os

import hglib
from graphviz import Digraph
from pyvis.network import Network
import git
import networkx as nx
from git import Repo
from colorama import Fore

from CustomErrors import NoChangesToCommitError, VCS_Error, NotInVCSRepositoryError, VCSCommitError, \
    VCSInitializationError, VCSRepoExistsError
from src.Entities.RepositoryDTO import RepositoryDTO
from src.Repository.Repository import Repository
from src.vcs.IVersionSystemControl import IVersionControlSystem

from src.Iterators.GitIterator import GitRepositoryIterator


class GitVersionControl(IVersionControlSystem):
    def __init__(self, connection):
        self.connection = connection
        self.repo = None

    def accept(self, visitor):
       return visitor.visit_git(self)

    def initialize_repository(self, repo_directory, vcs_type):
        git_dir = os.path.join(repo_directory, ".git")
        repo_name = os.path.basename(repo_directory)

        if os.path.isdir(git_dir):
            raise VCSRepoExistsError(f"Git repository already exists in: {repo_directory}")
        else:
            try:
                repo = Repo.init(repo_directory)
                if not repo.bare:
                    repository = Repository(self.connection)
                    repository.create(RepositoryDTO(None, repo_name, vcs_type, repo_directory))
                    return f"Git repository initialized successfully in: {repo_directory}"
                else:
                    raise VCSInitializationError(f"Error initializing Git repository in: {repo_directory}")
            except Exception as e:
                raise VCSInitializationError(f"Error initializing Git repository: {e}")

    def add(repo_path, file_name):
        try:
            repo = git.Repo(repo_path, search_parent_directories=True)
            if not repo.bare:
                index = repo.index
                index.add([file_name])
                return f"File '{file_name}' added to Git staging area."
            else:
                raise NotInVCSRepositoryError("Not in a Version Control System repository.")
        except git.exc.NoSuchPathError as e:
            raise VCS_Error(e)
        except git.exc.GitCommandError as e:
            raise VCS_Error(f"Error adding file to Git: {e}")
        except Exception as e:
            raise VCS_Error(f"An unexpected error occurred while adding file to Git: {e}")

    def commit(self,repo_path, file_name, message):
        try:
            repo = git.Repo(repo_path, search_parent_directories=True)
            if not repo.bare:
                index = repo.index
                index.add([file_name])
                if index.diff(None):
                    index.commit(message)
                    return f"Changes to file '{file_name}' committed successfully."
                else:
                    raise NoChangesToCommitError("No changes to commit.")
            else:
                raise NotInVCSRepositoryError("Not in a Version Control System repository.")
        except git.exc.NoSuchPathError as e:
            raise VCS_Error(e)
        except git.exc.GitCommandError as e:
            raise VCSCommitError(f"Error committing changes to Git: {e}")
        except Exception as e:
            raise VCS_Error(f"An unexpected error occurred while committing changes to Git: {e}")

    def watch_history(self, repo_path):
        try:
            repo = git.Repo(repo_path)
            commits = list(repo.iter_commits('HEAD'))

            commit_log = []
            for commit in commits:
                commit_info = {
                    'commit_id': commit.hexsha,
                    'author': commit.author.name,
                    'email': commit.author.email,
                    'message': commit.message.strip(),
                    'timestamp': commit.authored_datetime.strftime('%Y-%m-%d %H:%M:%S')
                }
                commit_log.append(commit_info)
            print(commit_log)
            return commit_log

        except git.exc.NoSuchPathError as e:
            raise VCS_Error(f"Error accessing repository: {e}")
        except Exception as e:
            raise VCS_Error(f"Error getting commit log: {e}")


    def show_repositories(self):
        repositories = Repository(self.connection).find_all()
        iterator = GitRepositoryIterator(repositories)

        repository_info = "\nRepositories for Git:\n"
        for repository in iterator:
            repository_info += (
                    Fore.BLUE + f"Name: {repository.name}, VCS Type: {repository.vcs_type}, URL: {repository.url}" + Fore.GREEN + "\n"
            )
        return repository_info

    def visualization(self,repo_path):
        try:
            repo = git.Repo(repo_path)
            commit_history = list(repo.iter_commits())

            graph = Digraph(comment='Commit History')  # Initialize the graph object

            # Add commits as nodes and relationships between them (parent relationships)
            for commit in commit_history:
                # Get branch names pointing to this commit
                branches = [branch.name for branch in repo.branches if commit.hexsha in branch.commit.hexsha]

                # Create a label containing commit info and branch names
                label = f"{commit.hexsha[:7]}\n{commit.author.name}\n{commit.summary}\nBranches: {', '.join(branches)}"

                # Add the commit as a node with the label
                graph.node(commit.hexsha[:7], label)

                for parent in commit.parents:
                    graph.edge(parent.hexsha[:7], commit.hexsha[:7])

            # Save the graph to a file
            graph.render(filename='commit_history_graph', format='pdf', view=True)  # Save as PNG image

            return "Commit history graph created: commit_history_graph.png"

        except git.exc.NoSuchPathError as e:
            raise VCS_Error(f"Error accessing repository: {e}")
        except Exception as e:
            raise VCS_Error(f"Error creating commit history graph: {e}")

    def push(self, repo_path, remote_name='origin', branch_name='main',remote_url=None):
        try:
            repo = git.Repo(repo_path)

            if remote_name not in [remote.name for remote in repo.remotes]:
                if remote_url is None:
                    raise VCS_Error("Remote URL is required when adding a new remote.")

                # If remote doesn't exist, add a new remote with the specified URL
                origin = repo.create_remote(remote_name, remote_url)
                return f"Remote '{remote_name}' added. Set up to push changes to 'origin/{branch_name}'."

            remote = repo.remote(remote_name)

            if not repo.head.is_valid():
                repo.index.commit("Initial commit")

            remote.push(refspec=f"{branch_name}:{branch_name}")
            return f"Changes pushed to '{remote_name}/{branch_name}'."

        except git.exc.GitCommandError as e:
            raise VCS_Error(f"Error pushing changes: {e}")
        except Exception as e:
            raise VCS_Error(f"Error during push: {e}")

    def update(self, repo_path, branch_name='main'):
        try:
            repo = git.Repo(repo_path)

            # Отримати оновлення з віддаленого репозиторію (fetch)
            repo.remotes.origin.fetch()

            # Перейти на вказану гілку (checkout)
            repo.git.checkout(branch_name)

            # Об'єднати зміни з віддаленої гілки в поточну (merge)
            repo.git.merge(f'origin/{branch_name}')

            return f"Оновлення успішно: взято зміни з 'origin/{branch_name}' та об'єднано їх."

        except git.exc.GitCommandError as e:
            raise VCS_Error(f"Помилка при оновленні репозиторію: {e}")
        except Exception as e:
            raise VCS_Error(f"Помилка під час оновлення: {e}")

    def pull(self, repo_path,branch_name='master'):
        try:
            repo = git.Repo(repo_path)
            origin = repo.remotes.origin

            # Fetch changes from the remote repository
            origin.fetch()

            # Pull changes from the specified remote branch into the local branch
            repo.git.checkout(branch_name)
            origin.pull(branch_name)

            return f"Pull successful: pulled changes from 'origin/{branch_name}'."

        except git.exc.GitCommandError as e:
            raise VCS_Error(f"Error during pull: {e}")
        except Exception as e:
            raise VCS_Error(f"Error occurred: {e}")

    def fetch(self, repo_path):
        try:
            repo = git.Repo(repo_path)
            repo.remotes.origin.fetch()
            return "Fetch successful: fetched changes from remote repository."

        except git.exc.GitCommandError as e:
            raise VCS_Error(f"Error fetching changes: {e}")
        except Exception as e:
            raise VCS_Error(f"Error during fetch: {e}")

    def list_branches(self, repo_path):
        try:
            repo = git.Repo(repo_path)
            branches = [str(branch) for branch in repo.branches]
            return branches

        except git.exc.GitCommandError as e:
            raise VCS_Error(f"Error listing branches: {e}")
        except Exception as e:
            raise VCS_Error(f"Error during listing branches: {e}")

    def list_patches(self, repo_path):
        try:
            repo = git.Repo(repo_path)

            # Retrieve all patches from the repository
            patches = [patch for patch in repo.git.format_patch('--stdout').split('From ') if patch.strip()]

            return patches

        except git.exc.GitCommandError as e:
            raise VCS_Error(f"Error listing patches: {e}")
        except Exception as e:
            raise VCS_Error(f"Error during listing patches: {e}")

    def create_branch(self, repo_path, branch_name):
        try:
            repo = git.Repo(repo_path)
            repo.git.branch(branch_name)
            return f"Branch '{branch_name}' created successfully."

        except git.exc.GitCommandError as e:
            raise VCS_Error(f"Error creating branch: {e}")
        except Exception as e:
            raise VCS_Error(f"Error during branch creation: {e}")

    def merge_branch(self,repo_path, source_branch, destination_branch='main'):
        try:
            repo = git.Repo(repo_path)

            # Checkout the target branch
            repo.git.checkout(destination_branch)

            # Merge changes from the source branch into the target branch
            repo.git.merge(source_branch)

            return f"Merged changes from '{source_branch}' into '{destination_branch}' successfully."

        except git.exc.GitCommandError as e:
            raise VCS_Error(f"Error during merge: {e}")
        except Exception as e:
            raise VCS_Error(f"Error occurred: {e}")

    def tag(self, repo_path, tag_name, tag_message=''):
        try:
            repo = git.Repo(repo_path)
            repo.create_tag(tag_name, message=tag_message)
            return f"Tag '{tag_name}' created successfully."

        except git.exc.GitCommandError as e:
            raise VCS_Error(f"Error creating tag: {e}")
        except Exception as e:
            raise VCS_Error(f"Error during tag creation: {e}")

    def status(self, repo_path):
        try:
            repo = git.Repo(repo_path)
            status = repo.git.status()
            return status

        except git.exc.GitCommandError as e:
            raise VCS_Error(f"Error getting repository status: {e}")
        except Exception as e:
            raise VCS_Error(f"Error during status check: {e}")


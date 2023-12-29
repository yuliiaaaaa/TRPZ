import os
import subprocess

import pysvn
from colorama import Fore
from graphviz import Digraph

from CustomErrors import VCS_Error
from src.vcs.IVersionSystemControl import IVersionControlSystem
from src.Repository.Repository import Repository
from src.Iterators.SVNIterator import SVNRepositoryIterator


class SVNVersionControl(IVersionControlSystem):
    def __init__(self, connection):
        self.connection = connection

    def accept(self, visitor):
        return visitor.visit_svn(self)


    def watch_history(self, repo_path):
        try:
            svn_log_command = ['svn', 'log', repo_path]
            output = subprocess.check_output(svn_log_command, text=True)
            return output
        except subprocess.CalledProcessError as e:
            # Handle errors if the 'svn log' command fails
            raise VCS_Error(f"Error retrieving SVN log: {e}")
        except Exception as ex:
            # Handle other unexpected errors
            raise VCS_Error(f"An unexpected error occurred: {ex}")

    def initialize_repository(self, repo_directory, vcs_type):
        svn_dir = os.path.join(repo_directory, ".svn")
        if os.path.exists(svn_dir) and os.path.isdir(svn_dir):
            print(f"SVN repository already exists in: {repo_directory}")
        else:
            try:
                client = pysvn.Client()
                client.checkout(repo_directory)
                print(f"SVN repository initialized successfully in: {repo_directory}")
            except pysvn.ClientError as svn_error:
                print(f"Error initializing SVN repository: {svn_error}")
            except Exception as e:
                print(f"Error initializing SVN repository: {e}")

    def update(self, repo_path):
        try:
            svn_update_command = ['svn', 'update', repo_path]
            subprocess.run(svn_update_command, check=True)
            return "SVN: Update completed successfully."
        except subprocess.CalledProcessError as e:
            raise VCS_Error(f"Error during SVN update: {e}")
        except Exception as ex:
            raise VCS_Error(f"An unexpected error occurred during update: {ex}")

    def list_branches(self, repo_path):
        branches_url = f"{repo_path}/branches"

        try:
            # Get the list of branches from the 'branches' directory
            branches_output = subprocess.run(['svn', 'list', branches_url], check=True,
                                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            branches_list = branches_output.stdout.splitlines()
            return branches_list
        except subprocess.CalledProcessError as e:
            raise VCS_Error(f"Error listing branches: {e.stderr}")

    def create_branch(self, repo_url, branch_name):
        branches_url = f"{repo_url}/branches"

        # Check if 'branches' directory exists
        try:
            subprocess.run(['svn', 'list', branches_url], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           text=True)
        except subprocess.CalledProcessError:
            # 'branches' directory does not exist, creating it
            pass
        else:
            # 'branches' directory exists, proceed to create the branch inside it
            branch_url = f"{branches_url}/{branch_name}"
            trunk_url = f"{repo_url}/trunk"

            try:
                subprocess.run(['svn', 'copy', trunk_url, branch_url],
                               check=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                return f"Branch '{branch_name}' created successfully"
            except subprocess.CalledProcessError as e:
                raise VCS_Error(f"Failed to create branch '{branch_name}': {e.stderr}")

    def fetch(self, repo_path):
        try:
            # Run 'svn update' to fetch changes from the repository
            svn_update_command = ['svn', 'update']
            subprocess.run(svn_update_command, cwd=repo_path, check=True)
            return "SVN: Fetch successful. Updated working copy."

        except subprocess.CalledProcessError as e:
            raise VCS_Error(f"Error fetching changes: {e}")
        except Exception as ex:
            raise VCS_Error(f"An unexpected error occurred: {ex}")

    def commit(self, repo_path, file_name, message):
        try:
            file_path = os.path.join(repo_path, file_name)
            # Commit the changes
            svn_commit_command = ['svn', 'commit', file_path, '-m', f'"{message}"']
            subprocess.run(svn_commit_command, cwd=repo_path, check=True)

            return f"SVN: File '{file_name}' added and changes committed successfully."
        except subprocess.CalledProcessError as e:
            # Handle errors if the commands fail
            raise VCS_Error(f"Error adding and committing changes: {e}")
        except Exception as ex:
            # Handle other unexpected errors
            raise VCS_Error(f"An unexpected error occurred: {ex}")

    def initialize_repository(self, repo_path,vcs_type):
        try:
            if not os.path.exists(os.path.join(repo_path, '.svn')):
                # Create the SVN repository
                svnadmin_create_command = ['svnadmin', 'create', repo_path]
                subprocess.run(svnadmin_create_command, check=True)

                # Checkout the repository to create a working copy
                svn_checkout_command = ['svn', 'checkout', f'file:///{repo_path}', repo_path]
                subprocess.run(svn_checkout_command, check=True)

                return "SVN: Repository initialized successfully."
            else:
                return "SVN: Repository already exists."
        except subprocess.CalledProcessError as e:
            raise VCS_Error(f"Error occurred during SVN initialization: {e}")
        except Exception as ex:
            raise VCS_Error(f"An unexpected error occurred: {ex}")


    def show_repositories(self):
        repositories = Repository(self.connection).find_all()
        iterator = SVNRepositoryIterator(repositories)

        repository_info = "\nRepositories for SVN\n"
        for repository in iterator:
            repository_info += (
                    Fore.BLUE + f"Name: {repository.name}, VCS Type: {repository.vcs_type}, URL: {repository.url}\n"+Fore.GREEN
            )
        return repository_info

    def add(self,repo_path, file_name):
        try:
            file_path = os.path.join(repo_path, file_name)
            svn_add_command = ['svn', 'add', file_path]
            subprocess.run(svn_add_command, check=True)
            return f"SVN: File '{file_name}' added successfully."
        except subprocess.CalledProcessError as e:
            raise VCS_Error(f"Error adding file '{file_name}': {e}")
        except Exception as ex:
            raise VCS_Error(f"An unexpected error occurred while adding file '{file_name}': {ex}")
    def merge_branch(self, repo_url, source_branch, destination_branch):
        try:
            svn_merge_command = ['svn', 'merge', f'^/branches/{source_branch}', f'^/branches/{destination_branch}']
            subprocess.run(svn_merge_command, check=True)

            return f"SVN: Merged changes from '{source_branch}' to '{destination_branch}' successfully."
        except subprocess.CalledProcessError as e:
            # Handle errors if the 'svn merge' command fails
            raise VCS_Error(f"Error merging branches: {e}")
        except Exception as ex:
            # Handle other unexpected errors
            raise VCS_Error(f"An unexpected error occurred: {ex}")

    def pull(self, repo_path):
        try:
            svn_pull_command = ['svn', 'pull', repo_path]
            subprocess.run(svn_pull_command, check=True)
            return "SVN: Pull completed successfully."
        except subprocess.CalledProcessError as e:
            raise VCS_Error(f"Error during SVN pull: {e}")
        except Exception as ex:
            raise VCS_Error(f"An unexpected error occurred during pull: {ex}")

    def push(self, repo_path):
        try:
            svn_push_command = ['svn', 'push', repo_path]
            subprocess.run(svn_push_command, check=True)
            return "SVN: Push completed successfully."
        except subprocess.CalledProcessError as e:
            raise VCS_Error(f"Error during SVN push: {e}")
        except Exception as ex:
            raise VCS_Error(f"An unexpected error occurred during push: {ex}")

    def tag(self, repo_url, tag_name, tag_message=None):
        tags_url = f"{repo_url}/tags"

        source_url = f"{repo_url}/{source_path}"  # Source path can be 'trunk', 'branches/branch_name', etc.

        try:
            # Check if 'tags' directory exists, create it if not
            subprocess.run(['svn', 'list', tags_url], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           text=True)
        except subprocess.CalledProcessError:
            # 'tags' directory doesn't exist, creating it
            try:
                subprocess.run(['svn', 'mkdir', tags_url, '-m', f"Creating 'tags' directory"], check=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            except subprocess.CalledProcessError as e:
                raise VCS_Error(f"Failed to create 'tags' directory: {e.stderr}")

        tag_url = f"{tags_url}/{tag_name}"

        try:
            subprocess.run(['svn', 'copy', source_url, tag_url, '-m', f"Creating tag '{tag_name}'"], check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return f"Tag '{tag_name}' created successfully"
        except subprocess.CalledProcessError as e:
            raise VCS_Error(f"Failed to create tag '{tag_name}': {e.stderr}")

    def visualization(self, repo_url):
        try:
            # Fetch SVN log for the repository
            svn_log_command = ['svn', 'log', '--xml', repo_url]
            log_output = subprocess.run(svn_log_command, capture_output=True, text=True, check=True).stdout

            # Initialize the graph object
            graph = Digraph(comment='Commit History', format='pdf')

            # Process XML log output to extract commit information
            commits = log_output.split('<logentry')

            for commit in commits[1:]:  # Skip first empty entry
                commit_info = commit.split('</logentry>')[0]
                revision = commit_info.split('revision="')[1].split('"')[0]
                author = commit_info.split('<author>')[1].split('</author>')[0]
                date = commit_info.split('<date>')[1].split('</date>')[0]
                message = commit_info.split('<msg>')[1].split('</msg>')[0]

                if revision and author and date and message:
                    graph.node(revision, f"Author: {author}\nDate: {date}\nMessage: {message}")

                if len(commits) > 1:
                    graph.edge(revision, commits[-1])

            # Save the graph to a file
            graph.render(filename='commit_history_graph', view=True)

            return "Commit history graph created: commit_history_graph.pdf"

        except subprocess.CalledProcessError as e:
            raise VCS_Error(f"Error accessing repository: {e}")
        except Exception as e:
            raise VCS_Error(f"Error creating commit history graph: {e}")

    def status(self, repo_path):
            try:
                svn_status_command = ['svn', 'status']
                status_output = subprocess.check_output(svn_status_command, cwd=repo_path, text=True)
                return status_output
            except subprocess.CalledProcessError as e:
                raise VCS_Error(f"Error occurred during status check: {e}")
            except Exception as ex:
                raise VCS_Error(f"An unexpected error occurred: {ex}")
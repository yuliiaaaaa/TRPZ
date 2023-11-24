import os
import pysvn
from colorama import Fore, Style

from IVersionSystemControl import IVersionControlSystem

class SVNVersionControl(IVersionControlSystem):
    def __init__(self, connection):
        self.connection = connection

    def commit(self, repo_url, message):
        try:
            client = pysvn.Client()
            client.checkin(repo_url, message)
            print(f"Committed changes with message: {message}")
        except pysvn.ClientError as svn_error:
            print(f"Error committing changes: {svn_error}")
        except Exception as e:
            print(f"Error committing changes: {e}")

    def watch_history(self, repo_url):
        try:
            client = pysvn.Client()
            log_entries = client.log(repo_url)
            for entry in log_entries:
                print(f"Revision {entry.revision.number}: {entry.message}")
        except pysvn.ClientError as svn_error:
            print(f"Error while watching commit history: {svn_error}")
        except Exception as e:
            print(f"Error while watching commit history: {e}")

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




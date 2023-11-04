from mercurial import hg, ui, commands
from datetime import date

class MercurialVersionControl:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.repo = hg.repository(ui.ui(), self.repo_path)

    def commit(self, repo_name, file_name, repo_id, message, commit_date):
        with self.repo.lock():
            # Add the file to the commit
            self.repo.add(file_name)

            # Commit the changes
            try:
                commit_user = f"{repo_id} <{repo_id}@example.com>"
                commit_date_str = commit_date.strftime('%Y-%m-%d %H:%M:%S %z')
                self.repo.commit(message, user=commit_user, date=commit_date_str)

                print(f"Committed changes for {file_name} with message: {message}")
            except hg.error.Abort as e:
                print(f"Error committing changes: {e}")

    def watch_history(self, repo_name):
        try:
            with self.repo.lock():
                # Display the commit history
                for rev in reversed(list(self.repo)):
                    changeset = self.repo[rev]
                    print(f"Revision: {changeset.rev()}")
                    print(f"User: {changeset.user()}")
                    print(f"Date: {changeset.date()}")
                    print(f"Message: {changeset.description()}")
                    print()
        except hg.error.Abort as e:
            print(f"Error while watching commit history: {e}")

    def initialize_repository(self, repo_directory):
        try:
            # Initialize a new Mercurial repository
            commands.init(ui.ui(), repo_directory)
            print(f"Mercurial repository initialized successfully in: {repo_directory}")
        except hg.error.Abort as e:
            print(f"Error initializing Mercurial repository: {e}")

import os

from colorama import Fore
import mercurial

from DatabaseConnection import connection
from GitIterator import GitRepositoryIterator
from GitVersionControl import GitVersionControl
from MercurialIterator import MercurialRepositoryIterator
from MercurialVersionControl import MercurialVersionControl
from Repository import Repository
from SVNIterator import SVNRepositoryIterator
from SVNVersionControl import SVNVersionControl


def show_menu():
    print(Fore.GREEN + "Welcome to VCS Console App!")
    print(
        "This application allows you to interact with various Version Control Systems (Git, Mercurial, SVN) using a simple console interface.")


def main_menu():
    while True:
        show_menu()

        print("Choose a Version Control System (VCS):")
        print("1. Git")
        print("2. Mercurial")
        print("3. SVN")
        print("5. Exit")

        choice = input("Enter the number of your choice: ")
        repo_name = None  # Initialize repo_name to None

        if choice == "1":
            repo_name = input("Enter the path to your Git repository: ")
            version_control = GitVersionControl(connection)
            process_vcs_commands(version_control, "Git", repo_name)  # Pass repo_name to process_vcs_commands
        elif choice == "2":
            try:
                repo_name = input("Enter the path to your Mercurial repository: ")
                version_control = MercurialVersionControl(connection)
            except mercurial.error.RepoError as e:
                print(f"Mercurial repository error: {e}")
                continue
            except Exception as e:
                print(f"Error initializing Mercurial Version Control: {e}")
                continue
            process_vcs_commands(version_control, "Mercurial", repo_name)  # Pass repo_name to process_vcs_commands
        elif choice == "3":
            repo_name = input("Enter the path to your SVN repository: ")
            version_control = SVNVersionControl(connection)
            process_vcs_commands(version_control, "SVN", repo_name)  # Pass repo_name to process_vcs_commands
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")


def show_repositories_for_vcs(vcs_type):
    repositories = Repository(connection).find_all()
    if vcs_type == "Git":
        iterator = GitRepositoryIterator(repositories)
    elif vcs_type == "Mercurial":
        iterator = MercurialRepositoryIterator(repositories)
    elif vcs_type == "SVN":
        iterator = SVNRepositoryIterator(repositories)
    else:
        print("Invalid VCS type")
        return

    # Display repositories for the chosen VCS type
    print(f"\nRepositories for {vcs_type}:")
    for repository in iterator:
        print(Fore.BLUE + f"Name: {repository.name}, VCS Type: {repository.vcs_type}, URL: {repository.url}"+Fore.GREEN)


def process_vcs_commands(version_control, vcs_type, repo_name):
    while True:
        print(f"Selected Version Control System: {vcs_type}")
        print(f"Current Repository: {repo_name}")  # Display the current repository
        print(f"Choose an action:")
        print("1. Commit")
        print("2. Watch History")
        print("3. Initialize Repository")
        print("4. Show Repositories")
        print("5. Back to Main Menu")

        action = input("Enter the number of your choice: ")

        if action == "1":
            file_name = input("Enter the file name: ")
            message = input("Enter the commit message: ")
            version_control.commit(repo_name, file_name, message)
        elif action == "2":
            version_control.watch_history(repo_name)
        elif action == "3":
            version_control.initialize_repository(repo_name, vcs_type)
        elif action == "4":
            show_repositories_for_vcs(vcs_type)
        elif action == "5":
            break
        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == '__main__':
    main_menu()

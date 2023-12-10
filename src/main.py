import os

from colorama import Fore
from DatabaseConnection import connection
from GitIterator import GitRepositoryIterator
from MercurialIterator import MercurialRepositoryIterator
from Repository import Repository
from SVNIterator import SVNRepositoryIterator
from src.AbsolutePathAdapter import AbsolutePathAdapter, convert_to_absolute_path
from src.VCSFacade import VCSFacade
from src.VCSFactory import VersionControlFactory


def show_menu():
    print(Fore.GREEN + "Welcome to VCS Console App!")
    print("This application allows you to interact with various Version Control Systems (Git, Mercurial, SVN) using a simple console interface.")

def main_menu():
    vcs_facade = VCSFacade(connection)
    version_control = None  # Initialize version_control object

    while True:
        show_menu()

        print("Choose a Version Control System (VCS):")
        print("1. Git")
        print("2. Mercurial")
        print("3. SVN")
        print("5. Exit")

        choice = input("Enter the number of your choice: ")
        repo_name = None

        if choice in ["1", "2", "3"]:
            vcs_type = "Git" if choice == "1" else "Mercurial" if choice == "2" else "SVN"
            repo_name = input(f"Enter the path to your {vcs_type} repository: ")
            repo_name = convert_to_absolute_path(repo_name)
            version_control = VersionControlFactory.create_version_control_system(connection, vcs_type)
            vcs_facade.initialize_repository(vcs_type, repo_name)

            while True:
                print(f"Selected Version Control System: {vcs_type}")
                print(f"Current Repository: {repo_name}")  # Display the current repository
                if not os.path.isdir(repo_name):
                    print("Error: Repository path is invalid or does not exist.")
                    break
                print(f"Choose an action:")
                print("1. Commit")
                print("2. Watch History")
                print("3. Show Repositories")
                print("4. Back to Main Menu")

                action = input("Enter the number of your choice: ")

                if action == "1":
                    if version_control:
                        file_name = input("Enter the file name: ")
                        message = input("Enter the commit message: ")
                        vcs_facade.commit_changes(version_control, repo_name, file_name, message)
                    else:
                        print("Version control not initialized.")
                elif action == "2":
                    if version_control:
                        vcs_facade.watch_history(version_control, repo_name)
                    else:
                        print("Version control not initialized.")
                elif action == "3":
                    vcs_facade.show_repositories(vcs_type)
                elif action == "4":
                    break
                else:
                    print("Invalid choice. Please enter a valid option.")
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == '__main__':
    main_menu()
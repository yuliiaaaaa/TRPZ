import logging
import threading
import socket

import networkx as nx
from matplotlib import pyplot as plt

from src.ConsoleLogger import ConsoleLogger
from src.PrintError import Printer
from src.modules.AbsolutePathAdapter import convert_to_absolute_path
from src.modules.VCSFacade import VCSFacade
from src.modules.VCSFactory import VersionControlFactory
from src.shared.config import encoding, SI, file_log, server_ports
from src.DB.DatabaseConnection import connection


def is_port_free(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((SI, port)) != 0


def find_free_port():
    for port in server_ports:
        if is_port_free(port):
            return port
    return None


def start_server_peer():
    logging.basicConfig(filename=file_log, level=logging.INFO)
    free_port = find_free_port()

    if free_port is None: return
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SI, free_port))
    server_socket.listen(1)
    logging.info(f"Server started on port {free_port}. Waiting for connections...")

    while True:
        client_socket, client_address = server_socket.accept()
        logging.info(f"Accepted connection from {client_address}")
        client_thread = threading.Thread(target=handle_client_peer_wrapper, args=(client_socket,))
        client_thread.start()


def handle_client_peer_wrapper(client_socket):
    try:
        handle_peer(client_socket, status=0)
    except (ConnectionAbortedError, ConnectionResetError) as exp:
        logging.error(f"Connection reset: {exp}")
    finally:
        client_socket.close()


def start_client_peer():
    port = find_free_port()
    if port is None: return
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SI, port))
    try:
        data = client_socket.recv(4096).decode('utf-8')
        print(data)
        while True:
            command = input('[-]')
            client_socket.sendall(command.encode('utf-8'))
            data = client_socket.recv(4096).decode('utf-8')
            print(data)
            if command.lower() == "exit":
                break
    finally:
        client_socket.close()


def handle_peer(client_socket, status):
    if status == 0:
        welcome_message = (
            b"\033[32mWelcome to VCS Console App!\n"
            b"This application allows you to interact with various Version Control Systems (Git, Mercurial, SVN) using a simple console interface.\n"
            b"Choose a Version Control System (VCS):\n"
            b"1. Git\n"
            b"2. Mercurial\n"
            b"3. SVN\n"
            b"4. Exit\n")

    client_socket.sendall(welcome_message)

    while True:
        command = client_socket.recv(1024).decode(encoding).strip()
        if command in ["1", "2", "3"]:
            vcs_type = "Git" if command == "1" else "Mercurial" if command == "2" else "SVN"
            client_socket.sendall(b"\033[31m[*]Enter path to " + vcs_type.encode(encoding) + b" repository: \033[0m")
            version_control = VersionControlFactory.create_version_control_system(connection, vcs_type)
            repo_path = convert_to_absolute_path(client_socket.recv(1024).decode(encoding).strip())
            vcs_facade = VCSFacade(connection)
            process_vcs_commands(client_socket, vcs_facade, version_control, repo_path, vcs_type)
        elif command.lower() == "exit":
            client_socket.sendall(b"[*] Exiting...\n")
            break
        else:
            client_socket.sendall(b"[*] Invalid command. Please enter 'git', 'svn', 'mercurial', or 'exit'.\n")


def process_vcs_commands(client_socket, vcs_facade, version_control, repo_path, vcs_type):
    log_error_handler = ConsoleLogger()
    print_error_handler = Printer()
    while True:
        try:
            client_socket.sendall(f"Selected Version Control System: {vcs_type}\n".encode(encoding) +
                                  f"Current Repository: {repo_path}\n".encode(encoding) +
                                  b"\nChoose an action:\n"
                                  b"1. Commit\n"
                                  b"2. Log\n"
                                  b"3. Show Repositories\n"
                                  b"4. Init\n"
                                  b"5. Visualization\n"
                                  b"6. Push\n"
                                  b"7. Update\n"
                                  b"8. Pull\n"
                                  b"9. Fetch\n"
                                  b"10. List\n"
                                  b"11. Add\n"
                                  b"12. Branch\n"
                                  b"13. Merge\n"
                                  b"14. Tag\n"
                                  b"15. Status\n"
                                  b"16. Back to Main Menu\n")
            action = client_socket.recv(1024).decode(encoding).strip()

            if action == "1":
                client_socket.sendall(b"Enter file name:\n")
                file_name = client_socket.recv(1024).decode(encoding).strip()
                client_socket.sendall(b"Enter commit message:\n")
                message = client_socket.recv(1024).decode(encoding).strip()
                print(vcs_facade.commit_changes(version_control, repo_path, file_name, message))
            elif action == "2":
                commit_log = vcs_facade.watch_history(version_control, repo_path)
                if commit_log:
                    print("Commit log:")
                    if type(commit_log) is str:
                        print(commit_log)
                    else:
                        for commit in commit_log:
                            print(f"Commit ID: {commit['commit_id']}")
                            print(f"Author: {commit['author']} ({commit['email']})")
                            print(f"Message: {commit['message']}")
                            print(f"Timestamp: {commit['timestamp']}")
                            print("-" * 20)
                else:
                    print("No commits found in the repository.")
            elif action == "3":
                print(vcs_facade.show_repositories(version_control))

            elif action == "4":
                result = vcs_facade.initialize_repository(version_control,vcs_type, repo_path)
                print(result)
            elif action == "5":
                vcs_facade.visualization(version_control, repo_path)
            elif action == "6":
                client_socket.sendall(b"Enter remote name:\n")
                remote_name = client_socket.recv(1024).decode(encoding).strip()
                client_socket.sendall(b"Enter branch name:\n")
                branch = client_socket.recv(1024).decode(encoding).strip()
                client_socket.sendall(b"Enter remote url name:\n")
                remote_url = client_socket.recv(1024).decode(encoding).strip()
                print(vcs_facade.push(version_control,repo_path,  remote_name=remote_name, branch_name=branch,remote_url=remote_url))
            elif action == "7":
                client_socket.sendall(b"Enter branch name:\n")
                branch = client_socket.recv(1024).decode(encoding).strip()
                print(vcs_facade.update(version_control, repo_path,branch))
            elif action == "8":
                client_socket.sendall(b"Enter branch name:\n")
                branch = client_socket.recv(1024).decode(encoding).strip()
                print(vcs_facade.pull(version_control, repo_path,branch))
            elif action == "9":
                print(vcs_facade.fetch(version_control, repo_path))
            elif action == "10":
                branches = vcs_facade.list(version_control, repo_path)
                if(branches):
                  print("Branches:")
                  for branch in branches:
                    print(branch)
                else:
                    print('No branches')
            elif action == "11":
                client_socket.sendall(b"Enter file name:\n")
                file_name = client_socket.recv(1024).decode(encoding).strip()
                print(vcs_facade.add(version_control, repo_path, file_name))
            elif action == "12":
                client_socket.sendall(b"Enter branch name:\n")
                branch_name = client_socket.recv(1024).decode(encoding).strip()
                print(vcs_facade.branch(version_control, repo_path,branch_name))

            elif action == "13":
                client_socket.sendall(b"Enter source branch:\n")
                source_branch = client_socket.recv(1024).decode(encoding).strip()
                client_socket.sendall(b"Enter destination branch:\n")
                destination_branch = client_socket.recv(1024).decode(encoding).strip()
                print(vcs_facade.merge(version_control, repo_path,source_branch=source_branch,destination_branch=destination_branch))
            elif action == "14":
                client_socket.sendall(b"Enter tag name:\n")
                tag_name = client_socket.recv(1024).decode(encoding).strip()
                print(vcs_facade.tag(version_control, repo_path,tag_name))
            elif action == "15":
                print(vcs_facade.status(version_control, repo_path))
            elif action == "16":
                handle_peer(client_socket, status=0)
            else:
                client_socket.sendall(b"\033[91m" + b"Invalid choice. Please enter a valid option.\n" + b"\033[0m")
        except socket.error as se:
            log_error_handler.log_error(f"Socket error in process_vcs_commands: {se}")
            print_error_handler.print_error(f"Socket error occurred: {se}")
            break
        except Exception as e:
            log_error_handler.log_error(f"Error in process_vcs_commands: {e}")
            print_error_handler.print_error(f"An error occurred: {e}")
            continue


if __name__ == "__main__":
    try:
        server_thread = threading.Thread(target=start_server_peer)
        server_thread.start()
        client_thread = threading.Thread(target=start_client_peer)
        client_thread.start()
        server_thread.join()
        client_thread.join()

    except Exception as e:
        print(f"An error occurred: {e}")

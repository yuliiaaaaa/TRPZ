import logging
import threading
import socket

from src.AbsolutePathAdapter import convert_to_absolute_path
from src.VCSFacade import VCSFacade
from src.VCSFactory import VersionControlFactory
from src.config import encoding, SI, file_log, server_ports
from DatabaseConnection import connection



def is_port_free(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((SI, port)) != 0
def find_free_port():
    for port in server_ports:
        if is_port_free(port):
            return port
    return None
def start_server_peer():
    logging.basicConfig(filename= file_log, level=logging.INFO)
    free_port = find_free_port()

    if free_port is None: return
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SI, free_port))
    server_socket.listen(1)
    logging.info(f"Server started on port {free_port}. Waiting for connections...")

    while True:
        client_socket, client_address = server_socket.accept()
        logging.info(f"Accepted connection from {client_address}")
        client_thread = threading.Thread(target=handle_client_peer_wrapper,args=(client_socket,))
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
            process_vcs_commands(client_socket, vcs_facade, version_control, repo_path,vcs_type)
        elif command.lower() == "exit":
            client_socket.sendall(b"[*] Exiting...\n")
            break
        else:
            client_socket.sendall(b"[*] Invalid command. Please enter 'git', 'svn', 'mercurial', or 'exit'.\n")

def process_vcs_commands(client_socket, vcs_facade, version_control, repo_path,vcs_type):
    while True:
        client_socket.sendall(f"Selected Version Control System: {vcs_type}\n".encode(encoding)+
                              f"Current Repository: {repo_path}\n".encode(encoding) +

                              b"\nChoose an action:\n"
                              b"1. Commit\n"
                              b"2. Log\n"
                              b"3. Show Repositories\n"
                              b"4. Init\n"
                              b"5. Back to Main Menu\n")
        action = client_socket.recv(1024).decode(encoding).strip()

        if action == "1":
            file_name = client_socket.recv(1024).decode(encoding).strip()
            message = client_socket.recv(1024).decode(encoding).strip()
            vcs_facade.commit_changes(version_control, repo_path, file_name, message)
        elif action == "2":
            vcs_facade.watch_history(version_control, repo_path)
        elif action == "3":
            vcs_facade.show_repositories(version_control)
        elif action == "4":
            vcs_facade.initialize_repository(vcs_type,repo_path)
        elif action == "5":
            handle_peer(client_socket,status=0)
        else:
            client_socket.sendall(b"Invalid choice. Please enter a valid option.\n")

if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server_peer)
    server_thread.start()
    client_thread = threading.Thread(target=start_client_peer)
    client_thread.start()
    server_thread.join()
    client_thread.join()
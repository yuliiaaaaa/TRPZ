import threading

from src.Peer.Peer import start_server_peer, start_client_peer


def main():
    server_thread = threading.Thread(target=start_server_peer)
    server_thread.start()
    client_thread = threading.Thread(target=start_client_peer)
    client_thread.start()
    server_thread.join()
    client_thread.join()

if __name__ == "__main__":
    main()
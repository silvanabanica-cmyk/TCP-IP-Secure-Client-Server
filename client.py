import socket

HOST = "127.0.0.1"
PORT = 5050
BUFFER_SIZE = 1024


def start_client():
    message = input("Enter message to send to server: ").strip()

    if not message:
        print("Message cannot be empty.")
        return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((HOST, PORT))
        client_socket.send(message.encode("utf-8"))

        response = client_socket.recv(BUFFER_SIZE).decode("utf-8")
        print(f"[SERVER RESPONSE] {response}")

    except ConnectionRefusedError:
        print("Connection failed. Make sure the server is running.")

    finally:
        client_socket.close()


if __name__ == "__main__":
    start_client()
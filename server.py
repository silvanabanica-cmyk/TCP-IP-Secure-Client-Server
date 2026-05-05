import socket
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5050
BUFFER_SIZE = 1024
MAX_MESSAGE_LENGTH = 200


def validate_message(message):
    if not message:
        return False, "Message cannot be empty."

    if len(message) > MAX_MESSAGE_LENGTH:
        return False, "Message is too long."

    blocked_patterns = ["<script>", "DROP TABLE", "--", "../"]

    for pattern in blocked_patterns:
        if pattern.lower() in message.lower():
            return False, "Message contains blocked content."

    return True, "Message accepted."


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print(f"[SERVER STARTED] Listening on {HOST}:{PORT}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"[NEW CONNECTION] {client_address} connected.")

            data = client_socket.recv(BUFFER_SIZE).decode("utf-8")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            is_valid, validation_message = validate_message(data)

            if is_valid:
                print(f"[{timestamp}] Valid message received: {data}")
                response = f"Server accepted your message: {data}"
            else:
                print(f"[{timestamp}] Invalid message blocked: {validation_message}")
                response = f"Request rejected: {validation_message}"

            client_socket.send(response.encode("utf-8"))
            client_socket.close()

            print(f"[CONNECTION CLOSED] {client_address}")

    except KeyboardInterrupt:
        print("\n[SERVER STOPPED]")

    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()
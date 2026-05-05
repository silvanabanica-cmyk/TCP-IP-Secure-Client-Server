import socket
from datetime import datetime

HOST = "127.0.0.1"
PORT = 8080
BUFFER_SIZE = 2048

ALLOWED_METHODS = ["GET"]
ALLOWED_PATHS = ["/", "/status"]

AUTH_TOKEN = "my-secure-token"


def build_response(status_code, status_text, body):
    response = (
        f"HTTP/1.1 {status_code} {status_text}\r\n"
        "Content-Type: text/html; charset=UTF-8\r\n"
        f"Content-Length: {len(body.encode('utf-8'))}\r\n"
        "Connection: close\r\n"
        "\r\n"
        f"{body}"
    )
    return response


def validate_http_request(request):
    if not request:
        return False, "400", "Bad Request", "Empty request."

    request_line = request.splitlines()[0]
    parts = request_line.split()

    if len(parts) != 3:
        return False, "400", "Bad Request", "Invalid request line."

    method, path, protocol = parts

    if method not in ALLOWED_METHODS:
        return False, "405", "Method Not Allowed", "Only GET requests are allowed."

    if path not in ALLOWED_PATHS:
        return False, "404", "Not Found", "Path not allowed."

    if not protocol.startswith("HTTP/"):
        return False, "400", "Bad Request", "Invalid HTTP protocol."

    if path == "/status" and f"Authorization: Bearer {AUTH_TOKEN}" not in request:
        return False, "401", "Unauthorized", "Missing or invalid authorization token."

    return True, "200", "OK", "Request accepted."


def start_http_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print(f"[HTTP SERVER STARTED] Listening on http://{HOST}:{PORT}")

        while True:
            client_socket, client_address = server_socket.accept()
            request = client_socket.recv(BUFFER_SIZE).decode("utf-8", errors="replace")

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] HTTP request from {client_address}:")
            print(request)

            is_valid, status_code, status_text, message = validate_http_request(request)

            if is_valid:
                body = f"""
                <html>
                    <head>
                        <title>Secure TCP/IP HTTP Server</title>
                    </head>
                    <body>
                        <h1>Secure HTTP Server Running</h1>
                        <p>{message}</p>
                        <p>This response was sent using Python sockets over TCP/IP.</p>
                    </body>
                </html>
                """
            else:
                body = f"""
                <html>
                    <head>
                        <title>{status_code} {status_text}</title>
                    </head>
                    <body>
                        <h1>{status_code} {status_text}</h1>
                        <p>{message}</p>
                    </body>
                </html>
                """

            response = build_response(status_code, status_text, body)
            client_socket.send(response.encode("utf-8"))
            client_socket.close()

    except KeyboardInterrupt:
        print("\n[HTTP SERVER STOPPED]")

    finally:
        server_socket.close()


if __name__ == "__main__":
    start_http_server()
import socket

HOST = 'localhost'
PORT = 8081
BUFFER_SIZE = 4096

def send_request(method):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    request = f"{method} / HTTP/1.1\r\nHost: {HOST}\r\n\r\n"
    client_socket.sendall(request.encode())

    response = b""
    while True:
        data = client_socket.recv(BUFFER_SIZE)
        if not data:
            break
        response += data

    print("Server Response:\n", response.decode())

    client_socket.close()

if __name__ == '__main__':
    methods = ['GET', 'HEAD', 'POST']
    for method in methods:
        print(f"Sending {method} request to server...")
        send_request(method)
        print()

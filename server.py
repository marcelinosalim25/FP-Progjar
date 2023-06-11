import socket
import select
import threading

# Konfigurasi server
HOST = 'localhost'
PORT = 8081
BUFFER_SIZE = 4096

# Konten respons
HTTP_RESPONSES = {
    200: 'HTTP/1.1 200 OK.',
    301: 'HTTP/1.1 301 Moved Permanently.',
    403: 'HTTP/1.1 403 Forbidden Access Denied.',
    404: 'HTTP/1.1 404 Not Found Page Not Found.',
    500: 'HTTP/1.1 500 Internal Server Error.',
}

# Fungsi untuk menghandle permintaan klien
def handle_client_request(client_socket):
    request_data = client_socket.recv(BUFFER_SIZE).decode()
    method = request_data.split(' ')[0]
    response_code = 200

    if method == 'GET':
        response_code = 200
    elif method == 'HEAD':
        response_code = 200
    elif method == 'POST':
        response_code = 200
        # Lakukan parsing HTML di sini

    response = HTTP_RESPONSES.get(response_code, 'HTTP/1.1 500 Internal Server Error.')
    client_socket.sendall(response.encode())
    client_socket.close()

# Fungsi utama untuk menjalankan server
def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    inputs = [server_socket]
    outputs = []
    lock = threading.Lock()

    while True:
        readable, writable, exceptional = select.select(inputs, outputs, inputs)

        for sock in readable:
            if sock is server_socket:
                client_socket, client_address = server_socket.accept()
                inputs.append(client_socket)
                t = threading.Thread(target=handle_client_request, args=(client_socket,))
                t.start()
            else:
                data = sock.recv(BUFFER_SIZE)
                if data:
                    # Tangani permintaan klien di thread terpisah
                    t = threading.Thread(target=handle_client_request, args=(sock,))
                    t.start()
                else:
                    sock.close()
                    inputs.remove(sock)

        for sock in exceptional:
            if sock in inputs:
                inputs.remove(sock)
            if sock in outputs:
                outputs.remove(sock)
            sock.close()

if __name__ == '__main__':
    run_server()

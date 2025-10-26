# File: pybluez_server.py
import bluetooth

# Create a Bluetooth socket using the RFCOMM protocol
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY)) # Bind to any available port
server_sock.listen(1) # Listen for one incoming connection

# Get the port number that the OS assigned to our socket
port = server_sock.getsockname()[1]

# A unique UUID is needed for the service discovery protocol (SDP)
# You can generate one online, e.g., at https://www.uuidgenerator.net/
# This is NOT a BLE UUID.
UUID = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

# Advertise the service
bluetooth.advertise_service(server_sock, "ChatServer",
                            service_id=UUID,
                            service_classes=[UUID, bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE],
                            )

print(f"Waiting for connection on RFCOMM channel {port}...")

try:
    # This is a blocking call that waits for a client to connect
    client_sock, client_info = server_sock.accept()
    print(f"Accepted connection from {client_info}")

    while True:
        # Receive data from the client (up to 1024 bytes)
        data = client_sock.recv(1024)
        if not data:
            break # Connection closed by client
        
        message = data.decode('utf-8')
        print(f"Client said: {message}")

        # Get a response from the server's user
        response = input("Server says: ")
        client_sock.send(response.encode('utf-8'))

except IOError:
    print("Connection error occurred.")
except KeyboardInterrupt:
    print("\nServer shutting down.")
finally:
    print("Closing sockets.")
    if 'client_sock' in locals():
        client_sock.close()
    server_sock.close()
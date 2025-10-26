# File: pybluez_client.py
import bluetooth
import sys

# --- IMPORTANT ---
# PASTE THE SERVER'S BLUETOOTH ADDRESS HERE
SERVER_ADDRESS = "XX:XX:XX:XX:XX:XX" # e.g., "00:1A:7D:DA:71:13"
# -----------------

if SERVER_ADDRESS == "XX:XX:XX:XX:XX:XX":
    print("Error: Please replace 'XX:XX:XX:XX:XX:XX' with the server's Bluetooth address.")
    sys.exit(1)

# The same UUID used by the server
UUID = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

print(f"Searching for ChatServer service on {SERVER_ADDRESS}...")

# Find the service running on the server
service_matches = bluetooth.find_service(uuid=UUID, address=SERVER_ADDRESS)

if len(service_matches) == 0:
    print("Couldn't find the ChatServer service.")
    sys.exit(0)

first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

print(f"Connecting to '{name}' on host {host} (channel {port})...")

# Create the client socket
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((host, port))
print("Connected successfully!")

try:
    while True:
        message = input("Client says: ")
        if not message:
            break

        sock.send(message.encode('utf-8'))
        
        # Wait for the server's response
        data = sock.recv(1024)
        print(f"Server said: {data.decode('utf-8')}")

except IOError:
    print("Connection error.")
except KeyboardInterrupt:
    print("\nDisconnecting.")
finally:
    sock.close()
    print("Socket closed.")
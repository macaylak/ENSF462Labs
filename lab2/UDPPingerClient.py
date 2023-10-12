import socket
import time

# Server address and port
server_address = ('localhost', 12000)

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Constants
NUM_PINGS = 10
TIMEOUT = 1.0  # 1 second timeout for waiting for a response

# Initialize variables for RTT calculation
min_rtt = float('inf')
max_rtt = 0
total_rtt = 0
packets_lost = 0

for sequence_number in range(1, NUM_PINGS + 1):
    # Prepare the ping message with the correct format
    ping_message = f'Ping {sequence_number} {time.time()}'

    # Send the ping message to the server
    client_socket.sendto(ping_message.encode(), server_address)

    # Set a timeout for receiving a response
    client_socket.settimeout(TIMEOUT)

    try:
        start_time = time.time()
        # Receive the response from the server
        response, server_address = client_socket.recvfrom(1024)
        end_time = time.time()

        # Calculate the round-trip time (RTT) in seconds
        rtt = end_time - start_time

        # Update min_rtt, max_rtt, and total_rtt
        min_rtt = min(min_rtt, rtt)
        max_rtt = max(max_rtt, rtt)
        total_rtt += rtt

        # Print the response message and RTT
        print(f'Response from {server_address}: {response.decode()} | RTT: {rtt:.6f} seconds')

    except socket.timeout:
        # Packet is lost (no response within the timeout)
        packets_lost += 1
        print(f'Request timed out')

    # Add a 1-second delay before sending the next ping
    time.sleep(1)

# Calculate the average RTT
avg_rtt = total_rtt / NUM_PINGS

# Calculate the packet loss rate in percentage
packet_loss_rate = (packets_lost / NUM_PINGS) * 100

# Print the summary
print('\nPing statistics:')
print(f'Minimum RTT: {min_rtt:.6f} seconds')
print(f'Maximum RTT: {max_rtt:.6f} seconds')
print(f'Average RTT: {avg_rtt:.6f} seconds')
print(f'Packet loss rate: {packet_loss_rate:.2f}%')

# Close the socket
client_socket.close()

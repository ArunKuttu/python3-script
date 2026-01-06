import os
from datetime import datetime
#Script Author : Arun.k
#Date : 03-07-2024
# Path to the OpenVPN status log file
log_path = '/etc/openvpn/server/openvpn-status.log'

# Function to parse the log file and extract information
def parse_openvpn_status_log(log_file):
    # Initialize variables to store extracted information
    clients = []

    # Open the log file for reading
    with open(log_file, 'r') as f:
        # Read the lines from the log file
        lines = f.readlines()

        # Iterate over each line in the log file
        for line in lines:
            # Check if the line starts with 'CLIENT_LIST'
            if line.startswith('CLIENT_LIST'):
                # Split the line by commas to extract fields
                fields = line.split(',')

                # Extract required fields
                common_name = fields[1]
                real_address = fields[2].split(':')[0]  # Extracting Public IP
                virtual_address = fields[3]  # Tunnel IP
                connected_since_str = fields[7].strip()  # Connected Since as string
                username = fields[9]  # Username
                connected = "Currently connected" if int(fields[11]) > 0 else "Not connected"
                
                # Convert connected_since_str to a datetime object
                connected_since = datetime.strptime(connected_since_str, '%a %b %d %H:%M:%S %Y')

                # Convert datetime object to a Unix timestamp
                connected_since_ts = int(connected_since.timestamp())

                # Create a dictionary with the extracted information
                client_info = {
                    'Common Name': common_name,
                    'Public IP': real_address,
                    'Tunnel IP': virtual_address,
                    'Connected Since': connected_since.strftime('%Y-%m-%d %H:%M:%S'),
                    'Username': username,
                    'Connection Status': connected
                }

                # Append the client information to the list
                clients.append(client_info)

    return clients

# Main script to call the function and print the results
if __name__ == "__main__":
    # Check if the log file exists
    if os.path.exists(log_path):
        # Parse the OpenVPN status log
        client_list = parse_openvpn_status_log(log_path)

        # Print the extracted information for each client
        for idx, client in enumerate(client_list, start=1):
            print(f"Client {idx}:")
            for key, value in client.items():
                print(f"{key}: {value}")
            print()
    else:
        print(f"Error: Log file '{log_path}' not found.")

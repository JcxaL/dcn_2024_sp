import socket
import json

UDP_IP = "0.0.0.0"
UDP_PORT = 53533
dns_records_file = "dns_records.json"

# STEP [2]
def dns_registration(data):
    try:
        parts = data.split()
        record = {
            'TYPE': parts[0],
            'NAME': parts[1],
            'VALUE': parts[2],
            'TTL': parts[3]
        }
        with open(dns_records_file, 'r+') as file:
            try:
                records = json.load(file)
            except json.JSONDecodeError:
                records = {}

            records[record['NAME']] = record
            file.seek(0)
            json.dump(records, file, indent=4)

        # STEP [3]
        return "Registration successful"

    except Exception as e:
        return f"Error during registration: {str(e)}"

# STEP [6]
def handle_query(data):
    try:
        with open(dns_records_file, 'r') as file:
            records = json.load(file)

        # Parse the query
        parts = data.split()
        query_name = parts[1]
        if query_name in records:
            record = records[query_name]
            return f"{record['TYPE']} {record['NAME']} {record['VALUE']} {record['TTL']}"
        else:
            return "Record not found"

    except Exception as e:
        return f"Error during query: {str(e)}"


def start_udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    sock.bind((UDP_IP, UDP_PORT))
    print(f"UDP server listening on {UDP_IP}:{UDP_PORT}")

    while True:
        data, addr = sock.recvfrom(1024) 
        data = data.decode('utf-8')
        print(f"received message: {data} from {addr}")

        if data.startswith('TYPE=A'):
            response = dns_registration(data)
        else:
            response = handle_query(data)
        
        sock.sendto(response.encode(), addr)


if __name__ == '__main__':
    # Initialize the file if !exist
    try:
        with open(dns_records_file, 'r+') as file:
            json.load(file) 
    except (FileNotFoundError, json.JSONDecodeError):
        with open(dns_records_file, 'w') as file:
            file.write('{}') 

    start_udp_server()

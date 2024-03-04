from flask import Flask, request, jsonify
import requests
import socket
import json

app = Flask(__name__)

def dns_query(as_ip, as_port, hostname):
    message = f'TYPE=A NAME={hostname}'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (as_ip, int(as_port)))
    data, _ = sock.recvfrom(512) 
    response = data.decode()
    
    # Lab format "TYPE=A NAME=fibonacci.com VALUE=IP_ADDRESS TTL=10"
    response_parts = response.split()
    ip_address = response_parts[4] 

    return ip_address


@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')
    
    if not all([hostname, fs_port, number, as_ip, as_port]):
        return jsonify({'error': 'Missing parameters'}), 400
    
    # STEP [5]
    fs_ip = dns_query(as_ip, as_port, hostname)
    
    # STEP [7]
    fs_response = requests.get(f'http://{fs_ip}:{fs_port}/fibonacci', params={'number': number})
    
    # STEP [9]
    if fs_response.status_code == 200:
        return jsonify({'result': fs_response.json()}), 200
    else:
        return jsonify({'error': 'Failed to get Fibonacci number'}), fs_response.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

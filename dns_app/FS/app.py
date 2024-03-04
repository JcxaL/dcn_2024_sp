from flask import Flask, request, jsonify
import socket
import json

app = Flask(__name__)


FS_IP = "172.18.0.2"  
AS_IP = "10.9.10.2" 
AS_PORT = 53533


# STEP [1]
def register_with_as(hostname, fs_ip, as_ip, as_port):
    message = f"TYPE=A NAME={hostname} VALUE={fs_ip} TTL=10"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (as_ip, as_port)
    try:
        sock.sendto(message.encode(), server_address)
    finally:
        sock.close()

@app.route('/register', methods=['PUT'])
def register():
    data = request.get_json()

    hostname = data.get('hostname')
    fs_ip = data.get('ip') 
    as_ip = data.get('as_ip')
    as_port = int(data.get('as_port'))

    register_with_as(hostname, fs_ip, as_ip, as_port)

    return jsonify({"message": "Registration successful"}), 201

# Server main function
def fibonacci(n):
    if n in {0, 1}: return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# STEP [8]
@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    number = request.args.get('number', type=int)
    if number is None or number < 0:
        return jsonify({'error': 'Invalid number'}), 400
    result = fibonacci(number)
    
    return jsonify({'result': result}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)

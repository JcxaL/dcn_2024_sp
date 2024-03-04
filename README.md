# Lab 3 DNS Application Project

## Overview
User Server (US): A simple Flask web server that accepts requests to calculate Fibonacci numbers. It queries the AS to resolve the FS's hostname to an IP address, then forwards the calculation request to the FS.
Fibonacci Server (FS): Also a Flask web server, it calculates Fibonacci numbers for a given sequence number that registers its hostname and IP address with the AS on startup.
Authoritative Server (AS): A simple UDP server handling DNS record registration and queries, pairs hostnames to IP addresses and responds to DNS queries from the US.

## Project Structure
```
dns_app/
│
├── AS/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt (if necessary)
│
├── FS/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
└── US/
    ├── app.py
    ├── Dockerfile
    └── requirements.txt
```

## Setup
Build the Docker images for the AS, FS, and US servers. Then, run the containers in the following order: AS, FS, and US.
```
# Authoritative Server
cd AS
docker build -t authoritative-server .

# Fibonacci Server
cd ../FS
docker build -t fibonacci-server .

# User Server
cd ../US
docker build -t user-server .

```

## Running the Lab 3
```
# Authoritative Server
docker run -d --name as -p 53533:53533/udp authoritative-server

# Fibonacci Server
docker run -d --name fs -p 9090:9090 fibonacci-server

# User Server
docker run -d --name us -p 8080:8080 user-server
```

## The Test I Used
```
curl "http://localhost:8080/fibonacci?hostname=fibonacci.com&fs_port=9090&number=10&as_ip=localhost&as_port=53533"
```


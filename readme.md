Server : python flypeng.py -s -p port
Client : python flyoeng.py -r ip -p port
The python version >= 3.6
Since no Certificate Authority is used, you should confirm with the server that the sha256 of the public key is correct. Once the connection is established, the software will save the hash of the public key locally, and it will be automatically verified during subsequent connections.
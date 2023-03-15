#FlyPeng
FlyPeng is a Python-based tool for secure communication between a client and a server without using a Certificate Authority. It uses RSA encryption to secure the communication and requires Python version 3.6 or above.

##Usage
To start the server, run the following command:

```python
python flypeng.py -s -p [port]
```
To connect to the server as a client, run the following command:

```python
python flyoeng.py -r [ip] -p [port]
```
Make sure to confirm with the server that the sha256 of the public key is correct, as no Certificate Authority is used. Once the connection is established, the software will save the hash of the public key locally, and it will be automatically verified during subsequent connections.

##License
This project is licensed under the MIT License. See the LICENSE file for details.

##Acknowledgements
FlyPeng is based on the RSA encryption algorithm and uses the pycryptodome library for cryptography. Thank you to the developers of these tools for their contributions to the open-source community.

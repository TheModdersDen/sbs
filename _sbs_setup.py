import os
import os.path
from time import sleep
from elevate import elevate
import platform
import urllib.request
import datetime
import logging
import subprocess


class SBS_Setup():

    def is_root():
        return os.getuid() == 0

    def __init__(self):
        self.logger = self.getLogger()
        self.logger.info('Starting up...')
        print("Starting up...\n")
        self.dt = datetime.date.today()
        self.now = datetime.datetime.now()
        self.current_time = self.now.strftime("%H:%M:%S")
        self.currentDate = self.dt.isoformat()
        self.logger.info(
            f"The current date and time is: '{self.currentDate}--{self.current_time}.'")
        print(
            f"The current date and time is: '{self.currentDate}--{self.current_time}.'\n")

    def main(self):
        if self.getCurrentOS() == 0:
            self.logger.debug(
                "Yay! You ran this program correctly, thus far.\nPrepare for unforseen consequences.")
            print("Yay! You ran this program correctly, thus far.")
        elif self.getCurrentOS() == 1:
            self._finish_and_exit_neatly(
                "Your OS, Windows, is currently not supported. Exiting gracefully..."
            )

        elif self.getCurrentOS() == 2:
            self._finish_and_exit_neatly(
                "Your OS, Darwin (AKA: macOS or Mac OS X), is currently not supported. Exiting gracefully..."
            )
        self.elevate_user()
        self.install_pip(self.getCurrentOS())
        self.install_dependencies(self.getCurrentOS())

    def elevate_user(self):
        if self.is_root == False:
            if self.getCurrentOS() == 0:  # If the user is on Linux and not running as 'root'.
                self.logger.info(
                    "User is not currently running the program as root. Requesting root privledges... NOW.")
                print(
                    "User is not currently running the program as root. Requesting root privledges... NOW.\n")
                elevate()
            # If the user is on Windows and not running as 'Administrator'.
            elif self.getCurrentOS() == 1:
                self.logger.info(
                    "User is not currently running the program as 'Administrator'. Requesting admin privledges... NOW.")
                print(
                    "User is not currently running the program as 'Administrator'. Requesting admin privledges... NOW.\n")
                elevate()
            elif self.getCurrentOS() == 2:  # If the user is on Darwin/macOS.
                self._finish_and_exit_neatly(
                    "Your OS, Darwin (AKA: macOS or Mac OS X), is currently not supported. Exiting gracefully...\n")

    def install_pip(self, os_type):
        if os_type == 0:
            command = "pip --version"
            process = subprocess.Popen(
                command, shell=True, stdout=subprocess.PIPE)
            process.wait()
            answer = self.yes_no(
                "Does this program have your permission to install Python3's pip module? (Y/N): ")
            if process.returncode != 0 and answer == True:
                command = "sudo apt install -y python3-pip"
                process = subprocess.Popen(
                    command, shell=True, stdout=subprocess.PIPE)
                process.wait()
                if process.returncode != 0:
                        print(
                            f"An error occured while running command '{command}'.\n The error code is: '{process.returncode}'.")
        elif os_type == 1:
            try:
                command = "pip --version"
                process = subprocess.Popen(
                    command, shell=True, stdout=subprocess.PIPE)
                process.wait()
                answer = self.yes_no(
                    "Does this program have your permission to install Python3.8.10 using Microsoft WinGet? (Y/N): ")
                if process.returncode != 0 and answer == True:
                    command = "winget install --id Python.Python.3 --version 3.8.10150.0"
                    process = subprocess.Popen(
                        command, shell=True, stdout=subprocess.PIPE)
                    process.wait()
                    if process.returncode != 0:
                        print(
                            f"An error occured while running command '{command}'.\n The error code is: '{process.returncode}'.")
            except Exception as error:
                self.logger.fatal(
                    f"There was a fatal error that occured. Here is the stack trace:\n{error}")
                self._finish_and_exit_neatly(
                    "Uh oh, Daisy Oh!\nPlease check the 'sbs-setup.log'. A fatal error occured...")
        else:
            self.logger.error("Uh... Houston, we have a problem.")
            print(
                "Uh... Houston, we have a problem.\nThis program will likely crash in the near future.")

    def install_dependencies(self, os_type):
        if os_type == 0:
            command = "sudo apt install -y libhunspell-dev"
            process = subprocess.Popen(
                command, shell=True, stdout=subprocess.PIPE)
            process.wait()
            if process.returncode != 0:
                print(f"An error occured while running command '{command}'.\n The error code is: '{process.returncode}'.")
            command = "sudo pip install -r " + os.getcwd() + os.path.sep + "requirements_linux.txt"
            process = subprocess.Popen(
                command, shell=True, stdout=subprocess.PIPE)
            process.wait()
            if process.returncode != 0:
                print(f"An error occured while running command '{command}'.\n The error code is: '{process.returncode}'.")
        elif os_type == 1:
            command = "pip install -r " + os.getcwd() + os.path.sep +"requirements_windows.txt"
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            process.wait()
            if process.returncode != 0:
                print(f"An error occured while running command '{command}'.\n The error code is: '{process.returncode}'.")
    
    def yes_no(self, input_question):
        prompt = str(input(input_question))
        
        if prompt in ["Y".lower(), "YES".lower()]:
            return True
        elif prompt in ["N".lower(), "NO".lower()]:
            return False
        else:
            self.yes_no(input_question)

    def _finish_and_exit_neatly(self, message):
        self.logger.error(message)
        print(message)
        sleep(5)
        exit(1)
        
    def getCurrentOS(self):
        if platform.system() == "Linux":
            return 0  # Linux
        elif platform.system() == "Windows":
            return 1  # Windows
        elif platform.system() == "Darwin":
            return 2  # macOS/Mac OS X
    
    def getLogger(self):
        logging.basicConfig(filename="sbs-setup.log",
                            format='%(asctime)s %(message)s',
                            filemode='w')
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        
        return logger

if __name__ == "__main__":
    sbs_setup = SBS_Setup()
    sbs_setup.main()
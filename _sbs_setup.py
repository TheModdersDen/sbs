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
        if (
            self.getCurrentOS() == 0
            or self.getCurrentOS() != 0
            and self.getCurrentOS() == 1
        ):
            self.logger.debug(
                "Yay! You ran this program correctly, thus far.")
            print("Yay! You ran this program correctly, thus far.")
            self.elevate_user()
            self.install_pip(self.getCurrentOS())
            self.install_dependencies(self.getCurrentOS())
        elif (
            self.getCurrentOS() != 0
            and self.getCurrentOS() != 1
            and self.getCurrentOS() == 2
        ):
            self._finish_and_exit_neatly(
                "Your OS, Darwin (AKA: macOS or Mac OS X), is currently not supported. Exiting gracefully..."
            )

    def elevate_user(self):  # sourcery skip: extract-duplicate-method
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
        # sourcery skip: extract-duplicate-method, extract-method, swap-if-else-branches
        if os_type == 0:
            try:
                command = "pip3 --version"
                process = subprocess.Popen(
                    command, shell=True, stdout=subprocess.PIPE)
                process.wait()
                if process.returncode != 0:
                    print("Python's PIP is not installed. Installing...")
                    self.logger.debug("Python's PIP is not installed. Installing...")
                    command = "sudo apt install -y python3-pip"
                    process = subprocess.Popen(
                        command, shell=True)
                    process.wait()
                    if process.returncode != 0:
                        print(
                            f"An error occured while running command '{command}'.\n The error code is: '{process.returncode}'.")
                    else:
                        print(f"Completed installation of Python with code '{process.returncode}'.")
                        self.logger.debug(f"Completed installation of Python with code '{process.returncode}'.")
                else:
                    print(f"Completed installation of Python with code '{process.returncode}'.")
                    self.logger.debug(f"Completed installation of Python with code '{process.returncode}'.")
            except Exception as error:
                self.logger.error("Uh... Houston, we have a problem.")
                print(
                "Uh... Houston, we have a problem.\nThis program will likely crash in the near future.")
        elif os_type == 1:
            try:
                command = "pip3 --version"
                process = subprocess.Popen(
                    command, shell=True, stdout=subprocess.PIPE)
                process.wait()
                if process.returncode != 0:
                    print("Python's PIP is not installed. Installing...")
                    self.logger.debug("Python's PIP is not installed. Installing...")
                    command = "winget install --id Python.Python.3 --version 3.8.10150.0"
                    process = subprocess.Popen(
                        command, shell=True)
                    process.wait()
                    if process.returncode != 0:
                        print(
                            f"An error occured while running command '{command}'.\n The error code is: '{process.returncode}'.")
                    else:
                        print(f"Completed installation of Python with code '{process.returncode}'.")
                        self.logger.debug(f"Completed installation of Python with code '{process.returncode}'.")      
                else:
                    print(f"Completed installation of Python 3 PIP with code '{process.returncode}'.")
                    self.logger.debug(f"Completed installation of Python 3 PIP with code '{process.returncode}'.")
            except Exception as error:
                self.logger.fatal(
                    f'There was a fatal error that occured. Here is the stack trace:\n{error}'
                )

                self._finish_and_exit_neatly(
                    "Uh oh, Daisy Oh!\nPlease check the 'sbs-setup.log'. A fatal error occured..."
                )

        else:
            self.logger.error("Uh... Houston, we have a problem.")
            print(
                "Uh... Houston, we have a problem.\nThis program will likely crash in the near future.")

    def install_dependencies(self, os_type):
        if os_type == 0:
            if self.is_root == False:
                return # Cancel out as all below code for Linux needs to have the 'sudo' command added to this python file when executed.
            command = "sudo apt install -y libhunspell-dev"
            exec = os.system(command)
            if exec != 0:
                print(f"An error occured while running command '{command}'.\n The error code is: '{exec}'.")
            command = "sudo pip install -r " + os.getcwd() + os.path.sep + "requirements_linux.txt"
            exec = os.system(command)
            if exec != 0:
                print(f"An error occured while running command '{command}'.\n The error code is: '{exec}'.")
            command = "sudo spacy download en_core_web_sm"
            exec = os.system(command)
            if exec != 0:
                print(f"An error occured while running command '{command}'.\n The error code is: '{exec}'.")
        elif os_type == 1:
            command = "pip install -r " + os.getcwd() + os.path.sep +"requirements_windows.txt"
            exec = os.system(command)
            if exec != 0:
                print(f"An error occured while running command '{command}'.\n The error code is: '{exec}'.")
    
    def yes_no(self, input_question):
        prompt = str(input(input_question))
        
        if prompt.lower() in ["Y".lower(), "YES".lower()]:
            return True
        elif prompt.lower() in ["N".lower(), "NO".lower()]:
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
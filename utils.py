import logging
import os
import csv
import platform

class Utils():

    logger = None
    
    # If on Linux, get the distribution name.
    def get_distro_name(self):  # sourcery skip: class-extract-method

        RELEASE_DATA = {}

        with open("/etc/os-release") as f:
            reader = csv.reader(f, delimiter="=")
            for row in reader:
                if row:
                    RELEASE_DATA[row[0]] = row[1]

        if RELEASE_DATA["ID"] in ["debian", "raspbian"]:
            with open("/etc/debian_version") as f:
                DEBIAN_VERSION = f.readline().strip()
            major_version = DEBIAN_VERSION.split(".")[0]
            version_split = RELEASE_DATA["VERSION"].split(" ", maxsplit=1)
            if version_split[0] == major_version:
                # Just major version shown, replace it with the full version
                RELEASE_DATA["VERSION"] = " ".join([DEBIAN_VERSION] + version_split[1:])

        return "{}".format(RELEASE_DATA["NAME"])
    
    # If on Linux, get the distribution version.
    def get_distro_version(self):

        RELEASE_DATA = {}

        with open("/etc/os-release") as f:
            reader = csv.reader(f, delimiter="=")
            for row in reader:
                if row:
                    RELEASE_DATA[row[0]] = row[1]

        if RELEASE_DATA["ID"] in ["debian", "raspbian"]:
            with open("/etc/debian_version") as f:
                DEBIAN_VERSION = f.readline().strip()
            major_version = DEBIAN_VERSION.split(".")[0]
            version_split = RELEASE_DATA["VERSION"].split(" ", maxsplit=1)
            if version_split[0] == major_version:
                # Just major version shown, replace it with the full version
                RELEASE_DATA["VERSION"] = " ".join([DEBIAN_VERSION] + version_split[1:])

        return "{}".format(RELEASE_DATA["VERSION"])
    
    # Create a file from a filepath, if it doesn't exist.
    def create_file_from_path(self, file_path):
        if not os.path.exists(os.path.dirname(file_path)):
            try:
                os.makedirs(os.path.dirname(file_path))
            except (OSError, Exception) as exc:
                self.utils.LOG_ERROR(f'{exc}')
                print(f'ERROR: {exc}')

    # Get the SBS logger.
    def getLogger(self):
        logging.basicConfig(filename=os.getcwd() + os.path.sep + "sbs.log",
                            format='%(asctime)s %(message)s',
                            filemode='w')
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        return logger

    # Initalize all the local variables.
    def __init__(self):
        self.logger = self.getLogger()
        self.distro = self.get_distro_name()
        self.distro_version = self.get_distro_version()
        self.windows_version = platform.version()

    # Check to see if a file is empty.
    def is_file_empty(self, file_path):
        """ Check if file is empty by confirming if its size is 0 bytes"""
        # Check if file exist and it is empty
        return bool(os.path.exists(file_path) and os.stat(file_path).st_size == 0)

    # Get the file size of a file at a certain path (for the RSS feed).
    def get_file_size(self, file_name):
        statinfo = os.stat(file_name)
        return statinfo.st_size

    # Log a DEBUG message.
    def LOG_DEBUG(self, MSG):
        self.logger.debug(f"DEBUG: {MSG}")
        print(f"DEBUG: {MSG}")

    # Log a WARNING message.
    def LOG_WARN(self, MSG):
        self.logger.warn(f"WARN: {MSG}")
        print(f"WARN: {MSG}")

    # Log an INFORMATION message.
    def LOG_INFO(self, MSG):
        self.logger.info(f"INFO: {MSG}")
        print(f"INFO: {MSG}")

    # Log an ERROR message
    def LOG_ERROR(self, MSG):
        self.logger.error(f"ERROR: {MSG}")
        print(f"ERROR: {MSG}")

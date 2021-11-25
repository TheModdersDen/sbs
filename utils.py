import logging
import os
from getpass import getpass

class Utils():

    logger = None
    
    def create_file_from_path(self, file_path):
        if not os.path.exists(os.path.dirname(file_path)):
            try:
                os.makedirs(os.path.dirname(file_path))
            except (OSError, Exception, PermissionError) as exc:
                self.utils.LOG_ERROR(f"{exc}")
                print(f"ERROR: {exc}")

    def getLogger(self):
        logging.basicConfig(filename="sbs.log",
                            format='%(asctime)s %(message)s',
                            filemode='w')
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        return logger

    def __init__(self):
        self.logger = self.getLogger()

    def is_file_empty(self, file_path):
        """ Check if file is empty by confirming if its size is 0 bytes"""
        # Check if file exist and it is empty
        if os.path.exists(file_path) and os.stat(file_path).st_size == 0:
            return True
        else:
            return False

    def get_file_size(self, file_name):
        statinfo = os.stat(file_name)
        return statinfo.st_size

    def LOG_DEBUG(self, MSG):
        self.logger.debug(f"DEBUG: {MSG}")
        print(f"DEBUG: {MSG}")

    def LOG_WARN(self, MSG):
        self.logger.warn(f"WARN: {MSG}")
        print(f"WARN: {MSG}")

    def LOG_INFO(self, MSG):
        self.logger.info(f"INFO: {MSG}")
        print(f"INFO: {MSG}")

    def LOG_ERROR(self, MSG):
        self.logger.error(f"ERROR: {MSG}")
        print(f"ERROR: {MSG}")

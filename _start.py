# Copyright (c) Bryan Hunter 2022

import os
from rich import print
import logging
from rich.logging import RichHandler
from rich.progress import track
from time import sleep
from rich.console import Console
import argparse

from sbs_old import SBS
from sbs_vars import SBS_vars

class SBS_Start():

    log = None
    FORMAT = None
    console = None

    def __init__(self):
        self.FORMAT = "%(asctime)s %(message)s"
        self.console = Console()
        self.vars = SBS_vars()

        logging.basicConfig(
            filename=os.getcwd() + os.path.sep + "sbs_latest.log", level="NOTSET", format=self.FORMAT, datefmt="[%X]", handlers=[RichHandler()], filemode="w"
        )
        self.log = logging.getLogger("sbs_skill")
        self.process_args()
        self.start_sbs_skill(self)
    
    def process_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
        parser.add_argument("-d", "--daily", help="Generate a feed based on the last day's Shower Thoughts", action="store_true")
        parser.add_argument("-h", "--hourly", help="Generate a feed based on the last hour's Shower Thoughts", action="store_true")
        parser.add_argument("-w", "--weekly", help="Generate a feed based on the last week's Shower Thoughts", action="store_true")
        args = parser.parse_ars()
        
        # Set the verbosity level
        if args.verbose:
            self.log.setLevel(logging.DEBUG)
            self.log.debug("Debugging mode enabled.")
        else:
            self.log.setLevel(logging.INFO)
        
        # Check for the daily, hourly, and weekly arguments.
        if args.daily:
            self.vars.update_frequency = "day"
        elif args.hourly:
            self.vars.update_frequency = "hour"
        elif args.weekly:
            self.vars.update_frequency = "week"
        else:
            self.log.warn("No update frequency specified. Defaulting to 'day'.")
            self.vars.update_frequency = "day"
      
    def start_sbs_skill(self):
        
        sbs = SBS()
        sbs.main()

if __name__ == "__main__":
    start = SBS_Start()
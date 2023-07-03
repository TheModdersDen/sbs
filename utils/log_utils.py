"""
 Copyright (c) 2023 Bryan Hunter (TheModdersDen) | https://github.com/TheModdersDen

 Permission is hereby granted, free of charge, to any person obtaining a copy of
 this software and associated documentation files (the "Software"), to deal in
 the Software without restriction, including without limitation the rights to
 use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 the Software, and to permit persons to whom the Software is furnished to do so,
 subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 """

# A class to handle the logging for the ShowerThoughts Briefing Skill

#! Copyright (c) 2023 Bryan Hunter (TheModdersDen)

import logging
from logging import FileHandler, Logger, getLogger
from os import getcwd, pathsep
from os.path import join

import rich
from rich.console import Console
from rich.logging import RichHandler


class LogUtils():

    loggerName = "sbs_skill"

    logLevel = "DEBUG"

    loggerPath = join(getcwd() + f"{pathsep}logs{pathsep}sbs_latest.log")

    sbsLogger = logging.getLogger(loggerName)

    def get_sbs_logger(self, name: str = "sbs_logger", log_level: str = "INFO") -> Logger:

        self.sbsLogger.addHandler(RichHandler(console=Console(
        ), show_time=True, show_level=True, show_path=True, markup=True))
        self.sbsLogger.addHandler(FileHandler(
            filename=getcwd() + f"{pathsep}logs{pathsep}sbs_latest.log", mode='a', encoding="utf8", delay=False))

        if log_level.upper() == "DEBUG":
            self.sbsLogger.setLevel(logging.DEBUG)
        elif log_level.upper() == "INFO":
            self.sbsLogger.setLevel(logging.INFO)
        elif log_level.upper() == "WARNING":
            self.sbsLogger.setLevel(logging.WARNING)
        elif log_level.upper() == "ERROR":
            self.sbsLogger.setLevel(logging.ERROR)
        elif log_level.upper() == "CRITICAL":
            self.sbsLogger.setLevel(logging.CRITICAL)
        else:
            self.sbsLogger.setLevel(logging.INFO)

        self.log_msg(f'Logger initialized: {self.sbsLogger}')

        return self.sbsLogger

    def log_msg(self, msg: str, log_level: str = "INFO") -> None:

        console = Console()
        if log_level.upper() == "DEBUG":
            console.print(msg, style="bold blue")
            self.sbsLogger.debug(msg)
        elif log_level.upper() == "INFO":
            console.print(msg, style="bold green")
            self.sbsLogger.info(msg)
        elif log_level.upper() == "WARNING":
            console.print(msg, style="bold yellow")
            self.sbsLogger.warning(msg)
        elif log_level.upper() == "ERROR":
            console.print(msg, style="bold red")
            self.sbsLogger.error(msg)
        elif log_level.upper() == "CRITICAL":
            console.print(msg, style="bold red")
            self.sbsLogger.critical(msg)
        else:
            console.print(msg, style="bold green")
            self.sbsLogger.info(msg)

    def __main__(self):
        self.sbsLogger = self.get_sbs_logger("sbs_skill", "INFO")
        self.sbsLogger.info("LogUtils initialized")

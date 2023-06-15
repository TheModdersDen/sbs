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

from datetime import datetime, timedelta
from os import getpid
from time import gmtime, sleep, strftime, time

from elevate import elevate
from psutil import Process

#! Process related utilities
from sbs import SBS


class ProcUtils():

    def __main__(self):
        self.sbs = SBS()
        self.logger = self.sbs.logger

        self.logger.debug('Proc Utils initializing...')

    # Get the current process ID
    def get_process_id(self) -> int:
        try:
            self.logger.debug('Getting process ID...')
            pid = getpid()
            self.logger.debug(f'Got process ID: {pid}')
            return pid
        except Exception as e:
            self.logger.error(f'Error getting process ID: {e}')
            return None

    # Get the current process
    def get_current_process(self) -> Process:
        try:
            self.logger.debug('Getting current process...')
            pid = self.get_process_id()
            p = Process(pid)
            self.logger.debug(f'Got current process: {p}')
            return p
        except Exception as e:
            self.logger.error(f'Error getting current process: {e}')
            return None

    # Get the current process CPU usage
    def get_process_cpu_usage(self) -> float:
        try:
            self.logger.debug('Getting process CPU usage...')
            p = self.get_current_process()
            cpu_usage = p.cpu_percent(interval=1)
            self.logger.debug(f'Got process CPU usage: {cpu_usage}')
            return cpu_usage
        except Exception as e:
            self.logger.error(f'Error getting process CPU usage: {e}')
            return None

    # Get the current process memory usage
    def get_process_memory_usage(self) -> float:
        try:
            self.logger.debug('Getting process memory usage...')
            p = self.get_current_process()
            mem_usage = p.memory_percent()
            self.logger.debug(f'Got process memory usage: {mem_usage}')
            return mem_usage
        except Exception as e:
            self.logger.error(f'Error getting process memory usage: {e}')
            return None

    # Get the current process CPU and memory usage
    def get_cpu_and_memory_usage(self) -> tuple:
        try:
            self.logger.debug('Getting process CPU and memory usage...')
            cpu_usage = self.get_process_cpu_usage()
            mem_usage = self.get_process_memory_usage()
            self.logger.debug(
                f'Got process CPU and memory usage: {cpu_usage}, {mem_usage}')
            return (cpu_usage, mem_usage)
        except Exception as e:
            self.logger.error(
                f'Error getting process CPU and memory usage: {e}')
            return None

    # Get the process file location
    def get_process_file_location(self) -> str:
        try:
            self.logger.debug('Getting process file location...')
            p = self.get_current_process()
            file_location = p.exe()
            self.logger.debug(f'Got process file location: {file_location}')
            return file_location
        except Exception as e:
            self.logger.error(f'Error getting process file location: {e}')
            return None

    # Get the process file name
    def get_process_file_name(self) -> str:
        try:
            self.logger.debug('Getting process file name...')
            p = self.get_current_process()
            file_name = p.name()
            self.logger.debug(f'Got process file name: {file_name}')
            return file_name
        except Exception as e:
            self.logger.error(f'Error getting process file name: {e}')
            return None

    # Get how long the process has been running
    def get_process_uptime(self) -> timedelta:
        try:
            self.logger.debug('Getting process uptime...')
            p = self.get_current_process()
            uptime = p.create_time()
            self.logger.debug(f'Got process uptime: {uptime}')
            return uptime
        except Exception as e:
            self.logger.error(f'Error getting process uptime: {e}')
            return None

    # Check to see if the process is running
    def is_process_running(self) -> bool:
        try:
            self.logger.debug('Checking if process is running...')
            p = self.get_current_process()
            is_running = p.is_running()
            self.logger.debug(f'Process is running: {is_running}')
            return is_running
        except Exception as e:
            self.logger.error(f'Error checking if process is running: {e}')
            return None

    # Check to see if the process is running as root/superuser/admin
    def is_elevated(self) -> bool:
        try:
            self.logger.debug(
                'Checking if process is running as root/superuser/admin...')
            is_elevated = elevate.is_root()
            self.logger.debug(
                f'Process with pid of {getpid()} is running as root/superuser/admin: {is_elevated}')
            return is_elevated
        except Exception as e:
            self.logger.error(
                f'Error checking if process is running as root/superuser/admin: {e}')
            return None

    # Elevate the process to root/superuser/admin
    def elevate(self) -> bool:
        if self.is_elevated():
            self.logger.debug(
                'Process is already running as root/superuser/admin, skipping...')
            return True
        else:
            try:
                self.logger.debug(
                    'Elevating process to root/superuser/admin...')
                elevate()
                self.logger.debug('Process elevated to root/superuser/admin')
                return True
            except Exception as e:
                self.logger.error(
                    f'Error elevating process to root/superuser/admin: {e}')
                return False

    # Get the process uptime in a human readable format
    def get_readable_uptime(self) -> str:
        try:
            self.logger.debug(
                'Getting process uptime in a human readable format...')
            uptime = self.get_process_uptime()
            readable_uptime = strftime('%H:%M:%S', gmtime(uptime))
            self.logger.debug(
                f'Got process uptime in a human readable format: {readable_uptime}')
            return readable_uptime
        except Exception as e:
            self.logger.error(
                f'Error getting process uptime in a human readable format: {e}')
            return None

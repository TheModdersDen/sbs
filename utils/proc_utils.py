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

from datetime import timedelta
from os import getpid
from time import gmtime, strftime

from elevate import elevate
from psutil import Process

from utils.log_utils import LogUtils

#! Process related utilities


class ProcUtils():

    log_utils = LogUtils()
    logger = log_utils.get_sbs_logger()

    def __main__(self):
        self.log_utils = LogUtils()

        self.log_utils.log_msg('Proc Utils initializing...', 'DEBUG')

    # Get the current process ID
    def get_process_id(self) -> int:
        try:
            self.log_utils.log_msg('Getting process ID...')
            pid = getpid()
            self.log_utils.log_msg(f'Got process ID: {pid}')
            return pid
        except Exception as e:
            self.logger.error(f'Error getting process ID: {e}')
            return None

    # Get the current process
    def get_current_process(self) -> Process:
        try:
            self.log_utils.log_msg('Getting current process...')
            pid = self.get_process_id()
            p = Process(pid)
            self.log_utils.log_msg(f'Got current process: {p}')
            return p
        except Exception as e:
            self.logger.error(f'Error getting current process: {e}')
            return None

    # Get the current process CPU usage
    def get_process_cpu_usage(self) -> float:
        try:
            self.log_utils.log_msg('Getting process CPU usage...')
            p = self.get_current_process()
            cpu_usage = p.cpu_percent(interval=1)
            self.log_utils.log_msg(f'Got process CPU usage: {cpu_usage}')
            return cpu_usage
        except Exception as e:
            self.logger.error(f'Error getting process CPU usage: {e}')
            return None

    # Get the current process memory usage
    def get_process_memory_usage(self) -> float:
        try:
            self.log_utils.log_msg('Getting process memory usage...')
            p = self.get_current_process()
            mem_usage = p.memory_percent()
            self.log_utils.log_msg(f'Got process memory usage: {mem_usage}')
            return mem_usage
        except Exception as e:
            self.logger.error(f'Error getting process memory usage: {e}')
            return None

    # Get the current process CPU and memory usage
    def get_cpu_and_memory_usage(self) -> tuple:
        try:
            self.log_utils.log_msg('Getting process CPU and memory usage...')
            cpu_usage = self.get_process_cpu_usage()
            mem_usage = self.get_process_memory_usage()
            self.log_utils.log_msg(
                f'Got process CPU and memory usage: {cpu_usage}, {mem_usage}')
            return (cpu_usage, mem_usage)
        except Exception as e:
            self.logger.error(
                f'Error getting process CPU and memory usage: {e}')
            return None

    # Get the process file location
    def get_process_file_location(self) -> str:
        try:
            self.log_utils.log_msg('Getting process file location...')
            p = self.get_current_process()
            file_location = p.exe()
            self.log_utils.log_msg(
                f'Got process file location: {file_location}')
            return file_location
        except Exception as e:
            self.logger.error(f'Error getting process file location: {e}')
            return None

    # Get the process file name
    def get_process_file_name(self) -> str:
        try:
            self.log_utils.log_msg('Getting process file name...')
            p = self.get_current_process()
            file_name = p.name()
            self.log_utils.log_msg(f'Got process file name: {file_name}')
            return file_name
        except Exception as e:
            self.logger.error(f'Error getting process file name: {e}')
            return None

    # Get how long the process has been running
    def get_process_uptime(self) -> timedelta:
        try:
            self.log_utils.log_msg('Getting process uptime...')
            p = self.get_current_process()
            uptime = p.create_time()
            self.log_utils.log_msg(f'Got process uptime: {uptime}')
            return uptime
        except Exception as e:
            self.logger.error(f'Error getting process uptime: {e}')
            return None

    # Check to see if the process is running
    def is_process_running(self) -> bool:
        try:
            self.log_utils.log_msg('Checking if process is running...')
            p = self.get_current_process()
            is_running = p.is_running()
            self.log_utils.log_msg(f'Process is running: {is_running}')
            return is_running
        except Exception as e:
            self.logger.error(f'Error checking if process is running: {e}')
            return None

    # Check to see if the process is running as root/superuser/admin
    def is_elevated(self) -> bool:
        try:
            self.log_utils.log_msg(
                'Checking if process is running as root/superuser/admin...', 'DEBUG')
            is_elevated = elevate.is_root()
            self.log_utils.log_msg(
                f'Process with pid of {getpid()} is running as root/superuser/admin: {is_elevated}', 'DEBUG')
            return is_elevated
        except Exception as e:
            self.log_utils.log_msg(
                f'Error checking if process is running as root/superuser/admin: {e}', 'ERROR')
            return None

    # Elevate the process to root/superuser/admin
    def elevate(self) -> bool:
        if self.is_elevated():
            self.log_utils.log_msg(
                'Process is already running as root/superuser/admin, skipping...', 'DEBUG')
            return True
        else:
            try:
                self.log_utils.log_msg(
                    'Elevating process to root/superuser/admin...', 'DEBUG')
                elevate()
                self.log_utils.log_msg(
                    'Process elevated to root/superuser/admin', 'DEBUG')
                return True
            except Exception as e:
                self.logger.error(
                    f'Error elevating process to root/superuser/admin: {e}', 'ERROR')
                return False

    # Get the process uptime in a human readable format
    def get_readable_uptime(self) -> str:
        try:
            self.log_utils.log_msg(
                'Getting process uptime in a human readable format...', 'DEBUG')
            uptime = self.get_process_uptime()
            readable_uptime = strftime('%H:%M:%S', gmtime(uptime))
            self.log_utils.log_msg(
                f'Got process uptime in a human readable format: {readable_uptime}', 'DEBUG')
            return readable_uptime
        except Exception as e:
            self.logger.error(
                f'Error getting process uptime in a human readable format: {e}', 'ERROR')
            return None

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

#! A class to handle network functions for the ShowerThoughts Briefing Skill

# Imports
import socket
from requests import get

from sbs import SBS

from datetime import datetime, timedelta    
from time import sleep, time, strftime, gmtime

class NetworkUtils():
    
    def __main__(self):
        self.sbs = SBS()
        self.logger = self.sbs.logger
        
        self.logger.debug('Network Utils initializing...')
    
    # Get the current date and time from the internet, using the NTP protocol and the device's local time zone
    def date_time_from_internet(self) -> datetime:
        try:
            self.logger.debug('Getting date and time from internet...')
            # Get the current date and time from the internet, using the NTP protocol and the device's local time zone
            # Code from: https://stackoverflow.com/questions/1101508/how-to-parse-the-output-of-time-zone-dump
            from ntplib import NTPClient, NTPException
            from datetime import datetime, timedelta
            from dateutil import tz
            from os import system
            from subprocess import Popen, PIPE
            
            # Get the current date and time from the internet, using the NTP protocol and the device's local time zone
            # Code from: https://stackoverflow.com/questions/1101508/how-to-parse-the-output-of-time-zone-dump
            c = NTPClient()
            try:
                response = c.request('pool.ntp.org', version=3)
                dt = datetime.fromtimestamp(response.tx_time)
                self.logger.debug(f'Got date and time from internet: {dt}')
                return dt
            except NTPException:
                self.logger.error('Could not get date and time from internet, using system time instead')
                return datetime.now()
        except Exception as e:
            self.logger.error(f'Could not get date and time from internet: {e}')
            return datetime.now()
    
    # Download a file, put it into a folder, and return True if successful, False if not
    def download_file(self, url: str, file_name: str, output_dir: str) -> bool:
        try:
            self.logger.debug(f'Downloading file from {url} to {output_dir}{file_name}...')
            from requests import get
            from os import path
            from os.path import exists
            from os import makedirs
            from shutil import copyfileobj
            from tempfile import TemporaryFile
            
            # Make sure the output directory exists
            if not exists(output_dir):
                makedirs(output_dir)
            
            # Download the file
            with TemporaryFile() as tf:
                r = get(url, stream=True)
                if r.status_code == 200:
                    with open(path.join(output_dir, file_name), 'wb') as f:
                        r.raw.decode_content = True
                        copyfileobj(r.raw, f)
                    self.logger.debug(f'File downloaded successfully to {output_dir}{file_name}')
                    return True
                else:
                    self.logger.error(f'Could not download file from {url}')
                    return False
        except Exception as e:
            self.logger.error(f'Could not download file from {url}: {e}')
            return False
    
    # Get the external IP address of the device
    def get_device_ip_address(self) -> str:
        return get('https://api.ipify.org').decode('utf8')
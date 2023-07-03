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

from datetime import datetime, timedelta
from os.path import exists, isdir, isfile, join

from sbs import SBS
from utils.os_utils import OSUtils

from datetime import datetime, timedelta
from time import sleep, time, strftime, gmtime


class NetworkUtils():

    def __main__(self):
        self.sbs = SBS()
        self.logger = self.sbs.logger
        self.os_utils = OSUtils()

        self.logger.debug('Network Utils initializing...')

    # Get the current date and time from the internet, using the NTP protocol and the device's local time zone
    def date_time_from_internet(self) -> datetime:
        try:
            self.logger.debug('Getting date and time from internet...')
            # Get the current date and time from the internet, using the NTP protocol and the device's local time zone
            # Code from: https://stackoverflow.com/questions/1101508/how-to-parse-the-output-of-time-zone-dump
            from datetime import datetime, timedelta
            from os import system
            from subprocess import PIPE, Popen

            from dateutil import tz
            from ntplib import NTPClient, NTPException

            # Get the current date and time from the internet, using the NTP protocol and the device's local time zone
            # Code from: https://stackoverflow.com/questions/1101508/how-to-parse-the-output-of-time-zone-dump
            c = NTPClient()
            try:
                response = c.request('pool.ntp.org', version=3)
                dt = datetime.fromtimestamp(response.tx_time)
                self.logger.debug(f'Got date and time from internet: {dt}')
                return dt
            except NTPException:
                self.logger.error(
                    'Could not get date and time from internet, using system time instead')
                return datetime.now()
        except Exception as e:
            self.logger.error(
                f'Could not get date and time from internet: {e}')
            return datetime.now()

    # Download a file, put it into a folder, and return True if successful, False if not
    def download_file(self, url: str, file_name: str, output_dir: str) -> bool:
        try:
            self.logger.debug(
                f'Downloading file from {url} to {output_dir}{file_name}...')
            from os import makedirs, path
            from os.path import exists
            from shutil import copyfileobj
            from tempfile import TemporaryFile

            from requests import get

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
                    self.logger.debug(
                        f'File downloaded successfully to {output_dir}{file_name}')
                    return True
                else:
                    self.logger.error(f'Could not download file from {url}')
                    return False
        except Exception as e:
            self.logger.error(f'Could not download file from {url}: {e}')
            return False

    # Get the external IP address of the machine or network:

    def get_external_ip_address(self) -> str:
        from requests import get
        try:
            self.sbs.logger.debug("Getting external IP address...")
            return get('https://api.ipify.org').content.decode('utf8')
        except Exception as e:
            self.sbs.logger.error(
                "An error occurred when trying to resolve an IP address. Error Info:\n" + e)
            return None

        # Get the internal IP address of the machine or network:
    def get_internal_ip_address(self) -> str:
        try:
            import socket
            self.sbs.logger.debug("Getting internal IP address...")
            return socket.gethostbyname(socket.gethostname())
        except Exception as e:
            self.sbs.logger.error(
                "An error occurred when trying to resolve an IP address. Error Info:\n" + e)
            return None

        # Get a list of open ports on the machine or network:
    def get_open_ports(self) -> list:
        try:
            import subprocess

            self.sbs.debug("Getting open ports...")

            open_ports = []
            if self._os != 'Linux':
                raise NotImplementedError

            subprocess.call('netstat -an > netstat.txt', shell=True)

            with open('netstat.txt', 'r') as netstat:
                for line in netstat:
                    if 'LISTEN' in line:
                        open_ports.append(line.split()[3].split(':')[1])
                    else:
                        continue
            return open_ports
        except Exception as e:
            self.sbs.logger.error(
                "An error occurred when trying to resolve open ports. Error Info:\n" + e)
            return None

    # Get the current webserver in use on the machine:
    def get_webserver(self) -> str:
        if self._os == 'Windows':
            return None
        elif self._os == 'Linux':
            if exists("/etc/apache2"):
                return "Apache"
            elif exists("/etc/nginx"):
                return "Nginx"
            elif exists("/etc/lighttpd"):
                return "Lighttpd"
            elif exists("/etc/httpd"):
                return "Httpd"
            elif exists("/etc/cherokee"):
                return "Cherokee"
            elif exists("/etc/varnish"):
                return "Varnish"
            elif exists("/etc/squid"):
                return "Squid"
            elif exists("/etc/pound"):
                return "Pound"
            elif exists("/etc/hiawatha"):
                return "Hiawatha"
            elif exists("/etc/haproxy"):
                return "HAProxy"
            elif exists("/etc/stunnel"):
                return "Stunnel"
            elif exists("/etc/monkey"):
                return "Monkey"
            elif exists("/etc/mini_httpd"):
                return "Mini_httpd"
            elif exists("/etc/mongoose"):
                return "Mongoose"
        elif self._os == 'Darwin':
            return None
        pass

    # From the webserver, get the version of the webserver:
    def get_webserver_version(self, webserver="") -> str:
        if webserver == "" or webserver == None:
            webserver = self._webserver_name
        elif webserver == "Apache":
            with open("/etc/apache2/httpd.conf", "r") as httpd_conf:
                for line in httpd_conf:
                    if "ServerTokens" in line:
                        return line.split()[1]
        elif webserver == "Nginx":
            with open("/etc/nginx/nginx.conf", "r") as nginx_conf:
                for line in nginx_conf:
                    if "nginx/" in line:
                        return line.split()[1]
        elif webserver == "Lighttpd":
            with open("/etc/lighttpd/lighttpd.conf", "r") as lighttpd_conf:
                for line in lighttpd_conf:
                    if "lighttpd/" in line:
                        return line.split()[1]
        elif webserver == "Httpd":
            with open("/etc/httpd/httpd.conf", "r") as httpd_conf:
                for line in httpd_conf:
                    if "ServerTokens" in line:
                        return line.split()[1]
        elif webserver == "Cherokee":
            with open("/etc/cherokee/cherokee.conf", "r") as cherokee_conf:
                for line in cherokee_conf:
                    if "ServerTokens" in line:
                        return line.split()[1]
        elif webserver == "Varnish":
            with open("/etc/varnish/varnish.conf", "r") as varnish_conf:
                for line in varnish_conf:
                    if "ServerTokens" in line:
                        return line.split()[1]
        elif webserver == "Squid":
            with open("/etc/squid/squid.conf", "r") as squid_conf:
                for line in squid_conf:
                    if "ServerTokens" in line:
                        return line.split()[1]
        elif webserver == "Pound":
            with open("/etc/pound/pound.cfg", "r") as pound_conf:
                for line in pound_conf:
                    if "ServerTokens" in line:
                        return line.split()[1]
        elif webserver == "Hiawatha":
            with open("/etc/hiawatha/hiawatha.conf", "r") as hiawatha_conf:
                for line in hiawatha_conf:
                    if "ServerTokens" in line:
                        return line.split()[1]
        elif webserver == "HAProxy":
            with open("/etc/haproxy/haproxy.cfg", "r") as haproxy_conf:
                for line in haproxy_conf:
                    if "ServerTokens" in line:
                        return line.split()[1]
        elif webserver == "Stunnel":
            with open("/etc/stunnel/stunnel.conf", "r") as stunnel_conf:
                for line in stunnel_conf:
                    if "ServerTokens" in line:
                        return line.split()[1]
        elif webserver == "Monkey":
            with open("/etc/monkey/monkey.conf", "r") as monkey_conf:
                for line in monkey_conf:
                    if "ServerTokens" in line:
                        return line.split()[1]
        elif webserver == "Mini_httpd":
            with open("/etc/mini_httpd/mini_httpd.conf", "r") as mini_httpd_conf:
                for line in mini_httpd_conf:
                    if "ServerTokens" in line:
                        return line.split()[1]
        elif webserver == "Mongoose":
            with open("/etc/mongoose/mongoose.conf", "r") as mongoose_conf:
                for line in mongoose_conf:
                    if "ServerTokens" in line:
                        return line.split()[1]
        else:
            return None  # ! Unknown webserver

    # Get the port the webserver is running on:
    def get_webserver_port(self, webserver="") -> int:
        if webserver == "" or webserver == None:
            webserver = self._webserver_name
        elif webserver == "Apache":
            return 80
        elif webserver == "Nginx":
            return 80
        elif webserver == "Lighttpd":
            return 80
        elif webserver == "Httpd":
            return 80
        elif webserver == "Cherokee":
            return 80
        elif webserver == "Varnish":
            return 80
        elif webserver == "Squid":
            return 80
        elif webserver == "Pound":
            return 80
        elif webserver == "Hiawatha":
            return 80
        elif webserver == "HAProxy":
            return 80
        elif webserver == "Stunnel":
            return 80
        elif webserver == "Monkey":
            return 80
        elif webserver == "Mini_httpd":
            return 80
        elif webserver == "Mongoose":
            return 80
        else:
            return -1  # ! Unknown webserver

    # Get the hostname of the machine:
    def get_hostname(self) -> str:
        return self.os_utils._node

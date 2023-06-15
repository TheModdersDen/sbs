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

from os.path import exists, isdir, isfile, join
# A utility class for the ShowerThoughts Briefing Skill to handle OS specific functions
from platform import (architecture, libc_ver, mac_ver, machine, node, platform,
                      processor, python_implementation, python_version,
                      release, system, uname, version, win32_ver)

import distro

from sbs import SBS


class OSUtils():

    def __main__(self) -> object:
        # OS specific variables
        self.sbs = SBS()
        self._os = system()
        self._system = platform()
        self._arch = architecture()
        self._release = release()
        self._processor = processor()
        self._version = version()
        self._mach_type = machine()
        self._node = node()
        self._uname = uname()
        if self._os == 'Windows':
            self._win_ver = win32_ver()
        elif self._os == 'Linux':
            self._linux_dist = distro.linux_distribution()
        elif self._os == 'Darwin':
            self._mac_ver = mac_ver()
        self._libc_ver = libc_ver()

        # Network specific variables
        self._internal_ip_address = self.get_internal_ip_address()
        self._external_ip_address = self.get_external_ip_address()
        self._open_ports = self.get_open_ports()
        self._hostname = self.get_hostname()
        self._webserver_name = self.get_webserver()
        self._webserver_version = self.get_webserver_version()
        self._webserver_port = self.get_webserver_port()

        # Python specific variables
        self._python_ver = python_version()
        self._python_impl = python_implementation()

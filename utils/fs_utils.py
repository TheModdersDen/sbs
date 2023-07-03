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

#! A filesystem utilities class for the ShowerThoughts Briefing Skill

from os import mkdir
from os.path import exists, isdir, isfile, join

from sbs import SBS


class FSUtils():

    def __main__(self):
        self.sbs = SBS()
        self.logger = self.sbs.logger

        self.logger.debug('FS Utils initializing...')

        self._rss_export_path = self.sbs.cfg_parser.get(
            'DEFAULT', 'rss_export_path')
        try:
            if self._rss_export_path is not None:
                self.logger.debug(
                    f'RSS export path set to: {self._rss_export_path}')
                if self.folder_exists(self._rss_export_path):
                    self.logger.debug(
                        f'RSS export path exists: {self._rss_export_path}')
                else:
                    self.logger.debug(
                        "RSS export path doesn't exist. Attempting to create it...")
                    self.create_folder(self._rss_export_path)
        except Exception as e:
            self.logger.error(
                f'Error setting or creating RSS export path: {e}')

    # Check if a folder exists

    def folder_exists(self, folder_path: str) -> bool:
        if folder_path is not None:
            if exists(folder_path):
                if isdir(folder_path):
                    return True
                else:
                    return False
            else:
                return False

    # Check if a file exists
    def file_exists(self, file_path: str) -> bool:
        if file_path is not None:
            if exists(file_path):
                if isfile(file_path):
                    return True
                else:
                    return False
            else:
                return False

    # Join paths
    def join_paths(self, *args) -> str:
        return join(*args)

    # Create a folder
    def create_folder(self, folder_path: str) -> bool:
        if self.folder_exists(folder_path):
            return True
        else:
            try:
                mkdir(folder_path)
                return True
            except Exception as e:
                self.logger.error(f'Error creating folder: {e}')
                return False

    # Create an empty file
    def create_file(self, file_path: str) -> bool:
        if self.file_exists(file_path):
            return True
        else:
            try:
                open(file_path, 'w').close()
                return True
            except Exception as e:
                self.sbs.logger.error(f'Error creating file: {e}')
                return False

    def save_thoughts(self, current_thoughts: list) -> None:
        try:
            self.logger.debug(
                f'Saving thoughts to file: {self._rss_export_path}')
            with open(self._rss_export_path, 'w') as f:
                f.write(current_thoughts)
            self.logger.debug('Saved thoughts to file')
        except Exception as e:
            self.logger.error(f'Error saving thoughts to file: {e}')

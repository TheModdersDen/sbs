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

from configparser import ConfigParser
from os import getcwd, pathsep

from sbs import SBS

#! A class to handle the configuration for the ShowerThoughts Briefing Skill


class CFGUtils():

    def __main__(self) -> object:
        self.sbs = SBS()
        self.logger = self.sbs.logger

        self.logger.debug('CFG Utils initializing...')
        # Get the current working directory
        self.cwd = getcwd()

        # Get the path to the config file
        self.cfg_path = f'{self.cwd}{pathsep}config{pathsep}config.ini'

        # Initialize the config parser
        self.cfg_parser = ConfigParser()

        # Read the config file
        self.cfg_parser.read(self.cfg_path)

        # Get the config sections
        self.cfg_parser_sections = self.cfg_parser.sections()

        # Get the config defaults
        self.cfg_parser_defaults = self.cfg_parser.defaults()

        # Get the config options
        self.cfg_parser_options = self.cfg_parser.options('DEFAULT')

        # Get the config values
        self.cfg_parser_values = self.cfg_parser.values('DEFAULT')

        # Get the config items
        self.cfg_parser_items = self.cfg_parser.items('DEFAULT')

        # Get the config keys
        self.cfg_parser_keys = self.cfg_parser.keys('DEFAULT')

        # If the config file doesn't exist, create it
        try:
            self.logger.debug('Checking if config file exists...')
            self.cfg_parser.read(self.cfg_path)
            self.logger.debug('Config file exists')
        except Exception as e:
            self.logger.error(f'Config file does not exist: {e}')
            self.logger.debug('Creating config file...')
            self.cfg_parser.write(self.cfg_path)
        finally:
            # Set the default config values
            # Set to True to enable debug logging
            self.cfg_parser.set('DEFAULT', 'debug', 'False')
            # Set to DEBUG to enable debug logging
            self.cfg_parser.set('DEFAULT', 'log_level', 'INFO')
            self.cfg_parser.set('DEFAULT', 'log_filename',
                                'sbs.log')  # Set to the log filename
            # Set to True to enable sound effects inside the skill's TTS responses
            self.cfg_parser.set('DEFAULT', 'sound_effects', 'False')
            # Set the volume of the sound effects
            self.cfg_parser.set('DEFAULT', 'tts_responses', 'False')

        self.logger.debug('CFG Utils initialized')

    # Set a config value
    def set_value(self, section: str, option: str, value: str) -> bool:
        try:
            self.cfg_parser.set(section, option, value)
            self.logger.debug(f'Set config value: {option} to {value}')
            return True
        except Exception as e:
            self.logger.error(f'Error setting config value: {e}')
            return False

    # Get a config value
    def get_value(self, section: str, option: str) -> str:
        try:
            value = self.cfg_parser.get(section, option)
            self.logger.debug(f'Got config value: {value}')
            return value
        except Exception as e:
            self.logger.error(f'Error getting config value: {e}')
            return None

    # Get the config sections
    def get_config_sections(self) -> list:
        try:
            self.logger.debug('Getting config sections...')
            sections = self.cfg_parser.sections()
            self.logger.debug(f'Got config sections: {sections}')
            return sections
        except Exception as e:
            self.logger.error(f'Error getting config sections: {e}')
            return None

    # Get the config defaults
    def get_config_defaults(self) -> dict:
        try:
            self.logger.debug('Getting config defaults...')
            defaults = self.cfg_parser.defaults()
            self.logger.debug(f'Got config defaults: {defaults}')
            return defaults
        except Exception as e:
            self.logger.error(f'Error getting config defaults: {e}')
            return None

    # Get the config options
    def get_config_options(self) -> list:
        try:
            self.logger.debug('Getting config options...')
            options = self.cfg_parser.options('DEFAULT')
            self.logger.debug(f'Got config options: {options}')
            return options
        except Exception as e:
            self.logger.error(f'Error getting config options: {e}')
            return None

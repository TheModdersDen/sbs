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

# The main class for the ShowerThoughts Briefing Skill:
#   - Handles the Alexa requests
#   - Requests the feed from Reddit using feedparser and the Reddit rss feed
#   - Generates the response in the Alexa format
#   - Sends the response to Alexa for the user

import base64
import gzip
import hashlib
import hmac
import json
import logging
import os
import random
import re
import urllib.parse
import urllib.request
import uuid
import xml.etree.ElementTree as ET
from argparse import ArgumentParser, Namespace
from configparser import ConfigParser
from datetime import datetime, timedelta
from os import getcwd, pathsep
from time import gmtime, sleep, strftime, time

import boto3
import pytz
from boto3.dynamodb.conditions import Attr, Key
from dotenv import load_dotenv

from utils.cfg_utils import CFGUtils
from utils.feed_utils import FeedUtils
from utils.fs_utils import FSUtils
from utils.log_utils import LogUtils
from utils.os_utils import OSUtils
from utils.proc_utils import ProcUtils
from utils.profanity_filter import SBSProfanityFilter


# The main SBS class
class SBS():

    def handle_cmdline(self) -> Namespace:
        self.arg_parser = ArgumentParser(
            description='ShowerThoughts Briefing Skill')
        self.arg_parser.add_argument(
            '-r', '--rate', help='The rate to refresh the ShowerThoughts (which feed to pull it from?)', required=True, dest='rate')
        self.arg_parser.add_argument('-p', '--profanity', help='Filter out profanity?',
                                     required=True, default=True, dest='profanity')
        self.arg_parser.add_argument('-c', '--censor', help='Censor the profanity?',
                                     required=False, default=True, dest='censor')
        self.arg_parser.add_argument(
            '-x', '--extra-words', help='Extra profanity word file to filter out profanity with', required=False, dest='extra_words')
        self.arg_parser.add_argument('-d', '--debug', help='Debug mode?', required=False,
                                     action='store_true', default=False, dest='debug')
        self.arg_parser.add_argument('-e', '--experimental', help='Experimental mode?',
                                     required=False, default=False, dest='experimental')
        self.arg_parser.add_argument('-f', '--feed', help='Save the thoughts to a RSS feed?',
                                     required=False, default=False, dest='feed')
        self.arg_parser.add_argument('-s', '--save', help='Save the thoughts to a text file?',
                                     required=False, default=False, dest='save')

        self.args = self.arg_parser.parse_args()

        return self.args

    # Initialize the class

    def __main__(self) -> object:

        # Load the environment variables
        load_dotenv()
        self.args = self.handle_cmdline()
        # Initialize the variables
        self.cfg_utils = CFGUtils()
        self.cfg_parser = self.cfg_utils.cfg_parser
        self.extra_profanity_words = None
        if self.args.profanity.lower() == "true" or self.args.profanity.lower() == "yes" or self.args.profanity.lower() == "y":
            try:
                with open(getcwd() + f"data{pathsep}badwords.txt", "r") as f:
                    self.extra_profanity_words = f.read().splitlines()
                self.profanity_filter = SBSProfanityFilter(
                    self.extra_profanity_words, False)
            except Exception as e:
                self.logger.error(f"Error loading extra profanity words: {e}")
        if self.args.profanity is False:
            self.extra_profanity_words = []

        self.os_utils = OSUtils()
        self.fs_utils = FSUtils()
        self.env_vars = []

        self.feed_utils.parse_feed()

    # Handle the main logic of the skill

    def process_data(self):
        self.args = self.handle_cmdline()
        self.feed_utils = FeedUtils()
        self.log_utils = LogUtils()
        self.proc_utils = ProcUtils()

        # Elevate the process if needed
        if self.proc_utils.is_elevated():
            self.log_utils.log_msg(
                'SBS Skill running with elevated privileges, no need to elevate...', "DEBUG")
        else:
            self.log_utils.log_msg(
                'SBS Skill not running with elevated privileges, elevating...', "DEBUG")
            self.proc_utils.elevate()

        # Get the current process
        self.current_process = self.proc_utils.get_current_process()

        # Parse the Reddit RSS feed
        self.feed_utils.parse_feed(
            f"https://reddit.com/r/showerthoughts/top.rss?t={self.args.rate}&limit=50")

        self.log_utils.log_msg('SBS Skill processing data...')

        # Get the thoughts from the feed
        self.current_thoughts = self.feed_utils.get_thoughts(self.args.rate)

        if self.args.save:
            # Save the thoughts to a text file
            self.fs_utils.save_thoughts(self.current_thoughts)

        # Get the thoughts from the feed
        self.feed_utils.generate_feed(self.current_thoughts)


if __name__ == '__main__':
    sbs = SBS()
    sbs.process_data()

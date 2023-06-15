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
import shutil
import sys
import time
import traceback
import urllib.parse
import urllib.request
import uuid
import xml.etree.ElementTree as ET
from argparse import ArgumentParser, Namespace
from configparser import ConfigParser
from datetime import datetime, timedelta
from os import getcwd, pathsep

import boto3
import feedparser
import pytz
from boto3.dynamodb.conditions import Attr, Key
from dotenv import load_dotenv

from utils.feed_utils import FeedUtils
from utils.os_utils import OSUtils
from utils.profanity_filter import ProfanityFilter


# The main SBS class
class SBS(object):

    # Initialize the class
    def __main__(self) -> object:

        # Load the environment variables
        load_dotenv()

        # Initialize the variables
        self.extra_profanity_words = []
        self.profanity_filter = ProfanityFilter(
            self.extra_profanity_words, False)
        self.feed_utils = FeedUtils()
        self.os_utils = OSUtils()
        self.env_vars = []
        handler = logging.FileHandler(
            getcwd() + f"{pathsep}logs{pathsep}sbs_latest.log")
        self.logger = logging.getLogger("sbs_skill")
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

        self.handle_cmdline()
        self.feed_utils.parse_feed()

    def handle_cmdline(self) -> Namespace:
        self.arg_parser = ArgumentParser(
            description='ShowerThoughts Briefing Skill')
        self.arg_parser.add_argument(
            '-r', '--rate', help='The rate to refresh the ShowerThoughts (which feed to pull it from?)', required=True, dest='rate', type=str)
        self.arg_parser.add_argument('-l', '--log', help='Log the output to a file?',
                                     required=False, action='store_true', default=False, dest='log', type=bool)
        self.arg_parser.add_argument('-p', '--profanity', help='Filter out profanity?',
                                     required=True, action='store_true', default=False, dest='profanity', type=bool)
        self.arg_parser.add_argument('-c', '--censor', help='Censor the profanity?',
                                     required=False, action='store_true', default=False, dest='censor', type=bool)
        self.arg_parser.add_argument(
            '-x', '--extra', help='Extra profanity word file to filter out profanity with', required=False, dest='extra', type=str)
        self.arg_parser.add_argument('-d', '--debug', help='Debug mode?', required=False,
                                     action='store_true', default=False, dest='debug', type=bool)
        self.arg_parser.add_argument('-e', '--experimental', help='Experimental mode?',
                                     required=False, action='store_true', default=False, dest='experimental', type=bool)
        self.arg_parser.add_argument('-v', '--version', help='Show the version and exit',
                                     required=False, action='store_true', default=False, dest='version', type=bool)
        self.arg_parser.add_argument('-f', '--feed', help='Save the thoughts to a RSS feed?',
                                     required=False, action='store_true', default=False, dest='feed', type=bool)
        self.arg_parser.add_argument('-s', '--save', help='Save the thoughts to a text file?',
                                     required=False, action='store_true', default=False, dest='save', type=bool)

        self.args = self.arg_parser.parse_args()

        return self.args

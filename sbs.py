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

import logging
import os
import random
import re
import requests
import time
import urllib
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import feedparser
from datetime import datetime, timedelta
import pytz
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import uuid
import hashlib
import hmac
import base64
from feedgenerator import Rss201rev2Feed, Enclosure
import io
import gzip
import shutil
import traceback
import sys
import platform
from dotenv import load_dotenv
from os import getcwd, pathsep

from utils.feed_utils import FeedUtils
from utils.os_utils import OSUtils
from utils.profanity_filter import ProfanityFilter

# The main SBS class
class SBS(object):
    
    # Initialize the class    
    def __main__(self) -> object:
        # Initialize the variables
        self.extra_profanity_words = []
        self.profanity_filter = ProfanityFilter(self.extra_profanity_words, False)
        self.feed_utils = FeedUtils()
        self.os_utils = OSUtils()
        self.env_vars = []
        handler = logging.FileHandler(getcwd() + f"{pathsep}logs{pathsep}sbs_latest.log")
        self.logger = logging.getLogger("sbs_skill")
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        
        
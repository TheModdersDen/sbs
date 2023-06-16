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

import io
from os import getcwd, pathsep
from time import gmtime, sleep, strftime, time

from feedgenerator import Enclosure, Rss201rev2Feed
from feedparser import parse

from sbs import SBS


# A class to handle the feed generation for the ShowerThoughts Briefing Skill

class FeedUtils():

    def __main__(self) -> object:
        self.sbs = SBS()

        self.sbs.logger.debug('Feed Utils initializing...')

        self.sbs.logger.debug('Feed Utils initialized')

    def parse_feed(self, feed_url: str) -> object:
        pass

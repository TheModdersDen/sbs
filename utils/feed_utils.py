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

import os
from os import getcwd, getenv, pathsep

from feedgenerator import Enclosure, Rss201rev2Feed
from feedparser import parse

from utils.log_utils import LogUtils
from utils.profanity_filter import SBSProfanityFilter

# A class to handle the feed generation for the ShowerThoughts Briefing Skill


class FeedUtils():

    def __main__(self) -> object:

        self.log_utils = LogUtils()

        self.log_utils.logger.debug('Feed Utils initializing...')

        self.rss_feed_last_build_date = getenv('RSS_FEED_LAST_BUILD_DATE')

        self.log_utils.logger.debug('Feed Utils initialized')

    # Parse the feed using feedparser
    def parse_feed(self, feed_url: str) -> object:
        self.log_utils = LogUtils()
        self.logger = self.log_utils.sbsLogger
        try:
            self.log_utils.log_msg(f'Parsing feed: {feed_url}', "DEBUG")
            feed = parse(feed_url)
            self.log_utils.log_msg(f'Parsed feed: {feed}', 'DEBUG')
            return feed
        except Exception as e:
            self.log_utils.log_msg(f'Error parsing feed: {e}', 'ERROR')
            return None

    # Process the feed using feedgenerator and the parsed feed, and return the feed as a list
    def process_feed(self, feed: object) -> list:
        self.log_utils = LogUtils()
        self.logger = self.log_utils.sbsLogger
        if feed is not None:
            try:
                self.log_utils.log_msg(f'Processing feed: {feed}', "DEBUG")
                feed_list = []
                for entry in feed.entries:
                    feed_list.append(entry)
                self.log_utils.log_msg(f'Processed feed: {feed_list}', "DEBUG")
                return feed_list
            except Exception as e:
                self.log_utils.log_msg(f'Error processing feed: {e}', "ERROR")
                return None
        else:
            self.sbs.logger.error('The feed has nothing to process!')
            raise Exception('The feed has nothing to process!')

    def generate_feed(self, feed_list: list) -> object:
        self.log_utils = LogUtils()
        self.logger = self.log_utils.sbsLogger
        if feed_list is not None:
            rss_list = []
            try:
                if "RSS_FEED_TITLE" in os.environ and "RSS_FEED_URL" in os.environ and "RSS_FEED_DESCRIPTION" in os.environ and "RSS_FEED_LANGUAGE" in os.environ and "RSS_FEED_URL_DIRECT" in os.environ and "RSS_FEED_TTL" in os.environ and "RSS_FEED_GENERATOR" in os.environ and "RSS_FEED_LAST_BUILD_DATE" in os.environ and "RSS_FEED_WEBMASTER" in os.environ and "RSS_FEED_PUBDATE" in os.environ:
                    self.log_utils.logger.debug(
                        f'Generating feed: {feed_list}')
                    feed = Rss201rev2Feed(
                        title=getenv('RSS_FEED_TITLE'),
                        link=getenv('RSS_FEED_URL'),
                        description=getenv('RSS_FEED_DESCRIPTION'),
                        language=getenv('RSS_FEED_LANGUAGE'),
                        feed_url=getenv('RSS_FEED_URL_DIRECT'),
                        ttl=getenv('RSS_FEED_TTL'),
                        generator=getenv('RSS_FEED_GENERATOR'),
                        lastBuildDate=getenv(
                            f'{self.rss_feed_last_build_date}'),
                        webMaster=getenv('RSS_FEED_WEBMASTER'),
                        pubDate=getenv('RSS_FEED_PUBDATE')
                    )
                    for entry in feed_list:
                        rss_list.append(feed.add_item(feed_item=entry))
                    self.log_utils.logger.debug(f'Generated feed: {rss_list}')
            except Exception as e:
                self.log_utils.logger.error(f'Error generating feed: {e}')
                raise Exception(
                    'The feed has nothing to generate! Please check the stack trace for more details.')

    def get_thoughts(self, feed_rate: str = "day", ) -> list:
        self.log_utils = LogUtils()
        sbs_pf = SBSProfanityFilter()
        self.logger = self.log_utils.sbsLogger
        try:
            self.log_utils.log_msg(
                f'Parsing feed: {f"https://reddit.com/r/showerthoughts/top.rss?t={feed_rate}&limit=50"}', "DEBUG")
            feed = parse(
                "https://reddit.com/r/showerthoughts/top.rss?t={feed_rate}&limit=50")
            self.log_utils.log_msg(f'Parsed feed: {feed}', 'DEBUG')
            feed_items = []
            for count in range(0, 49):
                if (feed.entries[count].title is not None) and (feed.entries[count].title != "") and sbs_pf.is_profane(feed.entries[count].title) == False:                    feed_items.append(feed.entries[count].title)
                else:
                    self.log_utils.log_msg(
                        f'Feed item number: {count} is profane, skipping...', 'WARNING')
                    continue
            return feed
        except Exception as e:
            self.log_utils.log_msg(f'Error parsing feed: {e}', 'ERROR')
            return None
    # Get the extra profanity words from the "badwords.txt" file in the data directory

    def get_extra_profanity_words(self) -> list:
        with open(getcwd() + f"{pathsep}data{pathsep}badwords.txt", "r") as f:
            self.badwords = f.read().splitlines()

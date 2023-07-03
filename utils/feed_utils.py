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

from os import getenv

from feedgenerator import Enclosure, Rss201rev2Feed
from feedparser import parse

from sbs import SBS

# A class to handle the feed generation for the ShowerThoughts Briefing Skill


class FeedUtils():

    def __main__(self) -> object:
        self.sbs = SBS()

        self.sbs.logger.debug('Feed Utils initializing...')

        self.sbs.logger.debug('Feed Utils initialized')

    # Parse the feed using feedparser
    def parse_feed(self, feed_url: str) -> object:
        try:
            self.sbs.logger.debug(f'Parsing feed: {feed_url}')
            feed = parse(feed_url)
            self.sbs.logger.debug(f'Parsed feed: {feed}')
            return feed
        except Exception as e:
            self.sbs.logger.error(f'Error parsing feed: {e}')
            return None

    # Process the feed using feedgenerator and the parsed feed, and return the feed as a list
    def process_feed(self, feed: object) -> list:
        if feed is not None:
            try:
                self.sbs.logger.debug(f'Processing feed: {feed}')
                feed_list = []
                for entry in feed.entries:
                    feed_list.append(entry)
                self.sbs.logger.debug(f'Processed feed: {feed_list}')
                return feed_list
            except Exception as e:
                self.sbs.logger.error(f'Error processing feed: {e}')
                return None
        else:
            self.sbs.logger.error('The feed has nothing to process!')
            raise Exception('The feed has nothing to process!')

    def generate_feed(self, feed_list: list) -> object:
        if feed_list is not None:
            rss_list = []
            try:
                self.sbs.logger.debug(f'Generating feed: {feed_list}')
                feed = Rss201rev2Feed(
                    title=getenv('RSS_FEED_TITLE'),
                    link=getenv('RSS_FEED_URL'),
                    description=getenv('RSS_FEED_DESCRIPTION'),
                    language=getenv('RSS_FEED_LANGUAGE'),
                    feed_url=getenv('RSS_FEED_URL_DIRECT'),
                    ttl=getenv('RSS_FEED_TTL'),
                    generator=getenv('RSS_FEED_GENERATOR'),
                )
                for entry in feed_list:
                    rss_list.append(feed.add_item(feed_item=entry))
                self.sbs.logger.debug(f'Generated feed: {rss_list}')
            except Exception as e:
                self.sbs.logger.error(f'Error generating feed: {e}')
                return None

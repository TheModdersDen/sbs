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

import logging
from os import getcwd
from os.path import pathsep

import spacy
from profanity_filter import ProfanityFilter

from sbs import SBS


# A class to filter out profanity from the ShowerThoughts Briefing Skill
class SBSProfanityFilter():

    def __main__(self, extra_filter_words=[], censor=False, log_profanity_filter=False) -> object:

        self.sbs = SBS()

        # Should we log the profanity filter?
        if log_profanity_filter:
            self.sbs.logger.debug(
                'Profanity filter initializing, logging enabled...')
        else:
            self.sbs.logger.debug(
                'Profanity filter initializing, logging disabled...')

        if extra_filter_words is None or extra_filter_words == []:
            try:
                self.sbs.logger.debug(
                    'Profanity filter: No extra filter words specified, using default')
                self.extra_filter_words = self.get_extra_profanity_words()
            except Exception as e:
                self.sbs.logger.error(
                    f'Profanity filter: Error getting extra filter words: {e}')
        else:
            self.extra_filter_words = extra_filter_words  # Extra words to filter out
        self.censor = censor  # Should the words be censored or removed?

        self.nlp = spacy.load('en')
        self.pf = ProfanityFilter(extra_profane_word_dictionaries=self.extra_filter_words,
                                  censor_whole_words=self.censor, censor_char='*', nlps={'en': self.nlp})

        self.sbs.logger.debug('Profanity filter initialized')

    # Check if the text contains profanity
    # Returns True if profanity is found, False if not
    def check_profanity(self, text: str) -> bool:
        return self.pf.is_profane(text)

    # Get the extra profanity words from the "badwords.txt" file in the data directory
    def get_extra_profanity_words(self) -> list:
        with open(getcwd() + f"{pathsep}data{pathsep}badwords.txt", "r") as f:
            self.badwords = f.read().splitlines()

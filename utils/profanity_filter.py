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

from os import getcwd
from os.path import pathsep

from utils import os_utils
from utils.log_utils import LogUtils
from utils.os_utils import OSUtils

# A class to filter out profanity from the ShowerThoughts Briefing Skill

if OSUtils._os == 'Linux':
    import spacy
    from profanity_filter import ProfanityFilter

    class SBSProfanityFilter():
        def __init__(self, extra_filter_words=[], censor=False, log_profanity_filter=False):
            self.nlp = spacy.load('en_core_web_sm')
            self.sbs_pf = ProfanityFilter(extra_profane_word_dictionaries=self.get_extra_profanity_words(),
                                          censor_whole_words=False, censor_char='*', nlps={'en': self.nlp})
            self.extra_filter_words = extra_filter_words
            self.censor = censor
            self.log_profanity_filter = log_profanity_filter

        def is_profane(self, text: str) -> bool:
            return self.sbs_pf.is_profane(text)

        def get_extra_profanity_words(self) -> list:
            with open(getcwd() + f"{pathsep}data{pathsep}badwords.txt", "r") as f:
                self.badwords = f.read().splitlines()
            return [self.badwords] if self.extra_filter_words == [] else [self.badwords, self.extra_filter_words]

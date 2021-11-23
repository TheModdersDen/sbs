from profanity_check import predict, predict_prob
import argparse
import codecs
import datetime
import io
import logging
import os
import os.path
import random
import uuid
import platform
import feedgenerator
import simplejson as json
import feedparser

def getLogger():
    logging.basicConfig(filename="sbs.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    return logger

logger = getLogger()

def main():
    #print(', '.join(sorted(analysis.value for analysis in AVAILABLE_ANALYSES)))
    currentOS = getCurrentOS()
    LOG_INFO(f"Current OS type is: '{platform.system()}.'")


def LOG_DEBUG(MSG):
    logger.debug(f"DEBUG: {MSG}")
    print(f"DEBUG: {MSG}")
def LOG_WARN(MSG):
    logger.warn(f"WARN: {MSG}")
    print(f"WARN: {MSG}")
def LOG_INFO(MSG):
    logger.info(f"INFO: {MSG}")
    print(f"INFO: {MSG}")
def LOG_ERROR(MSG):
    logger.error(f"ERROR: {MSG}")
    print(f"ERROR: {MSG}")

def isProfane(input):
    if predict_prob([input]) >= [0.1] or predict([input]) == [1]:
        return True
    else:
        return False

def getCurrentOS():
    if platform.system() == "Linux":
        return 0 # Linux
    elif platform.system() == "Windows":
        return 1 # Windows
    elif platform.system() == "Darwin":
        return 2 # macOS

def makeExtraProfanityDict(inputFile):
    extra_bad_words_dict = {}
    
    with open(inputFile, "r") as word_file:
        for item in word_file.readlines():
            print(item)
            extra_bad_words_dict.update({item})
    
    return extra_bad_words_dict

def create_tts_file(thought, out_file):
    pass

def create_rss_feed(out_file):
    pass

def processRedditFeed(update_frequency):
    thought_list = []
    if update_frequency not in ["daily", "hourly"]:
        pass
    d = feedparser.parse("https://reddit.com/r/showerthoughts/top.rss?t=" + update_frequency)
    
    for post in d.entries:
        if isProfane(post.title):
            print(f"NOT ADDING: '{post.title}' as it is profane.")
        else:
            thought_list.append(post.title)
        

if __name__ == "__main__":
    main()
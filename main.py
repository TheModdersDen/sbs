from profanity_check import predict, predict_prob
import argparse
import subprocess
import codecs
import datetime
import io
import logging
import os
import os.path
import random
import uuid
import platform
from feedgenerator import Rss201rev2Feed, Enclosure
import simplejson as json
import feedparser
from boto3 import Session, client
import glob
from decouple import config

uuid = uuid.uuid4()
currentId = str(uuid)
URN_UUID = uuid.urn
encoding_type = "utf-8"

dt = datetime.date.today()
now = datetime.datetime.now()
current_time = now.strftime("%H:%M:%S")
currentDate = dt.isoformat()
print(currentDate + "--" + current_time)
out_file = f"polly_output{currentId}.mp3"
feed_title = f"Your ShowerThoughts Update ({currentDate}--{current_time})"
feed_link = config("MAIN_URL") + f"polly_out/polly_output{currentId}.mp3"
feed_description="This is an expiremental feed to use Amazon Polly to read the ShowerThoughts Reddit page to end users."

out_dir = config("OUT_DIR")
feed_dir = config("FEED_DIR")
update_frequency = config("REFRESH_RATE")

VERSION = "0.0.0.1-dev"

def getLogger():
    logging.basicConfig(filename="sbs.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    return logger

def get_file_size(file_name):
        statinfo = os.stat(file_name)
        return statinfo.st_size

logger = getLogger()

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

def create_file_from_path(file_path):
        if not os.path.exists(os.path.dirname(file_path)):
            try:
                os.makedirs(os.path.dirname(file_path))
            except OSError as exc:
                LOG_ERROR(f"{exc}")
                print(f"ERROR: {exc}")

def create_tts_file(thought, out_dir_var,  out_file_name):
    polly_command = f'cd {out_dir_var} && sudo aws polly synthesize-speech --text-type ssml --output-format "mp3" --voice-id "Salli" --engine neural --text "<speak>{thought}</speak>" {out_file_name}'
    print(polly_command)
    polly = client('polly', region_name='us-west-2')
    
    os.system(polly_command)

def make_polly_file(out_dir_var):
    file_names = ""
    tts_files = glob.glob(f'{out_dir_var}/*.mp3')
    tts_files.sort()
    for tts_file in tts_files:
        file_names += f" {tts_file}"
    file_names = file_names[1:]
    merge_command = f"cat {file_names} >polly_output{currentId}.mp3"
    os.system(merge_command)
    file_names = ""
    for tts_file in tts_files:
        if tts_file == "_intro.mp3" or tts_file == "z_outro.mp3":
            continue
        else:
            file_names += f" {tts_file}"
    cleanup_command = f"rm {file_names}"
    os.system(cleanup_command)
    
    move_command = f"mv polly_output{currentId}.mp3 {out_dir}"
    print(move_command)
    os.system(move_command)

def create_rss_feed():
    test_feed = Rss201rev2Feed(
        title="ShowerThoughts Briefing Feed",
        link=config("MAIN_URL") + "st-test.xml",
        description=feed_description,
        ttl=60,
        language="en")
    
    tts_filesize = get_file_size(out_dir + out_file)
    
    test_feed.add_item(
            unique_id=URN_UUID,
            title=feed_title,
            description=feed_description,
            link=feed_link,
            pubdate=datetime.datetime.utcnow(),
            enclosure=Enclosure(str(feed_link), str(tts_filesize), "audio/mpeg")
    )
    
    with codecs.open(f"{feed_dir}st-test.xml", "w", encoding=encoding_type) as rss_feed:
            rss_feed.truncate()
            rss_feed.write(test_feed.writeString(encoding_type))
            rss_feed.close()

def processRedditFeed(update_frequency):
    thought_list = []
    if update_frequency not in ["day", "hour"]:
        raise Exception("Please put in either 'daily' or 'hourly' as a timeframe for the Reddit feed.")
    d = feedparser.parse("https://reddit.com/r/showerthoughts/top.rss?t=" + update_frequency)
    post_index = 0
    for post in d.entries:
        if isProfane(post.title):
            print(f"NOT ADDING: '{post.title}' as it is profane.")
        else:
            post_index += 1
            print(f"ADDING: '{post.title}' as it is NOT profane.")
            thought_list.append(post.title)
            create_tts_file(post.title, os.getcwd(), f"polly_out{post_index}.mp3")
    return thought_list
        
def main():
    #print(', '.join(sorted(analysis.value for analysis in AVAILABLE_ANALYSES)))
    currentOS = getCurrentOS()
    LOG_INFO(f"Current OS type is: '{platform.system()}.'")
    if currentOS == 0:
        create_file_from_path("/var/www/html/st/polly_out/")
    elif currentOS == 1:
        LOG_WARN("Your OS, Windows, is currently not supported. This program will likely fail.")
    elif currentOS == 2:
        LOG_WARN("Your OS, Darwin (macOS or Mac OS X), is currently not supported. This program will likely fail.")
    processRedditFeed(update_frequency)
    make_polly_file(os.getcwd())
    create_rss_feed()

if __name__ == "__main__":
    main()
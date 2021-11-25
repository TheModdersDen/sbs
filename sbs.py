from decouple import config
from profanity_check import predict, predict_prob
import urllib.request
import codecs
import datetime
import os
import os.path
import platform
from feedgenerator import Rss201rev2Feed, Enclosure
import feedparser
import glob
from time import sleep
from elevate import elevate

from sbs_vars import SBS_vars
from utils import Utils


class SBS():

    vars = SBS_vars()

    def __init__(self):
        self.feed = "https://reddit.com/r/showerthoughts/top.rss?t="
        self.env_vars_dict = {}
        self.vars_list = {}
        utils = Utils()

        self.thought_file = f"thoughts/thoughts-{self.vars.currentDate}--{self.vars.current_time}.txt"
        self.thoughts_data = None

        def is_root():
            return os.getuid() == 0

        if is_root() == False:
            elevate()
        else:
            utils.LOG_DEBUG(
                "Process is running as administrator/root. No need to elevate.")

            self.main_url = self.vars.main_url
            self.out_dir = self.vars.out_dir
            self.feed_dir = self.vars.feed_dir
            self.update_frequency = self.vars.update_frequency

    def isProfane(self, input):
        if predict_prob([input]) >= [0.1] or predict([input]) == [1]:
            return True
        else:
            return False

    def getCurrentOS(self):
        if platform.system() == "Linux":
            return 0  # Linux
        elif platform.system() == "Windows":
            return 1  # Windows
        elif platform.system() == "Darwin":
            return 2  # macOS

    def processRedditFeed(self, update_frequency):
        if self.update_frequency not in ["day", "hour"]:
            raise Exception(
                "Please put in either 'day' or 'hour' as a timeframe for the Reddit feed.")
        d = feedparser.parse(
            "https://reddit.com/r/showerthoughts/top.rss?t=" + update_frequency)
        post_index = 0
        for post in d.entries:
            if self.isProfane(post.title):
                print(f"NOT ADDING: '{post.title}' as it is profane.")
                self.vars.utils.LOG_INFO(
                    f"NOT ADDING: '{post.title}' as it is profane.")
            else:
                post_index += 1
                print(f"ADDING: '{post.title}' as it is NOT profane.")
                self.vars.utils.LOG_INFO(
                    f"ADDING: '{post.title}' as it is NOT profane.")
                self.create_tts_file(
                    post.title, os.getcwd(), f"polly_out{post_index}.mp3")
        thoughts = ['ShowerThoughts Database File:',
                    f"{self.vars.currentDate}--{self.vars.current_time}"]
        for post in d.entries:
            thoughts.append(post.title)
        thoughts.append(
            "That's all for today! Come back tomorrow for more ShowerThoughts.")
        self.vars.utils.create_file_from_path(f"{os.getcwd()}/thoughts/")
        with open(self.thought_file, "w+") as thought_file:
            for thought in thoughts:
                thought_file.write(thought + "\n")

    def create_tts_file(self, data, out_dir_var,  out_file_name):
        polly_command = f'cd {out_dir_var} && sudo aws polly synthesize-speech --text-type ssml --output-format "mp3" --voice-id "Salli" --engine neural --text "<speak>{data}</speak>" {out_file_name}'
        print(polly_command)
        os.system(polly_command)

    def make_polly_file(self, out_dir_var):
        file_names = ""
        tts_files = glob.glob(f'{out_dir_var}/*.mp3')
        tts_files.sort()
        for tts_file in tts_files:
            file_names += f" {tts_file}"
        file_names = file_names[1:]
        merge_command = f"cat {file_names} >polly_output{self.vars.currentId}.mp3"
        os.system(merge_command)
        self.vars.utils.LOG_DEBUG("Running command: '" + merge_command + "'")
        file_names = ""
        for tts_file in tts_files:
            if tts_file == "_intro.mp3" or tts_file == "z_outro.mp3":
                continue
            else:
                file_names += f" {tts_file}"
        cleanup_command = f"rm {file_names}"
        os.system(cleanup_command)
        self.vars.utils.LOG_DEBUG("Running command: '" + cleanup_command + "'")

        move_command = f"mv polly_output{self.vars.currentId}.mp3 {self.vars.out_dir}"
        self.vars.utils.LOG_DEBUG("Running command: '" + move_command + "'")
        os.system(move_command)

    def create_rss_feed(self):
        test_feed = Rss201rev2Feed(
            title="ShowerThoughts Briefing Feed",
            link=self.vars.main_url + "st-test.xml",
            description=self.vars.feed_description,
            ttl=60,
            language="en")

        tts_filesize = self.vars.utils.get_file_size(
            self.vars.out_dir + self.vars.out_file)

        test_feed.add_item(
            unique_id=self.vars.URN_UUID,
            title=self.vars.feed_title,
            description=self.vars.feed_description,
            link=self.vars.feed_link,
            pubdate=datetime.datetime.utcnow(),
            enclosure=Enclosure(str(self.vars.feed_link),
                                str(tts_filesize), "audio/mpeg")
        )

        with codecs.open(f"{self.vars.feed_dir}st-test.xml", "w", encoding=self.vars.encoding_type) as rss_feed:
            rss_feed.truncate()
            rss_feed.write(test_feed.writeString(self.vars.encoding_type))
            rss_feed.close()

    def main(self):
        version_URL = urllib.request.urlopen(f"{self.vars.main_url}ST_VERSION")
        self.vars.utils.LOG_DEBUG(
            f"result code for version_URL: {str(version_URL.getcode())}".strip("\n"))
        data = version_URL.read()
        print(f"Starting SBS v{data}... Please wait.")
        currentOS = self.getCurrentOS()
        self.vars.utils.LOG_INFO(f"Current OS type is: '{platform.system()}.'")
        if currentOS == 0:
            self.vars.utils.create_file_from_path("/var/www/html/st/polly_out/")
        elif currentOS == 1:
            print("Your OS, Windows, is currently not supported. Exiting gracefully...")
            self.vars.utils.LOG_ERROR(
                "Your OS, Windows, is currently not supported. Exiting gracefully...")
            sleep(5)
            exit(1)
        elif currentOS == 2:
            print(
                "Your OS, Darwin (AKA: macOS or Mac OS X), is currently not supported. Exiting gracefully...")
            self.vars.utils.LOG_ERROR(
                "Your OS, Darwin (AKA: macOS or Mac OS X), is currently not supported. Exiting gracefully...")
            sleep(5)
            exit(1)
        print(self.update_frequency)
        self.processRedditFeed(self.feed + self.update_frequency)
        self.make_polly_file(os.getcwd())
        self.create_rss_feed()


if __name__ == "__main__":
    sbs = SBS()
    sbs.main()

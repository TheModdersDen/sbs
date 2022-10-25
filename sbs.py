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
from profanity_filter.types_ import AnalysisType
import random

from sbs_vars import SBS_vars
from utils import Utils

class SBS():

    vars = SBS_vars()

    def is_root():
        return os.getuid() == 0

    feed = "https://reddit.com/r/showerthoughts/top.rss?t="
    env_vars_dict = {}
    vars_list = {}
    utils = Utils()

    thought_file = f"thoughts" + os.path.sep +f"thoughts-{vars.currentDate}--{vars.current_time}.txt"
    thoughts_data = None
    badwords_list = []
    
    # Checks to see if the program is running as Admin/root. If not, elevate the program so it is.
    if is_root() == False:
        elevate()
    else:
        utils.LOG_DEBUG(
            "Process is running as administrator/root. No need to elevate.")

        # Define some local variables and point them to the ones in the variables file.
        main_url = vars.main_url
        out_dir = vars.tts_out_dir
        out_file = vars.out_file
        feed_dir = vars.rss_out_dir
        update_frequency = vars.update_frequency

    # Check to see if a certain word, phrase, or even paragraph is profane. 
    # This has the capability to do deep-learning profanity checking as well.
    def isProfane(self, input):
        with open(os.getcwd() + os.path.sep + "data" + os.path.sep +"badwords.txt", "r+") as badwords_file:
            badwords = badwords_file.readlines()
            for word in badwords:
                word = word.strip("\n")
                self.badwords_list.append(word)
        if self.getCurrentOS() != 0:
            return (
                predict_prob([input]) >= [0.1]
                or predict([input]) == [1]
                or word.lower() in [input]
            )
        from profanity_filter.profanity_filter import ProfanityFilter
        from profanity_filter.config import Config
        pf = ProfanityFilter()
        pf.config = Config(
            analyses=[AnalysisType.DEEP],
            languages=['en_core_web_sm'],
        )
        pf.extra_profane_word_dictionaries={"en_core_web_sm": set(self.badwords_list)}

        return (
        predict_prob([input]) >= [0.1]
        or predict([input]) == [1]
        or word.lower() in [input]
        or pf.is_profane(input)
        )

    # Get the current OS type and send it back as an integer.
    def getCurrentOS(self):
        if platform.system() == "Linux":
            return 0  # Linux
        elif platform.system() == "Windows":
            return 1  # Windows
        elif platform.system() == "Darwin":
            return 2  # macOS

    # Proccess the /r/ShowerThoughts reddit RSS feed.
    def processRedditFeed(self, update_frequency):
        break_words = [" posted ", " said ", " thought ", " stated ", " remarked ", " commented "]
        
        # sourcery skip: hoist-statement-from-if
        if self.update_frequency not in ["day", "hour"]:
            raise Exception(
                "Please put in either 'day' or 'hour' as a timeframe for the Reddit feed.")
        d = feedparser.parse(
            "https://reddit.com/r/showerthoughts/top.rss?t=" + update_frequency)
        post_index = 0
        thoughts = ['ShowerThoughts Database File:',
                    f"{self.vars.currentDate}--{self.vars.current_time}"]
        for post in d.entries:
            post.author = str(post.author).strip("/u/").replace("_", "-")
            if self.isProfane(post.title) or self.isProfane(post.author):
                print(f"NOT ADDING: '{post.title}' as it is profane.")
                self.vars.utils.LOG_INFO(
                    f"NOT ADDING: '{post.title}' as it is profane.")
            else:
                post_index += 1
                print(f"ADDING: '{post.title}' by '{post.author}' as it is NOT profane.")
                self.vars.utils.LOG_INFO(
                    f"ADDING: '{post.title}' by '{post.author}' as it is NOT profane.")
                current_break_word = random.choice(break_words)
                if post_index < 10:
                    self.create_tts_file(
                        post.author + current_break_word + "'" + post.title + "'", os.getcwd(), f"polly_out0{post_index}.mp3")
                    thoughts.append(post.author + current_break_word + "'" + post.title + "'")
                else:
                    self.create_tts_file(
                        post.title, os.getcwd(), f"polly_out{post_index}.mp3")
                    thoughts.append(post.author + current_break_word + "'" + post.title + "'")
        post_index += 1
        self.create_tts_file(
            "That's all for today! Come back tomorrow for more ShowerThoughts.", os.getcwd(), f"polly_out{post_index}.mp3")
        thoughts.append(
            "That's all for today! Come back tomorrow for more ShowerThoughts.")
        self.vars.utils.create_file_from_path(os.getcwd() + os.path.sep + "/thoughts/")
        with open(self.thought_file, "w+") as thought_file:
            for thought in thoughts:
                thought_file.write(thought + "\n")

    # Create a text-to-speech file.
    def create_tts_file(self, data, out_dir_var,  out_file_name):
        polly_command = f'cd {out_dir_var} && sudo aws polly synthesize-speech --text-type ssml --output-format "mp3" --voice-id "Joanna" --engine neural --text "<speak><amazon:domain name=\\"news\\">{data}<break time= \\"1s\\"/></amazon:domain></speak>" {out_file_name}'
        print(polly_command)
        os.system(polly_command)

    # Make a singular file, which is a combination of all the TTS files generated above.
    def make_polly_file(self):
        tts_files = sorted(filter(os.path.isfile, glob.glob(
            os.getcwd() + os.path.sep + '*.mp3', recursive=False)))
        file_names = "".join(f" {tts_file}" for tts_file in tts_files)
        file_names = file_names[1:]
        merge_command = f"cat {file_names} >polly_output{self.vars.currentId}.mp3"
        os.system(merge_command)
        self.vars.utils.LOG_DEBUG("Running command: '" + merge_command + "'")
        file_names = ""
        for tts_file in tts_files:
            if tts_file not in ["_intro.mp3", "z_outro.mp3"]:
                file_names += f" {tts_file}"
        cleanup_command = f"rm {file_names}"
        os.system(cleanup_command)
        self.vars.utils.LOG_DEBUG("Running command: '" + cleanup_command + "'")

        move_command = f"mv polly_output{self.vars.currentId}.mp3 {self.vars.tts_out_dir}"
        self.vars.utils.LOG_DEBUG("Running command: '" + move_command + "'")
        os.system(move_command)

    # Generate an RSS feed to be read by ALEXA.
    def create_rss_feed(self):
        test_feed = Rss201rev2Feed(
            title="ShowerThoughts Briefing Feed",
            link=self.vars.main_url + "st-test.xml",
            description=self.vars.feed_description,
            ttl=60,
            language="en")

        tts_filesize = self.vars.utils.get_file_size(
            self.vars.tts_out_dir + self.vars.out_file)

        test_feed.add_item(
            unique_id=self.vars.URN_UUID,
            title=self.vars.feed_title,
            description=self.vars.feed_description,
            link=self.vars.feed_link,
            pubdate=datetime.datetime.utcnow(),
            enclosure=Enclosure(str(self.vars.feed_link),
                                str(tts_filesize), "audio/mpeg")
        )

        with codecs.open(f"{self.vars.rss_out_dir}st-test.xml", "w", encoding=self.vars.encoding_type) as rss_feed:
            rss_feed.truncate()
            rss_feed.write(test_feed.writeString(self.vars.encoding_type))
            rss_feed.close()

    # The main function.
    def main(self):
        #version_URL = urllib.request.Request(f"{self.vars.version_check_url}ST_VERSION")
        #with urllib.request.urlopen(version_URL) as response:
            #page_data = response.read()
            #sbs_ver = page_data.decode()
            #sbs_ver = sbs_ver.strip("\n")
        #self.utils.LOG_INFO(f"Starting SBS v{sbs_ver}... Please wait.")
        currentOS = self.getCurrentOS()
        self.utils.LOG_INFO(f"Current OS type is: '{platform.system()}.'")
        if currentOS == 0:
            self.utils.LOG_DEBUG(f"You are running {self.utils.distro} v{self.utils.distro_version}.")
            if self.utils.distro.lower() in ["Ubuntu".lower(), "Debian".lower(), "Kali".lower(), "Raspbian".lower()]:  
                self.utils.create_file_from_path(
                    self.vars.tts_out_dir
                )
                self.utils.create_file_from_path(
                    self.vars.rss_out_dir
                )
            else:
                self.utils.LOG_ERROR("You are running on an unsupported Linux Distro. Please install either Debian or Ubuntu and try again.")
        elif currentOS == 1:
            self.utils.LOG_WARN("NOTE: While Windows is supported, Linux is HIGHLY recommended due to a stronger profanity filter being possible to be used.\nHowever, this program will proceed anyway...")
            
            if self.utils.windows_version > 10:
                self.utils.create_file_from_path(
                    self.vars.tts_out_dir
                )
                self.utils.create_file_from_path(
                        self.vars.rss_out_dir
                )
            else:
                self._finish_and_exit_neatly(f"Your Windows version, v{self.utils.windows_version}, is not supported by this program.\nPlease either update your copy of Windows, run a Linux VM, or install Linux on your PC or a Raspberry Pi-like device.")

        elif currentOS == 2:
            self._finish_and_exit_neatly(
                "Your OS, Darwin (AKA: macOS or Mac OS X), is currently not supported. Exiting gracefully..."
            )

        self.utils.LOG_DEBUG(f"Current update_frequency: '{self.update_frequency}'.")
        self.processRedditFeed(self.feed + self.update_frequency)
        self.make_polly_file()
        self.create_rss_feed()

    # Finish and exit with a nice message is the OS is not supported.
    def _finish_and_exit_neatly(self, message):
        print(message)
        self.utils.LOG_ERROR(message)
        sleep(5)
        exit(1) # Generic exit error.


if __name__ == "__main__":
    sbs = SBS()
    sbs.main()

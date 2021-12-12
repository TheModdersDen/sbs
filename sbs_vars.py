import os
import platform
from utils import Utils
from uuid import uuid4
import datetime
from dotenv import load_dotenv

class SBS_vars():
    utils = Utils()
    # MAIN_URL=https://treasurevalley.tech/
    # TTS_MAIN_URL=https://treasurevalley.tech/st/
    # REFRESH_RATE=day
    # WEB_ROOT_DIR=/var/www/html/st/
    # RSS_OUT_DIR=/var/www/html/st/
    # POLLY_OUT_DIR=/var/www/html/st/polly_out/
    
    # Initialize local variables.
    def __init__(self):
        self.createEnvVars()
        load_dotenv()
        self.main_url = os.getenv("MAIN_URL")
        if self.main_url.endswith("/") == False:
            self.main_url += "/"
        self.version_check_url = os.getenv("VERSION_URL")
        if self.version_check_url.endswith("/") == False:
            self.version_check_url += "/"
        self.tts_main_url = os.getenv("TTS_MAIN_URL")
        if self.tts_main_url.endswith("/") == False:
            self.tts_main_url += "/"
        self.rss_main_url = os.getenv("RSS_MAIN_URL")
        if self.rss_main_url.endswith("/") == False:
            self.rss_main_url += "/"
        self.update_frequency = os.getenv("REFRESH_RATE")
        if self.getCurrentOS() != 0:
            raise Exception("Uh, oh! You are not running a supported OS with a supported web server. This program will likely crash now...")     

        self.rss_out_dir = "/var/www/html/" + "/".join(self.rss_main_url.split("/")[3:])
        self.tts_out_dir = "/var/www/html/" +  "/".join(self.tts_main_url.split("/")[3:])
        print(f"OUT DIRS ARE: {self.tts_out_dir} and {self.rss_out_dir}")
        self.uuid = uuid4()
        self.currentId = str(self.uuid)
        self.URN_UUID = self.uuid.urn
        self.encoding_type = "utf-8"
        self.dt = datetime.date.today()
        self.now = datetime.datetime.now()
        self.current_time = self.now.strftime("%H:%M:%S")
        self.currentDate = self.dt.isoformat()
        self.utils.LOG_DEBUG(
            f"The current date and time is: '{self.currentDate}--{self.current_time}.'")
        self.out_file = f"polly_output{self.currentId}.mp3"
        self.feed_title = f"Your ShowerThoughts Update ({self.currentDate}--{self.current_time})"
        self.feed_link = self.rss_main_url + f"polly_output{self.currentId}.mp3"

        self.feed_description = "This is an expiremental feed to use Amazon Polly to read the ShowerThoughts Reddit page to end users."

    # Get the current OS type and send it back as an integer.
    def getCurrentOS(self):
        if platform.system() == "Linux":
            return 0  # Linux
        elif platform.system() == "Windows":
            return 1  # Windows
        elif platform.system() == "Darwin":
            return 2  # macOS

    # Create the needed environment variables.
    def createEnvVars(self):
        if os.path.isfile(".env") == False or self.utils.is_file_empty(".env"):
            with open(".env", "w+") as env_file:
                self.ask_for_input(env_file)
            self.utils.LOG_DEBUG("Done writing program environment variables.")
        elif self.utils.is_file_empty(".env") == False or os.path.exists(".env") == True:
            self.utils.LOG_DEBUG("'.env' file exists. Continuing...")
    
    # Ask for the user's input for the "secret" variables, so that they can be stored privately.
    def ask_for_input(self, env_file):
        url_input=str(input(
            "What is the 'main' or 'base' URL of the site where the RSS feed and TTS files are stored. Example: 'https://example.com/'? (A full URL w/o quotes): "))
        if url_input is None:
            raise Exception(
                "Please put a valid URL as the 'MAIN_URL' input.\nRun this program to try again.")
        self.utils.LOG_DEBUG(
            f"Writing '{url_input}' as the 'MAIN_URL' variable.")
        env_file.write(f"MAIN_URL={url_input}\n")
        output_dir=str(input(
            "What is the URL where the text-to-speech files will be stored? (example: 'https://example.com/st/tts/', w/o quotes): "))
        if output_dir is None:
            raise Exception(
                "Please make that the 'TTS_MAIN_URL' input is a valid URL without quotes.\nRun this program to try again.")
        self.utils.LOG_DEBUG(
            f"Writing '{output_dir}' as the 'TTS_MAIN_URL' variable.")
        env_file.write(f"TTS_MAIN_URL={output_dir}\n")
        feed_dir=str(input(
            "What is the URL path where the RSS feed will be stored (not the direct path to the RSS feed)?: "))
        if feed_dir is None:
            raise Exception(
                "Please make that the 'RSS_MAIN_URL' input is a valid URL without quotes.\nRun this program to try again.")
        self.utils.LOG_DEBUG(
            f"Writing '{feed_dir}' as the 'RSS_MAIN_URL' variable.")
        env_file.write(f"RSS_MAIN_URL={feed_dir}\n")
        refresh_rate=str(input(
            "How often would you like the feed to be updated? NOTE: The more the feed is updated, the more strain will be put on your system (day/hour): "))
        if refresh_rate not in {"hour", "day"}:
            raise Exception(
                "Please make that the 'REFRESH_RATE' input is set to either 'day' or 'hour'.\nRun this program to try again.")
        self.utils.LOG_DEBUG(
            f"Writing '{refresh_rate}' as the 'REFRESH_RATE' variable.")
        env_file.write(f"REFRESH_RATE={refresh_rate}\n")
        version_url = str(input("What is the URL path that this program should check for a version from (example: https://example.com/st/)?: "))
        if version_url is None:
            raise Exception(
                "Please make that the 'VERSION_URL' input is set to a valid URL.\nRun this program to try again.")
        self.utils.LOG_DEBUG(
            f"Writing '{version_url}' as the 'VERSION_URL' variable.")
        env_file.write(f"VERSION_URL={version_url}\n")

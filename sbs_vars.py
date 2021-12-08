import os
from utils import Utils
from uuid import uuid4
import datetime
from decouple import config

class SBS_vars():
    utils = Utils()
    
    # Initialize local variables.
    def __init__(self):
        self.createEnvVars()
        self.main_url = config("TTS_MAIN_URL")
        self.out_dir = config("TTS_OUT_DIR")
        self.feed_dir = config("FEED_DIR")
        self.update_frequency = config("REFRESH_RATE")
        self.feed_link_extension = config("FEED_LINK_EXT")
        self.web_root_dir = config("WEB_ROOT_EXT")
        
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
        self.feed_link = (
            self.main_url +
            self.feed_link_extension
            + '/polly_output{self.currentId}.mp3'
        )

        self.feed_description = "This is an expiremental feed to use Amazon Polly to read the ShowerThoughts Reddit page to end users."

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
            "What is the main URL which will be read by the Alexa Skill? (A full URL w/o quotes): "))
        if url_input is None:
            raise Exception(
                "Please put a valid URL as the 'TTS_MAIN_URL' input.\nRun this program to try again.")
        self.utils.LOG_DEBUG(
            f"Writing '{url_input}' as the 'TTS_MAIN_URL' variable.")
        env_file.write(f"TTS_MAIN_URL={url_input}\n")
        output_dir=str(input(
            "Where would you like the final output of the ShowerThoughts text-to-speech '.mp3' file to be stored? (example: /var/www/html/tts-out/): "))
        if output_dir is None:
            raise Exception(
                "Please make that the 'TTS_OUT_DIR' input is a string/path.\nRun this program to try again.")
        self.utils.LOG_DEBUG(
            f"Writing '{output_dir}' as the 'TTS_OUT_DIR' variable.")
        env_file.write(f"TTS_OUT_DIR={output_dir}\n")
        feed_dir=str(input(
            "Where would you like the final output of the ShowerThoughts RSS '.xml' feed file to be stored? (example: /var/www/html/rss/): "))
        if feed_dir is None:
            raise Exception(
                "Please make that the 'FEED_DIR' input is a string/path.\nRun this program to try again.")
        self.utils.LOG_DEBUG(
            f"Writing '{feed_dir}' as the 'FEED_DIR' variable.")
        env_file.write(f"FEED_DIR={feed_dir}\n")
        refresh_rate=str(input(
            "How often would you like the feed to be updated? NOTE: The more the feed is updated, the more strain will be put on your system (day/hour): "))
        if refresh_rate not in {"hour", "day"}:
            raise Exception(
                "Please make that the 'REFRESH_RATE' input is set to either 'day' or 'hour'.\nRun this program to try again.")
        self.utils.LOG_DEBUG(
            f"Writing '{refresh_rate}' as the 'REFRESH_RATE' variable.")
        env_file.write(f"REFRESH_RATE={refresh_rate}\n")
        feed_link_extension=str(input(
            "What is the path (after the MAIN_URL) in which the Text-to-Speech files will be stored on the web server? (An example would be 'st/out', w/o quotes): "))
        if feed_link_extension is None:
            raise Exception(
                "Please make that the 'FEED_LINK_EXT' input is a valid URL path that leads to the folder with the TTS files folder.\nRun this program to try again.")
        self.utils.LOG_DEBUG(
            f"Writing '{feed_link_extension}' as the 'FEED_LINK_EXT' variable.")
        env_file.write(f"FEED_LINK_EXT={feed_link_extension}\n")
        web_root_dir=str(input(
            "What is the path of your webserver in which you will be hosting the ShowerThoughts TTS files and RSS feed? (example: /var/www/html/): "))
        if web_root_dir is None:
            raise Exception(
                "Please make that the 'WEB_ROOT_EXT' input is a valid path that leads to the base/root folder with the files for the SBS program will be hosted.\nRun this program to try again.")
        self.utils.LOG_DEBUG(
            f"Writing '{web_root_dir}' as the 'WEB_ROOT_EXT' variable.")
        env_file.write(f"WEB_ROOT_EXT={web_root_dir}\n")

from distutils import util
import os
from utils import Utils
from uuid import uuid4
import datetime
from decouple import config

class SBS_vars():
    utils = Utils()
    
    def __init__(self):
        self.createEnvVars()
        self.main_url = config("TTS_MAIN_URL")
        self.out_dir = config("TTS_OUT_DIR")
        self.feed_dir = config("FEED_DIR")
        self.update_frequency = config("REFRESH_RATE")

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
        self.feed_link = self.main_url + f"polly_out/polly_output{self.currentId}.mp3"
        self.feed_description = "This is an expiremental feed to use Amazon Polly to read the ShowerThoughts Reddit page to end users."

    def createEnvVars(self):
        if os.path.isfile(f"{os.getcwd()}/.env") == False or self.utils.is_file_empty(f"{os.getcwd()}/.env"):
            with open(f"{os.getcwd()}/.env", "w+") as env_file:
                self._extracted_from_createEnvVars_4(env_file)
            self.utils.LOG_DEBUG("Done writing program environment variables.")
        elif self.utils.is_file_empty(f"{os.getcwd()}/.env") == False or os.path.exists(f"{os.getcwd()}/.env") == True:
            self.utils.LOG_DEBUG("'.env' file exists. Continuing...")

    # TODO Rename this here and in `createEnvVars`
    def _extracted_from_createEnvVars_4(self, env_file):
        url_input=str(input(
            "What is the main URL which will be read by the Alexa Skill? (A full URL w/o quotes): "))
        if url_input is None:
            raise Exception(
                "Please put a valid URL as the 'TTS_MAIN_URL' input.\nRun this program to try again.")
        self.utils.LOG_DEBUG(
            f"Writing '{url_input}' as the 'TTS_MAIN_URL' variable.")
        env_file.write(f"TTS_MAIN_URL={url_input}\n")
        output_dir=str(input(
            "Where would you like the final output of the ShowerThoughts text-to-speech '.mp3' file to be stored? (example: /var/www/html/): "))
        if output_dir is None:
            raise Exception(
                "Please make that the 'TTS_OUT_DIR' input is a string/path.\nRun this program to try again.")
        self.utils.LOG_DEBUG(
            f"Writing '{output_dir}' as the 'TTS_OUT_DIR' variable.")
        env_file.write(f"TTS_OUT_DIR={output_dir}\n")
        feed_dir=str(input(
            "Where would you like the final output of the ShowerThoughts RSS '.xml' feed file to be stored? (example: /var/www/html/): "))
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

from distutils import util
import os
from utils import Utils
from uuid import uuid4
import datetime
from decouple import config

class SBS_vars():
    utils = Utils()

    try:

        main_url = config("MAIN_URL")
        out_dir = config("OUT_DIR")
        feed_dir = config("FEED_DIR")
        update_frequency = config("REFRESH_RATE")
        uuid = uuid4()
        currentId = str(uuid)
        URN_UUID = uuid.urn
        encoding_type = "utf-8"
        dt = datetime.date.today()
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        currentDate = dt.isoformat()
        utils.LOG_DEBUG(f"The current date and time is: '{currentDate}--{current_time}.'")
        out_file = f"polly_output{currentId}.mp3"
        feed_title = f"Your ShowerThoughts Update ({currentDate}--{current_time})"
        feed_link = main_url + f"polly_out/polly_output{currentId}.mp3"
        feed_description = "This is an expiremental feed to use Amazon Polly to read the ShowerThoughts Reddit page to end users."
    except {Exception} as error:
        print(f"ERROR: {error}")
        utils.LOG_DEBUG(f"ERROR: {error}")

    def createEnvVars(self):
        if os.path.isfile(f"{os.getcwd()}/.env") == False or self.utils.is_file_empty(f"{os.getcwd()}/.env"):
            env_file = open(f"{os.getcwd()}/.env", "w+")
            url_input = str(input(
                "What is the main URL which will be read by the Alexa Skill? (A full URL w/o quotes): "))
            if url_input == None:
                raise Exception(
                    "Please put a valid URL as the MAIN_URL input.\nRun this program to try again.")
            else:
                self.utils.LOG_DEBUG(
                    f"Writing '{url_input}' as the MAIN_URL variable.")
                env_file.write(f"MAIN_URL={url_input}\n")
            output_dir = str(input(
                "Where would you like the final output of the ShowerThoughts text-to-speech '.mp3' file to be stored? (example: /var/www/html/): "))
            if output_dir == None:
                raise Exception(
                    "Please make that the 'output_dir' input is a string/path.\nRun this program to try again.")
            else:
                self.utils.LOG_DEBUG(
                    f"Writing '{output_dir}' as the OUT_DIR variable.")
                env_file.write(f"OUT_DIR={output_dir}\n")
            feed_dir = str(input(
                "Where would you like the final output of the ShowerThoughts RSS '.xml' feed file to be stored? (example: /var/www/html/): "))
            if feed_dir == None:
                raise Exception(
                    "Please make that the 'feed_dir' input is a string/path.\nRun this program to try again.")
            else:
                self.utils.LOG_DEBUG(
                    f"Writing '{feed_dir}' as the OUT_DIR variable.")
                env_file.write(f"FEED_DIR={feed_dir}\n")
            refresh_rate = str(input(
                "How often would you like the feed to be updated? NOTE: The more the feed is updated, the more strain will be put on your system (day/hour): "))
            if refresh_rate not in ["hour", "day"]:
                raise Exception(
                    "Please make that the 'refresh_rate' input is set to either 'day' or 'hour'.\nRun this program to try again.")
            else:
                self.utils.LOG_DEBUG(
                    f"Writing '{refresh_rate}' as the OUT_DIR variable.")
                env_file.write(f"REFRESH_RATE={refresh_rate}\n")
            env_file.close()
            self.utils.LOG_DEBUG("Done writing program environment variables.")
        elif self.utils.is_file_empty(f"{os.getcwd()}/.env") == False or os.path.exists(f"{os.getcwd()}/.env") == True:
            self.utils.LOG_DEBUG("'.env' file exists. Continuing...")

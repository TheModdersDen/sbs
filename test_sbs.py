import pytest
import os
import glob

from sbs import SBS
from sbs_vars import SBS_vars
from utils import Utils

# Check to see if the profanity filter is working with the current wordset.
def test_isProfane():
    thought_files = sorted(filter(os.path.isfile, glob.glob(os.getcwd() + '/thoughts/*.txt', recursive=False)))
    badwords_list = []
    with open("data/badwords.txt", "r+") as badwords_file:
        badwords = badwords_file.readlines()
        for word in badwords:
            word = word.strip("\n")
            badwords_list.append(word)
            
        with open(thought_files[0], "r+") as thought_file:
            for line in thought_file:
                clean_line = line.strip()
                
                assert(word.lower() not in clean_line) == True

# Check to see if the program is running as root/admin.
def test_is_root():
    assert(SBS.is_root()) == SBS.is_root()

# Check to see if one of the TTS files generated does not equal 0 in filesize.
def test_is_file_empty():
    utils = Utils()
    assert(utils.is_file_empty(SBS.out_dir + SBS.out_file)) == False

# Check to see if the thoughts file begins with the correct phrase.
def test_processRedditFeed():
    pass

# Call the main function that is part of pytest so that
# the test functions in this file will start executing.
pytest.main(["-v", "--tb=line", "-rN", __file__])
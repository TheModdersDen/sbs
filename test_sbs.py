import pytest
import os
import glob

from sbs import SBS

# Check to see if the profanity filter is working with the current wordset.
def test_isProfane():
    thought_files = sorted(filter(os.path.isfile, glob.glob(os.getcwd() + '/thoughts/*.txt', recursive=False)))
    badwords_list = SBS.badwords_list     
    with open(thought_files[0], "r+") as thought_file:
        for word, line in zip(badwords_list, thought_file):
            clean_line = line.strip()
                
            assert(word.lower() not in clean_line) == True

# Check to see if the program is running as root/admin.
def test_is_root():
    assert(SBS.is_root()) == bool(os.getuid() == 0)

# Check to see if the thoughts file begins with the correct phrase.
def test_processRedditFeed():
    thought_files = sorted(filter(os.path.isfile, glob.glob(os.getcwd() + '/thoughts/*.txt', recursive=False)))
    with open(thought_files[0], "r+") as thought_file:
        for lines in thought_file.readlines():
            clean_lines = lines.strip()
        assert(clean_lines) == "That's all for today! Come back tomorrow for more ShowerThoughts."

# Call the main function that is part of pytest so that
# the test functions in this file will start executing.
pytest.main(["-v", "--tb=line", "-rN", __file__])
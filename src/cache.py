import os
import hashlib
import json
from util import *

def clear_noun_lists():
    dirPath = construct_noun_list_dir_path()
    os.rmdir(dirPath)

def clear_noun_declinations():
    dirPath = construct_decline_dir_path()
    os.rmdir(dirPath)

def clear_vocab_lists():
    for i in range(1, 41):
        if os.path.isfile(construct_vocab_list_path(i)):
            os.remove(construct_vocab_list_path(i))
        if os.path.isfile(construct_vocab_test_path(i, 'latin')):
            os.remove(construct_vocab_test_path(i, 'latin'))
        if os.path.isfile(construct_vocab_test_path(i, 'english')):
            os.remove(construct_vocab_test_path(i, 'english'))

def clear_cache():
    clear_vocab_lists()
    clear_noun_declinations()
    clear_noun_lists()

def db_is_changed():
    # Read hash value
    with open(dbhashPath, "r", encoding="utf-8") as json_file:
        db = json.load(json_file)
    # Convert newly created hash to text
    checksum = hashlib.md5(open(databasePath).read().encode('utf-8')).hexdigest()
    if db['hash'] != checksum:
        db['hash'] = checksum
        with open(dbhashPath, "w", encoding="utf-8") as json_file:
            json.dump(db, json_file)
        return True
    return False
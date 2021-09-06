import os
import hashlib
import json
from util import databasePath

def clear_lists():
    for i in range(1, 41):
        if os.path.isfile(f'../vocab-lists/{i}/ch{i}-vocab-extended-list.txt'):
            os.remove(f'../vocab-lists/{i}/ch{i}-vocab-extended-list.txt')
        if os.path.isfile(f'../vocab-lists/{i}/ch{i}-vocab-list.txt'):
            os.remove(f'../vocab-lists/{i}/ch{i}-vocab-list.txt')
        if os.path.isfile(f'../vocab-lists/{i}/ch{i}-vocab-test-english.txt'):
            os.remove(f'../vocab-lists/{i}/ch{i}-vocab-test-english.txt')
        if os.path.isfile(f'../vocab-lists/{i}/ch{i}-vocab-test-latin.txt'):
            os.remove(f'../vocab-lists/{i}/ch{i}-vocab-test-latin.txt')

def db_is_changed():
    # Read hash value
    with open("../databases/dbhash.json", "r", encoding="utf-8") as json_file:
        db = json.load(json_file)
    # Convert newly created hash to text
    checksum = hashlib.md5(open(databasePath).read().encode('utf-8')).hexdigest()
    if db['hash'] != checksum:
        db['hash'] = checksum
        with open("../databases/dbhash.json", "w", encoding="utf-8") as json_file:
            json.dump(db, json_file)
        return True
    return False
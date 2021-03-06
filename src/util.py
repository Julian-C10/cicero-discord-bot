databasePath = "databases/database.json"
dbhashPath = "databases/dbhash.json"

latin_greeting = "Salve!"

languages = ['english', 'latin']

suggestions_channel_id = "884522427588177951"

suggest_error_message = f"If you think I should have understood the request you entered, let me know by posting it in <#{suggestions_channel_id}>!"

help_msg = """
Salvē! I will respond to the following messages:
    Cicero
    latin history [wheelock-wikipedia]
    vocab word your_word_here
    chapter [1-40] vocab word
    chapter [1-40] vocab word your_word_here
    chapter [1-40] vocab list
    chapter [1-40] vocab test [latin-english]
    chapter [1-40] exercises
    chapter [1-40] exercises key
    chapter [1-40] sentences
    decline noun
    noun list [1st-5th] declension
All translations and audio credited to http://wheelockslatin.com/
Try asking me something! (type "examples" if you want to see some examples)
"""

example_msg = """
The following messages are examples of requests I would respond to:
    cicero
    latin history wheelock
    vocab word hello
    chapter 1 vocab word
    chapter 1 vocab word please
    chapter 1 vocab list
    chapter 1 vocab test latin
    chapter 1 exercises
    chapter 1 exercises key
    chapter 1 sentences
"""

latin_history_wheelock = """
I. Archaic through Early Republican Period (`...80 BC`)
II. Late Republican and Augustan Period (`80 BC - 14 AD`)
    A. Ciceronian Period (`80 - 43 BC`)
    B. Augustan Period (`43 BC - 14 AD`)
III. Post-Augustan Period ("Silver Age" `14 - 138 AD`)
IV. Patristic Period (`late 2nd - 5th cent.`)
V. Medieval Period (`6th - 14th cent.`)
VI. Renaissance (`15th cent. - the Present`)
Sources:
    http://wheelockslatin.com/
"""

latin_history_wikipedia = """
I. Old Latin (`...75 BC`)
II. Classical Latin (`75 BC - 3rd Century AD`)
    A. Golden Age (`75 BC - 14 AD`)
    B. Silver Age (`14 AD - 3rd Century AD`)
III. Vulgar Latin / Late Latin (`3rd - 6th Century AD`)
IV. Ecclesiastical Latin (`4th Century AD - the Present`)
IV. Medieval Latin (`4th - 14th Century AD`)
V. Renaissance Latin (`14th - 15th Century AD`)
VI. New Latin (`16th - 19th Century AD`)
VII. Contemporary Latin (`19th Century AD - to the Present`)
Sources:
    https://en.wikipedia.org/wiki/History_of_Latin
    """

latin_history_error = f"""
Sorry, I don't understand. Did you mean one of the following?
    latin history wheelock
    latin history wikipedia
{suggest_error_message}
"""

standard_error_message = ("Sorry, it looks like I didn't get that to work yet. "
                         f"Please post a message in <#{suggestions_channel_id}> "
                          "that has the command you just tried to use so I can "
                          "fix that when I get a chance!")

def chapter_num_out_of_range_error(num):
    return f"Sorry, chapter {num} does not exist. The chapters range from 1 - 40."

def vocab_missing_command(num):
    return ("Sorry, I don't understand. Did you mean one of the following?\n"
           f"   chapter {num} vocab word\n"
           f"   chapter {num} vocab word your_word_here\n"
           f"   chapter {num} vocab list\n"
           f"   chapter {num} vocab test english\n"
           f"   chapter {num} vocab test latin\n") + suggest_error_message

def missing_specific_vocab_word_error(reconstructedMsg, num):
    return f'Sorry, I couldn\'t find a vocab entry containing "{reconstructedMsg}" in chapter {num}.\n' + suggest_error_message

def missing_specific_vocab_word_all_chapters_error(reconstructedMsg):
    return f'Sorry, I couldn\'t find a vocab entry containing "{reconstructedMsg}" in any chapter.\n' + suggest_error_message

def missing_noun_error(reconstructedMsg):
    return f'Sorry, I couldn\'t find a noun entry containing "{reconstructedMsg}".\n' + suggest_error_message

def unable_to_decline_noun_error(reconstructedMsg):
    return f'Sorry, I don\'t know how to decline "{reconstructedMsg}".\n' + suggest_error_message

def vocab_test_missing_command(num):
    return ("Sorry, I don't understand. Did you mean one of the following?\n"
           f"   chapter {num} vocab test english\n"
           f"   chapter {num} vocab test latin\n") + suggest_error_message

def construct_vocab_list_path(num):
    return f'vocab-lists/{num}/ch{num}-vocab-list.txt'

def construct_vocab_test_path(num, lang):
    return f'vocab-lists/{num}/ch{num}-vocab-test-{lang}.txt'

def construct_sound_path(num, filename):
    return f'sounds/{num}/vocabulary/{filename}'

def construct_vocab_path():
    return 'vocab-lists'

def construct_vocab_dir_path(num):
    return f'vocab-lists/{num}'

def construct_decline_dir_path():
    return f'noun-declensions'

def construct_noun_list_path(declension):
    file = ""
    if (declension == "1st Declension"):
        file = "first-decl-nouns.txt"
    elif (declension == "2nd Declension"):
        file = "second-decl-nouns.txt"
    elif (declension == "3rd Declension"):
        file = "third-decl-nouns.txt"
    elif (declension == "4th Declension"):
        file = "fourth-decl-nouns.txt"
    elif (declension == "5th Declension"):
        file = "fifth-decl-nouns.txt"
    elif (declension == ""):
        file = "all-nouns.txt"
    return f"noun-lists/{file}"

def construct_noun_list_dir_path():
    return f'noun-lists'

def construct_decline_path(latinText):
    firstWord = latinText.split(',')[0]
    return f'noun-declensions/{firstWord}.txt'

def longest_line_length_util(words, lang):
    maxLen = len(words[0][lang])
    for i in range(1, len(words)):
        if len(words[i][lang]) > maxLen:
            maxLen = len(words[i][lang])
    return maxLen

def list_string_format(maxLatinLen, latinText, englishText):
    i = 0
    msg = ''
    for c in latinText:
        msg += c
        i += 1
    while i < maxLatinLen:
        msg += ' '
        i += 1
    i = 0
    for c in englishText:
        msg += c
    msg += '\n'
    return msg
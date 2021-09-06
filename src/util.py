databasePath = "../databases/database.json"

latin_greeting = "Salve!"

help_msg = """
Commands you can use:
    chapter [1-40] vocab word (example: chapter 1 vocab word)
    chapter [1-40] vocab word <your-word> (example: chapter 1 vocab word hello)
    chapter [1-40] vocab list (example: chapter 1 vocab list)
    chapter [1-40] vocab test [latin-english] (example: chapter 1 vocab test latin)
    chapter [1-40] exercises (example: chapter 1 exercises)
    chapter [1-40] exercises key (example: chapter 1 exercises key)
    chapter [1-40] sentences (example: chapter 1 sentences)
All translations and audio credited to http://wheelockslatin.com/
"""

latin_history = """
I. Old Latin / Archaic Latin through Early Republican Period (`...80 BC`)
II. Classical Latin / Late Republican and Augustan Period ("Golden Age", `80 BC - 14 AD`)
    A. Ciceronian Period (`80 - 43 BC`)
    B. Augustan Period (`43 BC - 14 AD`)
III. Classical Latin / Post-Augustan Period ("Silver Age" `14 - 138 AD`)
IV. Patristic Period (`late 2nd - 5th cent.`)
V. Medieval Period (`6th - 14th cent.`)
VI. Renaissance (`15th cent.`) to present
Sources:
    http://wheelockslatin.com/
    https://en.wikipedia.org/wiki/History_of_Latin
    """

languages = ['english', 'latin']

suggestions_channel_id = "884522427588177951"

standard_error_message = ("Sorry, it looks like I didn't get that to work yet. "
                           f"Please post a message in <#{suggestions_channel_id}>"
                           "that has the command you just tried to use so I have"
                           " a reminder to fix that when I get a chance!")
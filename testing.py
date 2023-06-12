print(r"""
  _  __                                _ 
 | |/ /                               | |
 | ' / ___ _   ___      _____  _ __ __| |
 |  < / _ \ | | \ \ /\ / / _ \| '__/ _` |
 | . \  __/ |_| |\ V  V / (_) | | | (_| |
 |_|\_\___|\__, | \_/\_/ \___/|_|  \__,_|
     /\     __/ |     | |         (_)    
    /  \   |___/  __ _| |_   _ ___ _ ___ 
   / /\ \ | '_ \ / _` | | | | / __| / __|
  / ____ \| | | | (_| | | |_| \__ \ \__ \
 /_/    \_\_| |_|\__,_|_|\__, |___/_|___/
                          __/ |          
                         |___/           
""")


depth = 1000


import csv

rows = []
phrases_sorted = []
phrase_frequencies = {}
word_frequencies = {}

with open("keywords.csv", "r") as file:
    reader = csv.reader(file)

    header = reader.__next__()
    # print(header)
    assert header == ['Keyword', 'Traffic', 'Exact KW', 'abortion', 'clinic', 'near', 'Campaign', 'Ad Group', 'Group']

    previous_frequency = float("inf")
    for i in range(depth):
        row = reader.__next__()
        phrase = row[0]
        frequency = int(row[1])

        rows.append(row)
        phrases_sorted.append(phrase)
        phrase_frequencies[phrase] = frequency

        for w in phrase.split():
            if w in word_frequencies:
                word_frequencies[w] += frequency
            else:
                word_frequencies[w] = frequency


        # print(row)
        # print(row[:2])

        if f"[{phrase}]" != row[2]:
            print(f"WARNING: row {i}: {row}")

        assert frequency <= previous_frequency
        previous_frequency = frequency





working_keywords = []

# matching_phrases = None
# unique_phrase_matches = None
# total_phrase_matches = None
# phrase_frequencies = None
# word_frequency_pairs = None


# def update_filter():
matching_phrases = phrases_sorted
unique_phrase_matches = len(matching_phrases)

total_phrase_matches = 0
for k in matching_phrases:
    total_phrase_matches += phrase_frequencies[k]

word_frequency_pairs = sorted(
    word_frequencies.items(), key=lambda x:x[1], reverse=True
)

total_word_matches = sum(word_frequencies.values())






def help_message():
    print("How to use: type words to build a filter to search keywords")
    print("Special commands:")
    print("   to show this help message")
    print(" $ to exit")
    print(" ? to show top matching words")
    print(" + to save current working keywords")
    print(" / to review saved keywords")
    print(" < to remove the newest working keyword")
    print(" [ to clear working keywords")
    print("Normal usage:")
    print(" Type a word to add it to the filter")
    print(" Type a number, corresponding to a word to add it to the filter")

def show_matches():
    count = 30
    indent = len(str(count)) + 1
    for i in range(count):
        line = str(i+1)
        line += " " * (indent - len(line))
        line += word_frequency_pairs[i][0]
        line += f"  [{word_frequency_pairs[i][1]}]"
        print(line)

def add_keywords(keywords):
    keywords = keywords.split(" ")
    working_keywords.extend(keywords)



while True:
    print(f"WARNING: only using top {depth} keywords for simple proof of concept")
    print("For help, press ENTER")
    print(f"Working keywords: {working_keywords}")
    print(f"{unique_phrase_matches} matching unique phrases ({total_phrase_matches} hits)")
    ans = input("> ").strip()
    print()

    if ans == "":
        help_message()

    elif ans == "$":
        break
    elif ans == "?":
        show_matches()
    elif ans == "+":
        print("TODO")
    elif ans == "/":
        print("TODO")
    elif ans == "<":
        print("TODO")
    elif ans == "[":
        print("TODO")

    elif ans.isdigit():
        index = int(ans)
        if index < 1 or index > unique_phrase_matches:
            print(f"Index must be within 1 to {unique_phrase_matches}")
        else:
            print("TODO")
    
    # elif 

    else:
        print(f"Unrecognized input: '{ans}'")

    print()



print("TODO: save keywords to a file for reload")

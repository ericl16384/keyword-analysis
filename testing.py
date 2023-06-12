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


depth = 10000
show_matches_count = 30


import csv


def load_from_csv(filename, row_count):
    global phrases, keywords
    #, phrases_sorted, phrase_frequencies, word_frequencies
    phrases = []
    keywords = []
    # phrases_sorted = []
    # phrase_frequencies = {}
    # word_frequencies = {}

    with open(filename, "r") as file:
        reader = csv.reader(file)

        header = reader.__next__()
        assert header == ['Keyword', 'Traffic', 'Exact KW', 'abortion', 'clinic', 'near', 'Campaign', 'Ad Group', 'Group']

        for i in range(row_count):
            errors = 0

            try:
                row = reader.__next__()
            except UnicodeDecodeError:
                errors += 1
                continue

            words = row[0].split()

            try:
                count = int(row[1])
            except ValueError:
                errors += 1
                continue

            phrases.append((words, count))

def filter_by_keywords(keywords):
    if len(keywords) == 0:
        return

    global phrases
    new_phrases = []
    for phrase in phrases:
        words = phrase[0]
        for w in words:
            if w in keywords:
                new_phrases.append(phrase)
                break
    phrases = new_phrases

def count_words():
    global word_counts, total_hits
    word_counts = {}
    total_hits = 0

    for words, frequency in phrases:
        count = int(frequency)
        for w in words:
            if w in word_counts:
                word_counts[w] += count
            else:
                word_counts[w] = count
        total_hits += count

def sort_words():
    global sorted_words
    sorted_words = sorted(
        word_counts.items(), key=lambda x:x[1], reverse=True
    )

        




            # phrase = row[0]
            # frequency = int(row[1])

            # phrases.append(row)
            # phrases_sorted.append(phrase)
            # phrase_frequencies[phrase] = frequency

            # for w in phrase.split():
            #     if w in word_frequencies:
            #         word_frequencies[w] += frequency
            #     else:
            #         word_frequencies[w] = frequency


            # # print(row)
            # # print(row[:2])

            # # if f"[{phrase}]" != row[2]:
            # #     print(f"WARNING: row {i}: {row}")

            # assert frequency <= previous_frequency
            # previous_frequency = frequency





# working_keywords = []

# matching_phrases = None
# unique_phrase_matches = None
# total_phrase_matches = None
# phrase_frequencies = None
# word_frequency_pairs = None


# matching_phrases = phrases_sorted
# unique_phrase_matches = len(matching_phrases)

# total_phrase_matches = 0
# for k in matching_phrases:
#     total_phrase_matches += phrase_frequencies[k]

# word_frequency_pairs = sorted(
#     word_frequencies.items(), key=lambda x:x[1], reverse=True
# )

# total_word_matches = sum(word_frequencies.values())


# sorted_word_frequencies = sorted(word_frequencies)

# for w in sorted_word_frequencies:
#     print(w, word_frequencies[w])



# def update_filter(keyword):
#     global phrases
#     phrases = [i for i in filter(lambda r: keyword in r[0], phrases)]

#     global word_frequency_pairs
#     word_frequency_pairs = sorted(
#         word_frequencies.items(), key=lambda x:x[1], reverse=True
#     )

# working_keywords.append("baby")
# update_filter("baby")




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
    count = min(show_matches_count, len(sorted_words))

    rows = []
    for i in range(count):
        word, f = sorted_words[i]
        rows.append((str(i+1), word, str(f)))
    
    widths = [0, 0, 0]
    for row in rows:
        for i, item in enumerate(row):
            widths[i] = max(widths[i], len(item))
    
    for row in rows:
        line = ""
        for i, item in enumerate(row):
            if i == 2:
                line += " " * (widths[i] - len(item) + 1)
                line += item
            else:
                line += item
                line += " " * (widths[i] - len(item) + 1)
        # line += word
        # line += f"  [{f}]"
        print(line)

    #     second_indent = max(second_indent, len(line)+1)
    # first_indent = len(str(count)) + 1
    # second_indent = 0
    
    # lines = []
    # for i in range(len(lines)):
    #     lines[i] += " " * (second_indent - len(line))
    #     lines[i] += 

    # for l in lines:
    #     print(l)

# def add_keywords(keywords):
#     keywords = keywords.split(" ")
#     working_keywords.extend(keywords)





load_from_csv("keywords.csv", depth)
filter_by_keywords(keywords)
count_words()
sort_words()




while True:
    print(f"WARNING: only using top {depth} keywords for simple proof of concept")
    print("For help, press ENTER")
    print(f"Working keywords: {keywords}")
    print(f"{len(phrases)} matching unique phrases ({total_hits} hits)")
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
        # index = int(ans)
        # if index < 1 or index > unique_phrase_matches:
        #     print(f"Index must be within 1 to {unique_phrase_matches}")
        # else:
            print("TODO")
    
    # elif 

    else:
        print(f"Unrecognized input: '{ans}'")

    print()



print("TODO: save keywords to a file for reload")

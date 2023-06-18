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

import csv



depth = 10**9
display_count = 30
load_file = "keywords.csv"
keywords = []



def load_from_csv(filename, row_count):
    global phrase_counts, keywords, whole_file_read
    #, phrases_sorted, phrase_frequencies, word_frequencies
    phrase_counts = []
    # keywords = []
    # phrases_sorted = []
    # phrase_frequencies = {}
    # word_frequencies = {}

    whole_file_read = False

    errors = 0
    with open(filename, "r") as file:
        reader = csv.reader(file)

        header = reader.__next__()
        assert header == ['Keyword', 'Traffic', 'Exact KW', 'abortion', 'clinic', 'near', 'Campaign', 'Ad Group', 'Group']

        i = 0
        while i < row_count:
            try:
                row = reader.__next__()
            except StopIteration:
                whole_file_read = True
                break
            except UnicodeDecodeError:
                errors += 1
                continue

            words = row[0].split()

            if len(words) == 0:
                continue

            try:
                count = int(row[1])
            except ValueError:
                errors += 1
                continue

            phrase_counts.append((words, count))

            i += 1
    
    if not whole_file_read:
        print(f"WARNING: only using top {depth} keywords")
    
    if errors:
        print(f"{errors} erroneous lines found in '{filename}'")

    print(f"Read {i} lines from '{filename}'")
    

        

def filter_by_keywords():
    if len(keywords) == 0:
        return

    global phrase_counts
    new_phrases = []

    # print(phrase_counts)
    # print(keywords)

    # blocked_phrases = 0
    for phrase_count in phrase_counts:
        phrase, count = phrase_count
        keep = True
        for k in keywords:
            # print(phrase, k)
            if k not in phrase or k[0] == "!" and k[1:] in phrase:
                # blocked_phrases += 1
                # print(f"Ignoring '{phrase}'")
                keep = False
                break
            # if k in phrase:
            #     keep = True
            #     print(f"{k} in '{phrase}'")
        if keep:
            new_phrases.append(phrase_count)
            # print(f"Keeping '{phrase}'")
            # print(phrase)
    # print(new_phrases)
    phrase_counts = new_phrases

    # print(phrase_counts)
    # assert False
    # input()

def count_words():
    global word_counts, total_hits
    word_counts = {}
    total_hits = 0

    # print(phrase_counts[0])
    for words, frequency in phrase_counts:
        count = int(frequency)
        for w in words:
            assert isinstance(w, str)
            assert isinstance(count, int)
            if w in word_counts:
                word_counts[w] += count
            else:
                word_counts[w] = count
                # print(w)
        total_hits += count

def find_display_words():
    global display_words
    display_words = []


    while len(display_words) < display_count:
        max_count = 0
        max_word = None

        for word, count in word_counts.items():
            if count <= max_count:
                continue
            if word in keywords:
                continue
            if word in display_words:
                continue
            max_count = count
            max_word = word
        
        if max_word == None:
            break

        display_words.append(max_word)

def add_keyword_from_display_words(rank, negate=False):
    rank = int(rank)
    if rank < 1 or rank > len(display_words):
        print(f"Number must be within 1 to {len(display_words)}")
    else:
        index = rank - 1
        keyword = display_words[index]
        if negate:
            keyword = "!" + keyword
        # print(keywords)
        keywords.append(keyword)
        # print(keywords)
        print(f"Added keyword: '{keyword}'")
        filter_by_keywords()
        count_words()
        find_display_words()
        print()
        show_matches()







def reload():
    print(f"Loading from {load_file}")
    load_from_csv(load_file, depth)
    filter_by_keywords()
    count_words()
    find_display_words()

def save_searches():
    filename = "SAVEFILE " + " ".join(keywords)
    filename += ".csv"
    print(f"saving to '{filename}'")

    header = ["Keyword", "Frequency"]
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for phrase, count in phrase_counts:
            writer.writerow((" ".join(phrase), count))


            


def help_message():
    print("Normal usage:")
    # print(" Type a word to add it to the filter")
    print("  Type a number, corresponding to a word to add it to the filter")
    print("  Type a ! before the number, to disallow that word")
    print("Special commands:")
    print("    to show this help message")
    print("  $ to exit program")
    print("  ? to show top matching words")
    print("  + to save current working keywords")
    # print("  / to review saved keywords")
    print("  < to remove the newest working keyword")
    print("  [ to clear working keywords")

def show_matches():
    if len(display_words) == 0:
        print("No new words found using current keywords")

    rows = []
    for i, word in enumerate(display_words):
        try:
            rows.append((str(i+1), word, str(word_counts[word])))
        except:
            print("ERROR")
            print(str(i+1), word)
    
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
        print(line)




reload()
print()

while True:
    print("For help, press ENTER")
    print(f"Working keywords: {keywords}")
    print(f"{len(phrase_counts)} matching unique phrases ({total_hits} hits)")
    try:
        ans = input("> ")
    except EOFError as err:
        print()
        print("Error in input. Please try again.")
        print()
        continue
    ans = ans.strip()
    print()

    if ans == "":
        help_message()

    elif ans == "$":
        break
    elif ans == "?":
        show_matches()
    elif ans == "+":
        if len(keywords) == 0:
            print("Before saving, you must select at least one keyword")
        else:
            save_searches()
    # elif ans == "/":
    #     print("TODO")
    elif ans == "<":
        if len(keywords) == 0:
            print("Keyword list already empty")
        else:
            print(f"Removed '{keywords.pop()}' from keywords")
            reload()
            print()
            show_matches()
    elif ans == "[":
        if len(keywords) == 0:
            print("Keyword list already empty")
        else:
            for k in keywords:
                print(f"Removed '{k}' from keywords")
        keywords = []
        reload()
        print()
        show_matches()

    elif ans.isdigit():
        add_keyword_from_display_words(ans)
    
    elif ans[0] == "!" and ans[1:].isdigit():
        print("TODO")
        # rank = ans[1:]
        # add_keyword_from_display_words(rank, True)

    else:
        print(f"Unrecognized input: '{ans}'")

    print()

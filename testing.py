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


depth = 1000000000 #10**6
display_count = 30
current_file = "keywords.csv"
keywords = []


import csv


def load_from_csv(filename, row_count):
    global phrases, keywords, whole_file_read
    #, phrases_sorted, phrase_frequencies, word_frequencies
    phrases = []
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

            phrases.append((words, count))

            i += 1
    
    if not whole_file_read:
        print(f"WARNING: only using top {depth} keywords")
    
    if errors:
        print(f"{errors} erroneous lines found in {filename}")

    print(f"Read {i} lines from {filename}")
    

        

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

def find_important_words():
    global display_words
    display_words = []


    while len(display_words) <= display_count:
        # if word[0] not in keywords:
        #     display_words.append(word)

        max_count = 0
        max_word = None

        for word, count in word_counts.items():
            if count > max_count and word not in display_words:
                max_count = count
                max_word = word

        display_words.append(max_word)

        




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
    print("Normal usage:")
    # print(" Type a word to add it to the filter")
    print(" Type a number, corresponding to a word to add it to the filter")
    print("Special commands:")
    print("   to show this help message")
    print(" $ to exit")
    print(" ? to show top matching words")
    # print(" + to save current working keywords")
    # print(" / to review saved keywords")
    print(" < to remove the newest working keyword")
    print(" [ to clear working keywords")

def show_matches():
    count = min(display_count, len(display_words))

    rows = []
    for i in range(count):
        word = display_words[i]
        rows.append((str(i+1), word, str(word_counts[word])))
    
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




def reload():
    print(f"Loading from {current_file}")
    load_from_csv(current_file, depth)
    filter_by_keywords(keywords)
    count_words()
    find_important_words()

reload()
print()




while True:
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
        if len(keywords) == 0:
            print("Keyword list already empty")
        else:
            print(f"Removed '{keywords.pop()}' from keywords")
            reload()
            print()
            show_matches()
    elif ans == "[":
        for k in keywords:
            print(f"Removed '{k}' from keywords")
        keywords = []
        reload()
        print()
        show_matches()

    elif ans.isdigit():
        index = int(ans)
        if index < 1 or index > len(display_words):
            print(f"Index must be within 1 to {len(display_words)}")
        else:
            keyword = display_words[index-1]
            keywords.append(keyword)
            filter_by_keywords(keyword)
            count_words()
            find_important_words()
            show_matches()
    
    # elif 

    else:
        print(f"Unrecognized input: '{ans}'")

    print()



print("TODO: save keywords to a file for reload")

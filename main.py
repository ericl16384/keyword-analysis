import csv, datetime



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
        print(f"{errors} erroneous lines found in '{filename}'")

    print(f"Read {i} lines from '{filename}'")
    

        

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
            assert isinstance(w, str)
            assert isinstance(count, int)
            if w in word_counts:
                word_counts[w] += count
            else:
                word_counts[w] = count
        total_hits += count

def find_display_words():
    global display_words
    display_words = []


    while len(display_words) <= display_count:
        # if word[0] not in keywords:
        #     display_words.append(word)

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




def help_message():
    print("Normal usage:")
    # print(" Type a word to add it to the filter")
    print(" Type a number, corresponding to a word to add it to the filter")
    print("Special commands:")
    print("   to show this help message")
    print(" $ to exit program")
    print(" ? to show top matching words")
    print(" + to save current working keywords")
    # print(" / to review saved keywords")
    print(" < to remove the newest working keyword")
    print(" [ to clear working keywords")

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





def reload():
    print(f"Loading from {current_file}")
    load_from_csv(current_file, depth)
    filter_by_keywords(keywords)
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
        for phrase, count in phrases:
            writer.writerow((" ".join(phrase), count))

reload()
print()




while True:
    print("For help, press ENTER")
    print(f"Working keywords: {keywords}")
    print(f"{len(phrases)} matching unique phrases ({total_hits} hits)")
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
        index = int(ans)
        if index < 1 or index > len(display_words):
            print(f"Index must be within 1 to {len(display_words)}")
        else:
            keyword = display_words[index-1]
            keywords.append(keyword)
            filter_by_keywords(keyword)
            count_words()
            find_display_words()
            show_matches()
    
    # elif 

    else:
        print(f"Unrecognized input: '{ans}'")

    print()



print("TODO: save keywords to a file for reload")

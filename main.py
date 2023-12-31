import csv, json, time


print("TODO: word-match")

config_file = "config.json"

def load_config():
    global config
    global locations_file, searches_file, adgroups_file, output_file
    global use_adgroups, adgroups_ignored_rows, adgroups_ignored_columns, adgroups_rows_are_synonyms

    # global AND_symbol, OR_symbol

    with open(config_file, "r") as f:
        config = json.loads(f.read())

    locations_file = config["locations_file"]
    searches_file = config["searches_file"]
    adgroups_file = config["adgroups_file"]
    # output_file = config["output_file"]

    use_adgroups= config["filter using adgroups"]
    adgroups_ignored_rows = config["ignored first adgroup rows"]
    adgroups_ignored_columns = config["ignored first adgroup columns"]
    adgroups_rows_are_synonyms = config["rows are synonymns"]

    # AND_symbol = config["AND symbol"]
    # OR_symbol = config["OR symbol"]


keywords = []


def load_locations():
    global locations
    print("Loading locations")
    with open(locations_file, "r") as f:
        locations = f.read()
    locations = set(json.loads(locations))

def load_searches():
    print(f"Loading from {searches_file}")

    global phrase_counts, keywords, whole_file_read
    phrase_counts = []

    whole_file_read = False

    errors = 0
    with open(searches_file, "r") as file:
        reader = csv.reader(file)

        # header = reader.__next__()
        header_raw = file.readline().strip()
        # assert header_raw in (
        #     "Keyword,Frequency",
        #     "Keyword,Traffic,Exact KW,abortion,clinic,near,Campaign,Ad Group,Group"
        # )

        i = 0
        while not whole_file_read:
            try:
                row = reader.__next__()
            except StopIteration:
                whole_file_read = True
                break
            except UnicodeDecodeError:
                errors += 1
                continue

            phrase = row[0]
            # words = phrase.split()

            if not phrase:
                continue

            try:
                count = int(row[1])
            except ValueError:
                errors += 1
                continue

            phrase_counts.append((phrase, count))

            i += 1
    
    # if not whole_file_read:
    #     print(f"WARNING: only using top {depth} keywords")
    
    if errors:
        print(f"{errors} erroneous lines found in '{searches_file}'")

    print(f"Read {i} lines from '{searches_file}'")

def load_adgroups():
    global adgroups

    with open(adgroups_file, "r") as f:
        reader = csv.reader(f)
        
        lines = []

        more_lines = True
        while more_lines:
            try:
                lines.append(reader.__next__())
            except StopIteration:
                more_lines = False

    adgroups = []
    trace = []

    y = adgroups_ignored_rows

    if adgroups_rows_are_synonyms:
        while y < len(lines):
            line = lines[y]

            current = [y, None, []]

            x = adgroups_ignored_columns
            while x < len(line):
                item = line[x]

                if item:
                    if current[1] == None:
                        current[1] = x

                    if item != "LOCATION":
                        item = item.lower()
                        
                    current[2].append(item)
                
                x += 1
            
            # print(current)
            
            if current[2]:
                while trace and current[1] <= trace[-1][1]:
                    # print(json.dumps(trace, indent=2))
                    # input()

                    adgroup = []
                    for l in trace:
                        adgroup.append(l[2])
                    adgroups.append(adgroup)
                    trace.pop()
                    # print(adgroup)

                trace.append(current)

            y += 1

            

            # print(trace)
            # print(current)

            # print(y)
            # print(json.dumps(adgroups, indent=2))
            # input()
            # for i in range(10):
            #     print()

        while trace:
            adgroup = []
            for l in trace:
                adgroup.append(l[2])
            adgroups.append(adgroup)
            trace.pop()

    else:
        while y < len(lines):
            line = lines[y]

            x = adgroups_ignored_columns
            while x < len(line):
                item = line[x]

                if item:
                    if item != "LOCATION":
                        item = item.lower()
                        
                    current = (y, x, item)

                    while trace and current[1] <= trace[-1][1]:
                        adgroup = []
                        for l in trace:
                            adgroup.append([l[2]])
                        adgroups.append(adgroup)
                        trace.pop()

                    trace.append(current)
                
                x += 1
            y += 1

        while trace:
            adgroup = []
            for l in trace:
                adgroup.append(l[2])
            adgroups.append(adgroup)
            trace.pop()
    
    for adgroup in adgroups:
        # print(adgroup)
        # input()
        for synonyms in adgroup:
            for phrase in synonyms:
                # print(phrase)
                if phrase.startswith(" "):
                    print(f"SUGGESTION: Replace space at start or end of adgroup member '{phrase}' in '{adgroup_to_string(adgroup)}' with # to signify the phrase must be at the start and/or end of a word.")
                    # input()

    # print(adgroups)

def save_overwrite_keywords():
    print(f"Overwriting '{searches_file}'")

    header = ["Keyword", "Frequency"]
    with open(searches_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        # for phrase, count in phrase_counts:
        #     writer.writerow((" ".join(phrase), count))
        writer.writerows(phrase_counts)


class KeywordData:
    def __init__(self, keyword) -> None:
        self.not_ = False
        self.start = False
        self.end = False

        while keyword:
            if keyword[0] == config["NOT symbol"]:
                self.not_ = True
            elif keyword[0] == config["word match symbol"]:
                self.start = True
            else:
                break
            keyword = keyword[1:]

        while keyword:
            if keyword[-1] == config["word match symbol"]:
                self.end = True
            else:
                break
            keyword = keyword[:-1]
        
        self.keyword = keyword

def process_keyword_flags(keyword):
    flags = {
        "not": False,
        "start": False,
        "end": False
    }

    while keyword:
        if keyword[0] == config["NOT symbol"]:
            flags["not"] = True
        elif keyword[0] == config["word match symbol"]:
            flags["start"] = True
        else:
            break
        keyword = keyword[1:]

    while keyword:
        if keyword[-1] == config["word match symbol"]:
            flags["end"] = True
        else:
            break
        keyword = keyword[:-1]
    
    flags["keyword"] = keyword
    
    return flags

def find_in_phrase_by_flags(phrase, flags):
    phrase = " " + phrase + " "

    keyword = flags["keyword"]
    if flags["start"]:
        keyword = " " + keyword
    if flags["end"]:
        keyword = keyword + " "

    return phrase.find(keyword) != -1

def filter_by_keywords(treat_as_AND=True):
    if len(keywords) == 0:
        return

    global phrase_counts
    new_phrases = []

    # print(phrase_counts)
    # print(keywords)

    # blocked_phrases = 0
    for phrase_count in phrase_counts:
        phrase, count = phrase_count

        keep = treat_as_AND

        for keyword in keywords:
            flags = process_keyword_flags(keyword)

            negate = flags["not"] ^ treat_as_AND

            if find_in_phrase_by_flags(phrase, flags) ^ negate:
                keep = not treat_as_AND
                break

        if keep:
            new_phrases.append(phrase_count)
            
    phrase_counts = new_phrases

def count_words():
    global word_counts, total_hits
    word_counts = {}
    total_hits = 0

    print("Counting remaining words")

    # print(phrase_counts[0])
    for phrase, frequency in phrase_counts:
        count = int(frequency)
        for w in phrase.split():
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
    find_display_words()

    rank = int(rank)
    if rank < 1 or rank > len(display_words):
        print(f"Number must be within 1 to {len(display_words)}")
    else:
        index = rank - 1
        keyword = display_words[index]
        if negate:
            keyword = config["NOT symbol"] + keyword
        # print(keywords)
        keywords.append(keyword)
        # print(keywords)
        print(f"Added keyword: '{keyword}'")
        filter_by_keywords()
        count_words()
        find_display_words()
        print()
        show_matches()

def replace_locations():
    print("Replacing locations with LOCATION")
    for i, phrase_count in enumerate(phrase_counts):
        phrase, count = phrase_count
        words = phrase.split()
        for start in range(len(words)):
            for end in range(start, len(words)):
                p = " ".join(words[start:end+1])
                if p in locations:
                    words = words[:start] + ["LOCATION"] + words[end+1:]
                    phrase_counts[i] = (" ".join(words), count)
                    words = phrase_counts[i][0].split()

def adgroup_to_string(adgroup):
    rows = []
    for row in adgroup:
        text = config["OR symbol"].join(row)
        if len(row) > 1 and len(adgroup) > 1:
            text = config["open parentheses symbol"] + text + config["close parentheses symbol"]
        rows.append(text)
        # print(row)
        # print(text)
        # input()
    adgroup_text = config["AND symbol"].join(rows)
        
    # else:
    #     adgroup_text = config["AND symbol"].join(adgroup)
    
    return adgroup_text


def reload():
    global start_time
    start_time = time.time()

    load_config()
    # load_file_hashes()

    load_searches()
    if config["replace with LOCATION"]:
        load_locations()
        replace_locations()
    filter_by_keywords()
    count_words()

def save_searches(filename=None):
    if not filename:
        filename = "SAVEFILE " + " ".join(keywords)
        filename += ".csv"
    print(f"Saving to '{filename}'")

    header = ["Keyword", "Frequency"]
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        # for phrase, count in phrase_counts:
        #     writer.writerow((" ".join(phrase), count))
        writer.writerows(phrase_counts)


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
    find_display_words()

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


def user_interface():
    global keywords

    global display_count
    display_count = 30

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
            # print("TODO")
            rank = ans[1:]
            add_keyword_from_display_words(rank, True)

        else:
            print(f"Unrecognized input: '{ans}'")

        print()
    
def save_top_words():
    filename = config["top_remaining_words_file"]
    number = config["number of saved remaining words"]

    print(f"Finding top {number} words")
    print()

    top_words_set = set()
    top_word_counts = []
    
    while len(top_word_counts) < number:
        max_count = 0
        max_word = None

        for word_count in word_counts.items():
            word, count = word_count
            
            # if word_count in top_word_counts:
            #     continue
            if word in top_words_set:
                continue

            if count <= max_count:
                continue

            max_count = count
            max_word = word
        
        if max_word == None:
            break

        top_words_set.add(max_word)
        top_word_counts.append((max_word, max_count))

        # print(top_words_set)
        # input()
    
    print(f"Saving top remaining words to {filename}")
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(("Word", "Count"))
        writer.writerows(top_word_counts)

# def filter_and_save_by_adgroups():
#     global phrase_counts, keywords

#     output_rows = []
#     unused_adgroups = []

#     for adgroup in adgroups:
#         if len(adgroup) < 2:
#             continue
            
#         print(adgroup)
#         input()

#         # skip = False
#         # for term in adgroup:
#         #     if " " in term:
#         #         print(f"WARNING: text-match not yet implemented. Skipping '{adgroup}'.")
#         #         skip = True
#         #         break
#         # if skip:
#         #     continue

#         # TODO word-match

#         # print()


#         old_phrases = phrase_counts.copy()

#         keywords = adgroup

#         # print("phrase_counts:", len(phrase_counts))
#         # print(keywords)
#         filter_by_keywords()
#         # print("phrase_counts:", len(phrase_counts))

#         # save_searches()
#         for phrase, count, in phrase_counts:
#             output_rows.append((
#                 " ".join(adgroup),
#                 phrase,
#                 count
#             ))

#         unused_phrases = []
#         i = 0

#         for phrase in old_phrases:
#             if i >= len(phrase_counts) or phrase != phrase_counts[i]:
#                 unused_phrases.append(phrase)
#             else:
#                 i += 1

#         # print(f"Adgroup: {adgroup}")
#         # print(f"Searches: {len(phrase_counts)}")
#         # print(f"Remaining: {len(unused_phrases)}")
#         print(f"{len(phrase_counts)}/{len(unused_phrases)} \"{adgroup_to_string(adgroup)}\"")
#         print()
#         if not phrase_counts:
#             unused_adgroups.append(adgroup)
        
#         phrase_counts = unused_phrases

#         # input()
    
#     print("Storing remaining phrases")
#     adgroup = ["REMAINING_PHRASES"]
#     for phrase, count, in phrase_counts:
#         output_rows.append((
#             " ".join(adgroup),
#             phrase,
#             count
#         ))
    
#     print(f"Saving adgroups to {output_file}")
#     with open(output_file, "w", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerow(("Adgroup", "Phrase", "Count"))
#         writer.writerows(output_rows)

#     if len(unused_adgroups):
#         print()
#         print("The following adgroups did not result in any matches. Please check their ordering and spelling.")
#         for w in unused_adgroups:
#             print(f"  {w}")

#     print()
    
#     count_words()
#     save_top_words()

#     print("Done saving")

def filter_and_save_by_adgroups():
    global phrase_counts, keywords

    unused_adgroups = []

    adgroup_output_rows = []
    adgroup_statistics_output_rows = []

    for adgroup in adgroups:
        # if len(a) < 2:
        #     continue

        # category = a[0]
        # adgroup = a[1:]

        # skip = False
        # for term in adgroup:
        #     if " " in term:
        #         print(f"WARNING: text-match not yet implemented. Skipping '{adgroup}'.")
        #         skip = True
        #         break
        # if skip:
        #     continue

        # TODO word-match

        # print()


        old_phrases = phrase_counts.copy()

        for k in adgroup:
            keywords = k
            filter_by_keywords(treat_as_AND=False)
        
        adgroup_text = adgroup_to_string(adgroup)
        
        # print(adgroup)
        # print(adgroup_text)
        # for x in phrase_counts[:30]:
        #     print(x)
        # input()

        # save_searches()


        unique_counts = 0
        aggregrate_counts = 0

        for phrase, count, in phrase_counts:
            adgroup_output_rows.append((
                adgroup_text,
                phrase,
                count
            ))

            unique_counts += 1
            aggregrate_counts += count

        adgroup_statistics_output_rows.append((
            adgroup_text,
            unique_counts,
            aggregrate_counts
        ))


        unused_phrases = []
        i = 0

        for phrase in old_phrases:
            if i >= len(phrase_counts) or phrase != phrase_counts[i]:
                unused_phrases.append(phrase)
            else:
                i += 1

        print(f"\"{adgroup_to_string(adgroup)}\"    {len(phrase_counts)}/{len(unused_phrases)}")
        # print()
        if not phrase_counts:
            unused_adgroups.append(adgroup)
        
        phrase_counts = unused_phrases

        # input()
    
    adgroup_text = "REMAINING_PHRASES"
    print(f"{adgroup_text}    {len(unused_phrases)}")
    unique_counts = 0
    aggregrate_counts = 0
    adgroup = [adgroup_text]
    for phrase, count, in phrase_counts:
        adgroup_output_rows.append((
            " ".join(adgroup),
            phrase,
            count
        ))
        unique_counts += 1
        aggregrate_counts += count
    adgroup_statistics_output_rows.append((
        adgroup_text,
        unique_counts,
        aggregrate_counts
    ))

    if len(unused_adgroups):
        print()
        print("The following adgroups did not result in any matches. Please check their ordering and spelling.")
        for w in unused_adgroups:
            print(f"  {adgroup_to_string(w)}")
    
    print()
    
    fn = config["output_file"]
    print(f"Saving adgroups to {fn}")
    with open(fn, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(("Adgroup", "Phrase", "Count"))
        writer.writerows(adgroup_output_rows)

    fn = config["adgroup_statistics_file"]
    print(f"Saving adgroup statistics to {fn}")
    with open(fn, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(("Adgroup", "Unique Phrases", "Aggregrate Matches"))
        writer.writerows(adgroup_statistics_output_rows)
    
    # print()
    # print(f"{len(unused_phrases)} phrases were not categorized.")

    print()
    
    count_words()
    save_top_words()

    # print("Done saving")



if __name__ == "__main__":
    reload()

    print()

    if use_adgroups:
        load_adgroups()
        filter_and_save_by_adgroups()
    else:
        user_interface()
    
    print()
    print(f"Elapsed time: {time.time()-start_time} seconds.")
    print("Program end. Press ENTER to exit.")
    input()


        

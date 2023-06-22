import csv, json

with open("adgroups_template.csv", "r") as f:
    reader = csv.reader(f)
    
    lines = []

    more_lines = True
    while more_lines:
        try:
            lines.append(reader.__next__())
        except StopIteration:
            more_lines = False

# class Item:
#     def __init__(self, content, parent):
#         self.content = content
#         self.parent = parent
#         self.children = []


# def parse_line(line, path):
#     if 

# data = {}
# path = []
# for line in lines:
#     for i, item in enumerate(line):
#         if not item:
#             continue
        
#         while i > len(path):
#             path.append("")
#         if i == len(path):

#             data[]


# lines = lines[35:47]

# print(json.dumps(lines, indent=2))


adgroups = []
line_trace = []
index = 0

index = 35

while index < len(lines):
    line = lines[index]

    for i, item in enumerate(line):
        if not item:
            continue

        if item:
            if i >= len(line_trace):
                line_trace.append(index)
                break
    
    index += 1

    if index == 47:
        break

print(line_trace)

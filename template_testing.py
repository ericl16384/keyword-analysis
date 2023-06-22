import csv, json

with open("adgroups_template.csv", "r") as f:
# with open("example_template.csv", "r") as f:
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
#     for x, item in enumerate(line):
#         if not item:
#             continue
        
#         while x > len(path):
#             path.append("")
#         if x == len(path):

#             data[]


# lines = lines[35:47]

# print(json.dumps(lines, indent=2))


adgroups = []
trace = []
y = 0

# y = 35
# y = 41

while y < len(lines):
    line = lines[y]

    x = 0
    while x < len(line):
        if x > 3:
            break

        # print(y, x)
        item = line[x]

        if item:
            current = (y, x, item)


            # for t in trace:
            #     print(t)
            # print("current:", current)
            # input()


            while trace and current[1] <= trace[-1][1]:
                adgroup = []
                for l in trace:
                    adgroup.append(l[2])
                adgroups.append(adgroup)
                trace.pop()

                # print("adgroup:", adgroups[-1])
                # print()

            trace.append(current)
        
        x += 1




            

            # if len(trace) < 2:
            #     x += 1

            # # same column
            # elif trace[-1][1] == trace[-2][1]:
            #     adgroup = []
            #     for l in trace:
            #         adgroup.append(l[2])
            #     adgroups.append(adgroup)
            #     print("adgroup:", adgroups[-1])

            # else:
            #     x += 1


            # if len(trace) < 2:
            #     pass
            # new_x = trace[-1][1]
            # old_x = trace[-2][1]

            # # new column
            # if new_x > old_x:
            #     pass

            # # same column
            # elif new_x <= old_x:
            #     adgroup = []
            #     for l in trace:
            #         adgroup.append(l[2])
            #     adgroups.append(adgroup)
            #     trace.pop()
            #     trace.pop()
            #     print("adgroup:", adgroups[-1])
            #     print()
            #     continue
            
            # else:
            #     # trace.append((y, x, item))
            #     print("todo")
            #     input()



            # else:
            #     trace.append((y, x, item))
            #     print("trace:", trace)
            #     input()



            # print(x, len(trace))
            # if x > len(trace):
            #     pass
            # elif x == len(trace):
            #     y -= 1
            # else:
            #     adgroup_found()
            #     trace.pop()
            #     y -= 2
        
    # print(y, trace)
    # input()
    
    y += 1

    # if y == 47:
    #     break

# print([x+1 for x in trace])

for adgroup in adgroups:
    print(adgroup)

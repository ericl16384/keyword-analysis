import csv, json

adgroups_template = "adgroups_template.csv"

def load_adgroups():
    global adgroups

    with open(adgroups_template, "r") as f:
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
    y = 0

    while y < len(lines):
        line = lines[y]

        x = 0
        while x < len(line):
            item = line[x]

            if item:
                current = (y, x, item)

                while trace and current[1] <= trace[-1][1]:
                    adgroup = []
                    for l in trace:
                        adgroup.append(l[2])
                    adgroups.append(adgroup)
                    trace.pop()

                trace.append(current)
            
            x += 1
        y += 1


load_adgroups()
for adgroup in adgroups:
    print(adgroup)

import sys
import csv

USAGE = '''USAGE: python3 add_results.py
Adds the predictions of FUDIA and the baselines to results.csv

Options:
    -h, --help      Displays this help
'''

# Handling paramters
if len(sys.argv) > 1 :
    print("ArgumentError: Needs no argument", file=sys.stderr)
    print(USAGE, file=sys.stderr)
    exit()

# Handling paramters
prefix = ""
i = 1
while i < len(sys.argv):
    arg = sys.argv[i]
    if arg == "--help" or arg == "-h":
        print(USAGE)
        exit()

    i += 1


# Loading positive ids
names = ["fudia", "quecq", "simplefudic"]
positives = {}
for name in names:
    written = open("Annotated/written_"+ name +".txt", "r")
    spoken = open("Annotated/spoken_"+ name +".txt", "r")
    positives[name] = [l[:-1] for l in written] + [l[:-1] for l in spoken]
    written.close()
    spoken.close()


# Opening result file
f = open("results.csv", "w")
results = csv.writer(f)

# header
results.writerow(["sent_id"] + names)

# list od ids
ids = ["written__"+str(i+1) for i in range(100)]
ids += ["spoken__"+str(i+1) for i in range(100)]

# For each row, puts 1 if the programme predicts
# a positive output on the sentence in that row
for id in ids:
    row = [id, "", "", ""]

    # Filling rows with 1 or 0
    for i, name in enumerate(names):
        if id in positives[name]:
            row[i+1] = 1
        else:
            row[i+1] = 0

    results.writerow(row)


# Closing file
f.close()
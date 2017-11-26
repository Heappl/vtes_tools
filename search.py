import csv, sys, unicodedata, re, subprocess, json, os
from difflib import SequenceMatcher

def getnormalized(name):
    ret = unicodedata.normalize('NFKD', name).encode('ascii','ignore').decode('ascii').lower()
    return re.compile("[^a-z0-9]").sub("", ret)
def addnormalized(arg):
    name = arg['Name']
    if ('Advanced' in arg) and arg['Advanced']:
        name += " adv"
    if ('Adv' in arg) and arg['Adv']:
        name += " adv"
    arg['normalized'] = getnormalized(name)
    return arg
def find_pictures(name):
    aux = subprocess.getoutput(['find pictures -name "' + name + '.*"']).split("\n")
    return [f for f in aux if os.path.isfile(f)]
def findfiles(arg):
    def exists(f):
        return os.path.isfile(f)
    def path(c):
        return "cards/" + c['id'] + ".jpg"
    return [path(c) for c in arg if 'id' in c and exists(path(c))] + sum([find_pictures(c['normalized']) for c in arg], [])
def addextra(arg):
    return addnormalized(arg)
    
def todict(cards):
    ret = {}
    for v in cards:
        name = v['normalized']
        if name not in ret:
            ret[name] = []
        ret[name].append(v)
    return ret

def readdata(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        all = [row for row in reader]
        header = all[0]
        return [addextra(dict(zip(header, row))) for row in all[1:]]
def readjsondata(filename):
    with open(filename, 'r') as jsonfile:
        return [addextra(e) for e in json.loads(jsonfile.read())]

def getnames(cards):
    return [card['filename'] for card in cards]


def get_diff(first, second):
    aux = [SequenceMatcher(None, first[i:i+len(second)], second).ratio() + (-0.01 * i) for i in range(0, len(first) - len(second))]
    if not aux:
        return len(second) + len(first)
    return len(second) / (1 + max(aux))
    

def find_card(name, cards):
    name = getnormalized(name)
    if name in cards:
        return cards[name]
    best = None
    best_score = 2123123
    for k in cards.keys():
        score = get_diff(k, name)
        if (score < best_score):
            best = cards[k]
            best_score = score
    return best

def pick_random(cards):
    import random
    return cards[random.randint(0, len(cards) - 1)]


if len(sys.argv) < 3:
    print("usage: search.py input output")
    sys.exit(1)

with open(sys.argv[1]) as inp:
    cards = todict(readdata('vteslib.csv') + readjsondata("vteslib.json") + readdata('vtescrypt.csv') + readjsondata('vtescrypt.json'))
    commands = []
    outputs = []
    files = []
    for f in inp.read().split("\n"):
        if f == "":
            continue
        tokens = f.split(" ")
        n = 1
        if tokens[-1].isdigit():
            f = " ".join(tokens[:-1])
            n = int(tokens[-1])
        card = find_card(f, cards)
        found = findfiles(card)
        if not found:
            print("ERROR: ", f, card, found)
            sys.exit(1)
        files += [pick_random(found) for i in range(0, n)]
    for i in range(0, len(files), 9):
        output = "merged_" + str(i // 9) + ".jpg"
        commands.append(" ".join(["./merge_cards.sh", output] + files[i:i+9]))
        outputs.append(output)


    for c in commands:
        print(c)
        subprocess.getoutput(c)
    subprocess.getoutput("rm " + sys.argv[2])
    subprocess.getoutput("bash topdf.sh " + " " + sys.argv[2] + " " + " ".join(outputs))
    subprocess.getoutput("rm " + " ".join(outputs))

#readjsondata("vteslib.json")

#for card in lib:
    #print(card['Name'])


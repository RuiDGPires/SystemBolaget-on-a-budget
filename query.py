import json
from drink import *
from glob import glob
import os
from dataclasses import dataclass
import sys
from optimize import optimize

def getFileName(path):
    name = os.path.basename(path)
    return os.path.splitext(name)[0]

DIR = os.path.abspath(os.path.dirname(__file__))
FILES = glob(f"{DIR}/data/*.json")
BLACKLISTS = list(map(lambda x: getFileName(x), glob(f"{DIR}/blacklist/*")))


drinks = {}
budget = None
N_DRINKS = None


for file in FILES:
    with open(file, "r", encoding="utf-8") as f:
        drinks[getFileName(file)] = json.load(f)
    drinks[getFileName(file)] = list(map(lambda x: Drink.from_dict(x), drinks[getFileName(file)]))

def print_help():
    print("Options:")
    print("\t-s <section>[,section]*\t|", "Sections to view")
    print("\t\t Sections:", str(drinks.keys()))
    print("\t-p <n> \t|", "Number of pages")
    exit()

argc = len(sys.argv)
i = 0
sections = list(drinks.keys())
verbose = False
blacklist = []

while i < argc:
    if sys.argv[i] == "-s":
        _secs = sys.argv[i+1].split(",")
        sections = []
        for sec in _secs:
            if sec == "cider":
                sec = "cider-blanddrycker"

            if sec not in drinks:
                print("Invalid section:", sec)
                exit()
            sections.append(sec)

        i += 1 
    elif sys.argv[i] == "-n":
        N_DRINKS = int(sys.argv[i+1])
        i += 1 
    elif sys.argv[i] == "-b":
        budget = float(sys.argv[i+1])
        i += 1 
    elif sys.argv[i] == "-v":
        verbose = True
    elif sys.argv[i] == "-l": # Location
        location = sys.argv[i+1]
        if location not in BLACKLISTS:
            print("Unknown store")
            exit()

        with open(os.path.join("blacklist", f"{location}.txt"), encoding="utf-8") as f:
            blacklist = list(map(lambda line: line.rstrip(), f.readlines()))

        i += 1
        
    i += 1

    
@dataclass
class RatioObject:
    id: int
    section: str
    ratio: int
    
def calcRatio(drink):
    return drink.ratio()

def sortFunc(r: RatioObject):
    return r.ratio

def getBest(lst, n=10):
    i = 1 
    for ratio in lst[:n]:
        r = ratio.ratio
        drink = drinks[ratio.section][ratio.id]
        print(f"[{i}]", drink)
        i += 1

if not budget:
    ratios = []
    for section in sections:
        i = 0
        for drink in drinks[section]:
            if drink.name in blacklist: continue
            ratios.append(RatioObject(id=i,section=section,ratio=calcRatio(drink)))
            i += 1

    ratios.sort(key=sortFunc)
    if N_DRINKS:
        getBest(ratios, N_DRINKS)
    else:
        getBest(ratios)
else:
    all_drinks = []
    for section in sections:
        all_drinks += drinks[section]

    if N_DRINKS:
        all_drinks = all_drinks[:N_DRINKS]

    all_drinks = list(filter(lambda x: x.name not in blacklist, all_drinks))

    res = optimize(all_drinks, budget, verbose=verbose)
    price = 0

    print()
    print(f"For a budget of {budget} SEK, here is the best combination of drinks to buy:")
    for row in res:
        print(f"\t{int(row[1])} x {row[0]}")
        price += row[1]*row[0].getPrice()
    print("Total price:", round(price, 2), "SEK")
    
    
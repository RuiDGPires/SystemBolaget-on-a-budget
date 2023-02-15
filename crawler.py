from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.firefox.options import Options
from dataclasses import dataclass, asdict
import json
import sys
from drink import Drink

SECTIONS = ["vin", "ol", "sprit", "cider-blanddrycker"]
sections = SECTIONS
PAGES = 100

i = 1
argc = len(sys.argv)

def print_help():
    print("Options:")
    print("\t-s <section>[,section]*\t|", "Sections to gather info from")
    print("\t\t Sections:", str(SECTIONS))
    print("\t-p <n> \t|", "Number of pages")
    exit()


while i < argc:
    if sys.argv[i] == "-s":
        _secs = sys.argv[i+1].split(",")
        for sec in _secs:
            if sec not in SECTIONS:
                print("Invalid section:", sec)
                exit()

        sections = _secs

        i += 1 
    elif sys.argv[i] == "-p":
        PAGES = int(sys.argv[i+1])
        i += 1
    elif sys.argv[i] == "-h":
        print_help()

    i += 1

    
print("Gathering info from:", str(sections))
print("Pages:", str(PAGES))
print()

class CrawlerException(Exception):
    pass

class NoName(CrawlerException):
    def str(self):
        return "No name"

class NoQuantity(CrawlerException):
    def str(self):
        return "No quantity"

drinks = {}

for section in sections:
    drinks[section] = []

options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)

def waitForLoad():
    while True:
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, "Jag har fyllt 20 år")))
            print("Page Loaded")
            break
        except TimeoutException:
            continue
    

def waitForSearch(page):
    while True:
        try:
            WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/main/div[2]/div[2]/div/div[2]/div[2]/div/div[1]/div[1]/h2"), "produkter"))
            print(f"{page} Search Complete")
            break
        except TimeoutException:
            continue

def agreeAll():
    waitForLoad()
    element = driver.find_element(By.LINK_TEXT, "Jag har fyllt 20 år")
    element.click()
    element = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/button[1]")
    element.click()

def getDrinkFromElement(element):

    # /html/body/div/main/div[2]/div[2]/div/div[2]/div[2]/div/div[2]"
    try:
        name = element.find_element(By.XPATH, "./div/div[1]/div/div[2]/div[1]/p[1]").text
    except:
        raise NoName

    price = tuple(map(lambda x : int(x.replace("*", "").replace(" ", "").replace("-", "0")), element.find_element(By.XPATH, "./div/div[1]/div/div[2]/div[2]/p").text.split(":"))) # (Kr, Cent)

    div = element.find_element(By.XPATH, "./div/div[1]/div/div[2]/div[2]")
    perc = float(div.find_element(By.XPATH, ".//*[contains(text(),'%')]").text.replace("%", "").replace(",", "."))

    # Quantity stuff:
    try:
        string =  div.find_element(By.XPATH, ".//*[contains(text(),'ml')]").text.replace("ml", "")
    except:
        raise NoQuantity

    calc = []
    if "påsar à" in string:
        calc = string.split("påsar à")
    elif "fl à" in string:
        calc = string.split("fl à")
    elif "flaskor à" in string:
        calc = string.split("flaskor à")
    elif "flaskor á" in string:
        calc = string.split("flaskor á")
    elif "flaskor a" in string:
        calc = string.split("flaskor a")
    else:
        calc = ["1", string]

    try:
        quantity = int(calc[0]) * int(calc[1])
    except:
        quantity = 0

    type = element.find_element(By.XPATH, "./div/div[1]/div/div[2]/p").text
    info = ""
    try:
        info = element.find_element(By.XPATH, "./div/div[1]/div/div[2]/div[1]/p[2]").text
    except:
        pass

    return Drink(name=name, price=price, perc=perc, quantity=quantity, type=type, info=info)

first = True
for section in sections:
    url = f"https://www.systembolaget.se/sortiment/{section}/?p={PAGES}&sortera-pa=Price&i-riktning=Ascending"
    driver.get(url)

    if first:
        agreeAll()
        first = False
    waitForSearch(section)

    # Get div
    element  = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[2]/div/div[2]/div[2]/div/div[2]")
    children = element.find_elements(By.XPATH, ".//a")
    total = len(children)

    n = 1
    last = 0
    for child in children:
        try:
            drinks[section].append(getDrinkFromElement(child).dict())
        except CrawlerException:
            pass
        
        new = 100 * n // total
        if new // 10 != last:
            print(n, "|", total, f"({new}%)")
            last = new // 10
        n += 1

    with open(f"out/{section}.json", "w", encoding="utf-8") as f:
        json.dump(drinks[section], f, ensure_ascii=False)

    print(f"{section} page Complete")

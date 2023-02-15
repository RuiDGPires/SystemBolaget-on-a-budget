# Systembolaget on a budget

## Installation

- Get  [python3](https://www.python.org/)
- Install the requirements:\
    Run the following commands on the command line  (make sure you are in the right directory):\
    Use pip3 or pip depending on the OS
```sh
    $pip3 install -r query-requirements.txt 
```
## Usage

Use python3 or python depending on the OS

```sh
    $python3 query.py [-s <SECTION>[,<SECTION>]*] [-b <BUDGET>] [-n <N_DRINKS>]
```

**Sections:**
- ol (beer)
- cider (cider and stuff)
- vin (wine)
- sprit (spirits)

## Examples

### Listing by Ratio
---

For example, if you want to get the 10 best drinks in price per alcohol percentage:

```sh
    $python3 query.py -n 10
```
---

If you want to get the 5 best ciders in price per alcohol percentage:

```sh
    $python3 query.py -s cider -n 10
```
---

### Planning by budget
---

If you want to get the best combination of drinks in terms of total alcohol for a budget of 150 SEK:

```sh
    $python3 query.py -b 150
```
---

If you want to get the best combination of **wine and cider** in terms of total alcohol for a budget of 150 SEK:

```sh
    $python3 query.py -s vin,cider -b 150
```

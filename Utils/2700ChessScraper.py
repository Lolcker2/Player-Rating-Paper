from math import ceil
from glob import glob
from playwright.sync_api import sync_playwright

ResultWeights = {"W": 1, "D": 0.5, "L": 0}

# returns whether the contents of a given string is an integer
def isInt(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def formatName(name: str) -> str:
    first, last = name.split("_")
    return f"{first}, {last}".lower()

def read(filename: str)->str:
    with open(filename, "r",  encoding="UTF-8") as f:
        return f.read()

def unifyTempCache(name):
    files = sorted(glob(r"../TempCache/*.txt"), key=lambda x: int(x.split("../TempCache\\")[1].split(r".txt")[0]))
    print(files)
    result = "\n".join([read(file) for file in files])
    filename = rf"../Cache/{name.replace('_', ' ')}-unified_matches.txt"
    with open(filename, "w+", encoding="UTF-8") as f:
        f.write(result)

def getMatches(webPage, name: str, pageNum: int) -> list:
        webPage.goto(f"https://2700chess.com/players/{name}?page={pageNum}", wait_until="networkidle")
        rows = webPage.locator("table tbody tr")

        history = []
        for row in rows.all():
            cells = [td.inner_text().strip() for td in row.locator("td").all()]
            result = ResultWeights[cells[5][-1]]

            # skip all draws
            if result == 0.5:
                continue

            if not isInt(cells[2]) or not isInt(cells[4]):
                continue

            # reorient
            if cells[3].lower() == formatName(name):
                history.append([cells[4], cells[2], -1 * result + 1])
                continue
            history.append([cells[2], cells[4], result])

        return history

def cachePage(result: list, page: int):
    filename = rf"../TempCache/{page}.txt"
    with open(filename, "w+", encoding="UTF-8") as f:
        f.write("\n".join([f"{match[0]} VS {match[1]} | {match[2]}" for match in result]))

def get_rating_history(name: str, number: int, starting_page: int = 1) -> None:
    aggregate = []

    with (sync_playwright() as p):
        browser = p.chromium.launch(headless=False)
        webPage = browser.new_page()

        # last
        pages = ceil(number / 50) + starting_page
        for page in range(starting_page, pages - 1):

            # caching
            result = getMatches(webPage, name, page)
            cachePage(result, page)

            aggregate += result


        # caching
        result = getMatches(webPage, name, pages)[0:50 if number%50==0 else number%50] # last page
        cachePage(result, pages)

        aggregate += result
        browser.close()

    final = "\n".join([f"{match[0]} VS {match[1]} | {match[2]}" for match in aggregate])

    filename = rf"../Cache/{name.replace('_', ' ')}-{number}_matches.txt"
    with open(filename, "w+", encoding="UTF-8") as f:
        f.write(final)


# add a way to start at page 21, do 5~10 chunks of 20 pages each for 5k~10k matches
if __name__ == "__main__":
    # get_rating_history("carlsen_magnus", 1000, 80)
    unifyTempCache("carlsen_magnus")
from math import ceil
from playwright.sync_api import sync_playwright

ResultWeights = {"W": 1, "D": 0.5, "L": 0}

def formatName(name: str) -> str:
    first, last = name.split("_")
    return f"{first}, {last}".lower()

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

            if cells[3].lower() == formatName(name):
                history.append([cells[4], cells[2], -1 * result + 1])
                continue
            history.append([cells[2], cells[4], result])

        return history


def get_rating_history(name: str, number: int) -> None:
    aggregate = []


    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        webPage = browser.new_page()

    # last
        pages = ceil(number / 50)
        for page in range(pages - 1):
            aggregate += getMatches(webPage, name, page)

        aggregate += getMatches(webPage, name, pages)[0:50 if number%50==0 else number%50] # last page
        browser.close()

    final = "\n".join([f"{match[0]} VS {match[1]} | {match[2]}" for match in aggregate])

    filename = rf"../Cache/{name.replace('_', ' ')}-{number}_matches.txt"
    with open(filename, "w+", encoding="UTF-8") as f:
        f.write(final)


if __name__ == "__main__":
    get_rating_history("carlsen_magnus", 50)
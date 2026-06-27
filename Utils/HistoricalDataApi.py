import requests

USER_AGENT_HEADER = {"User-Agent": "personal-cache-tool/1.0"}
RESULT_DICT = {"win": 1, "agreed": 0.5, "repetition": 0.5, "stalemate": 0.5, "insufficient": 0.5, "50move": 0.5, "timevsinsufficient": 0.5, "draws": 0.5}

# get all achives
def getArchives(name: str) -> list[str]:
    url = f"https://api.chess.com/pub/player/{name}/games/archives"
    return requests.get(url, headers=USER_AGENT_HEADER).json().get("archives", [])

# get all games from a given archive
def gamesFromArchive(archive_url: str) -> list[dict]:
    return requests.get(archive_url, headers=USER_AGENT_HEADER).json().get("games", [])

# reorder the game for costum format
def formatGame(game: dict, name: str) -> str:
    players = [game.get("white", {}), game.get("black", {})]
    players = players if players[0].get("username", "").lower() == name.lower() else players[::-1]

    result = players[0].get("result", "")
    result = RESULT_DICT[result] if result in RESULT_DICT else 0

    player = f"{players[0].get('username', '?')}, {players[0].get('rating', '?')}"
    opp = f"{players[1].get('username', '?')}, {players[1].get('rating', '?')}"

    return f"{player} VS {opp} | {result}"

# save & cache
def cacheMatches(name: str, num: int):
    archives = getArchives(name)
    collected: list[str] = []

    # loop recent -> old all archives
    for archive_url in reversed(archives):
        games = gamesFromArchive(archive_url)

        # loop recent -> old all games from archive
        for game in reversed(games):
            collected.append(formatGame(game, name))

            if len(collected) >= num:
                break

    # cache
    output = "\n".join(collected)
    filename = rf"{name}-{num}_matches.txt"
    with open(filename, "w+", encoding="UTF-8") as f:
        f.write(output)

if __name__ == "__main__":
    cacheMatches("hikaru", 50)
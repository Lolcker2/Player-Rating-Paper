import requests

BASE_URL = "https://api.chess.com"
USER_AGENT_HEADER = {"User-Agent": "personal-cache-tool/1.0 contact@example.com"}


def get_archives(username: str) -> list[str]:
    """Return list of monthly archive URLs for a player, oldest first."""
    url = f"{BASE_URL}/pub/player/{username}/games/archives"
    response = requests.get(url, headers=USER_AGENT_HEADER)
    response.raise_for_status()
    return response.json().get("archives", [])


def get_games_from_archive(archive_url: str) -> list[dict]:
    """Fetch all games from a single monthly archive URL."""
    response = requests.get(archive_url, headers=USER_AGENT_HEADER)
    response.raise_for_status()
    return response.json().get("games", [])


def format_game(game: dict, username: str) -> str:
    white = game.get("white", {})
    black = game.get("black", {})

    is_white = white.get("username", "").lower() == username.lower()
    player  = white if is_white else black
    opponent = black if is_white else white

    raw_result = player.get("result", "")
    if raw_result == "win":
        result = 1
    elif raw_result in ("agreed", "repetition", "stalemate", "insufficient",
                        "50move", "timevsinsufficient", "draws"):
        result = 0.5
    else:
        result = 0  # loss, resigned, timeout, checkmated, abandoned, etc.

    player_str   = f"{player.get('username', '?')}, {player.get('rating', '?')}"
    opponent_str = f"{opponent.get('username', '?')}, {opponent.get('rating', '?')}"

    return f"{player_str} VS {opponent_str} | {result}"


def cache_matches(username: str, num: int):
    """
    Fetch the most recent `num` games for `username` and write them to a file.
    Games are fetched newest-first (archives reversed), stopping at `num`.
    """
    archives = get_archives(username)
    if not archives:
        print(f"No archives found for '{username}'.")
        return

    collected: list[str] = []

    # Work backwards through archives (most recent first)
    for archive_url in reversed(archives):
        if len(collected) >= num:
            break

        print(f"Fetching {archive_url} ...")
        games = get_games_from_archive(archive_url)

        # Most recent games are at the end of each archive
        for game in reversed(games):
            if len(collected) >= num:
                break
            collected.append(format_game(game, username))

    output = "\n".join(collected)
    filename = rf"{username}-{num}_matches.txt"
    with open(filename, "w+", encoding="UTF-8") as f:
        f.write(output)

    print(f"Wrote {len(collected)} games to {filename}")

if __name__ == "__main__":
    cache_matches("hikaru", 50)
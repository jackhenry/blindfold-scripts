import datetime
import re
import requests
import pytz

from datetime import timezone

local = pytz.timezone("US/Central")

createQuery = """
mutation createScoreboard($input: ScoreboardInput) {
  createScoreboard(input: $input) {
    date
  }
}
"""


def parse_status(status: str):

    if status == "Final":
        return status

    for fmt in ("%H:%M %p %z", "%a %H:%M %p %z"):
        try:
            trimmed = ""
            if "CT" not in status:
                trimmed = status + " CT"
            trimmed = status.replace("\n", " ").replace("CT", "+0600").upper()
            formatted = datetime.datetime.strptime(trimmed, fmt)
            return str(formatted)
        except:
            pass

    return status


def parse_date(date):
    formatted_date = re.sub(r"(\d)(st|nd|rd|th)", r"\1", date)
    for fmt in ("%A, %B %d", "%B %d, %Y"):
        try:
            parsed_date = datetime.datetime.strptime(formatted_date, fmt)
            current_year = datetime.datetime.now().year
            parsed_date = parsed_date.replace(year=current_year)
            return parsed_date
        except ValueError:
            pass


def send_boxscore_backend(boxscores, league):
    for date in boxscores:
        for game in boxscores[date]:
            status = game["status"]
            gameId = game["gameId"]
            awayTeamName = game["away"]["name"]
            awayTeamRecord = game["away"]["record"]
            awayTeamQuarters = game["away"]["quarters"]
            awayTeamScore = game["away"]["total"]
            awayTeamRecord = game["away"]["record"]

            homeTeamName = game["home"]["name"]
            homeTeamRecord = game["home"]["record"]
            homeTeamQuarters = game["home"]["quarters"]
            homeTeamScore = game["home"]["total"]
            homeTeamRecord = game["home"]["record"]

            week = game["week"] if "week" in game else None

            parsed_date = parse_date(date)
            try:
                response = requests.post(
                    "http://localhost:3001/graphql",
                    json={
                        "query": createQuery,
                        "variables": {
                            "input": {
                                "gameId": gameId,
                                "awayTeamName": awayTeamName,
                                "awayTeamQuarters": awayTeamQuarters,
                                "awayTeamScore": awayTeamScore,
                                "awayTeamRecord": awayTeamRecord,
                                "homeTeamName": homeTeamName,
                                "homeTeamQuarters": homeTeamQuarters,
                                "homeTeamScore": homeTeamScore,
                                "homeTeamRecord": homeTeamRecord,
                                "week": week,
                                "league": league,
                                "date": str(parsed_date.isoformat() + "Z"),
                                "status": status,
                            }
                        },
                    },
                )
            except:
                print("No connection to backend. Skipping...")

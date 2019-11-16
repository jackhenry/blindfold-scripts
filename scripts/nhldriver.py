from bs4 import BeautifulSoup
from datetime import datetime
import json

import client


def parseBoxScore(data):
    team_name = data.find("div", attrs={"class": "ScoreCell__TeamName"}).text
    team_record = data.find("span", attrs={"class": "ScoreboardScoreCell__Record"}).text

    period_score_values = data.findAll(
        "div", attrs={"class": "ScoreboardScoreCell__Value"}
    )
    team_quarters = []
    for score in period_score_values:
        team_quarters.append(score.text)

    team_total = ""
    try:
        team_total = data.find("div", attrs={"class": "ScoreCell__Score"}).text
    except:
        pass

    return {
        "name": team_name,
        "record": team_record,
        "total": team_total,
        "quarters": team_quarters,
    }


def parse(html):
    soup = BeautifulSoup(html, "html.parser")

    date = soup.select_one("div.Card__Header__Title__Wrapper > h3").text
    print(date)
    scoreboards = soup.findAll("section", attrs={"class": "Scoreboard"})

    final_format = {}
    for scoreboard in scoreboards:
        gameId = scoreboard.attrs["id"]
        status: str = scoreboard.find("div", attrs={"class": "ScoreCell__Time"}).text
        try:
            datetime.strptime(status.upper(), "%H:%M %p")
            # String is in the format of 3:00 pm, append ET
            status = status.upper() + " ET"
        except:
            pass

        print(status)
        home_team_data = scoreboard.find(
            "li", attrs={"class": "ScoreboardScoreCell__Item--home"}
        )
        away_team_data = scoreboard.find(
            "li", attrs={"class": "ScoreboardScoreCell__Item--away"}
        )
        home_box = parseBoxScore(home_team_data)
        away_box = parseBoxScore(away_team_data)

        if date not in final_format:
            final_format[date] = []
        final_format[date].append(
            {"gameId": gameId, "away": away_box, "home": home_box, "status": status}
        )
    client.send_boxscore_backend(final_format, "NHL")

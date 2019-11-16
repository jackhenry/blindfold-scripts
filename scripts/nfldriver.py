from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from datetime import datetime


import json
import re
import requests

import client

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

    try:
        status = status.replace("\n", " ").replace("CT", "-0600")
        formatted = datetime.strptime(status, "%a %H:%M %p %z")
        return formatted
    except:
        return status


def parseBoxScore(table, team):
    team_data = table.select_one("td.{}".format(team))
    team_name = team_data.select_one("span.sb-team-short").text
    team_record = team_data.select_one("p.record.overall").text.strip()

    team_quarters = []
    team_total = ""
    score_elements = team_data.findNextSiblings("td")
    for elem in score_elements:
        if "class" in elem.attrs:
            if "score" in elem.attrs["class"]:
                team_quarters.append(elem.text.strip())
            if "total" in elem.attrs["class"]:
                team_total = elem.text.strip()

    return {
        "name": team_name,
        "record": team_record,
        "total": team_total,
        "quarters": team_quarters,
    }


def parseWeek(weekText: str):
    weeksMap = {
        "Preseason Week 1": -4,
        "Preseason Week 2": -3,
        "Preseason Week 3": -2,
        "Preseason Week 4": -1,
        "Week 1": 1,
        "Week 2": 2,
        "Week 3": 3,
        "Week 4": 4,
        "Week 5": 5,
        "Week 6": 6,
        "Week 7": 7,
        "Week 8": 8,
        "Week 9": 9,
        "Week 10": 10,
        "Week 11": 11,
        "Week 12": 12,
        "Week 13": 13,
        "Week 14": 14,
        "Week 15": 15,
        "Week 16": 16,
        "Week 17": 17,
        "Wild Card": 18,
        "Divisional Round": 19,
        "Conference Championships": 20,
        "Super Bowl": 21,
    }

    return weeksMap.get(weekText, 0)


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    events = soup.select_one(
        """section#pane-main > section#main-container > div.main-content > section.col-b > div.scoreboards > div#events"""
    )

    weekText = soup.select_one("div.dropdown-type-week > button").text.strip()
    week = parseWeek(weekText)

    final_format = {}
    scoreboards = events.findAll("article", attrs={"class": ["scoreboard", "football"]})
    for game in scoreboards:
        # The closest h2.date-heading is the date of the game
        date = game.findPreviousSibling("h2", attrs={"class": ["date-heading"]}).text
        gameId = game.attrs["id"]
        table = game.find("table")
        status = table.select_one("th", attrs={"class": "date-time"}).text.strip()
        home_box = parseBoxScore(table, "home")
        away_box = parseBoxScore(table, "away")

        # If data-date attribute exists, use that for status instead
        try:
            utcDate = game.select_one("th", attrs={"class": "date-time"}).attrs[
                "data-date"
            ]
            canFormat = datetime.strptime(utcDate, "%Y-%m-%dT%H:%MZ")
            status = utcDate
        except:
            pass

        if date not in final_format:
            final_format[date] = []
        final_format[date].append(
            {
                "gameId": gameId,
                "status": status,
                "week": week,
                "away": away_box,
                "home": home_box,
            }
        )

    client.send_boxscore_backend(final_format, "NFL")


def main():
    pass


if __name__ == "__main__":
    main()


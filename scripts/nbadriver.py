from bs4 import BeautifulSoup
from datetime import datetime
import client


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


def parse(html):
    soup = BeautifulSoup(html, "html.parser")

    # Select date so it can be prepended to html file
    date = soup.select_one("div.carousel-day > span")

    final_format = {}
    date = date.text.replace("Scores for ", "")
    scoreboards = soup.find_all(
        "article", attrs={"class": ["scoreboard", "basketball"]}
    )
    for game in scoreboards:
        gameId = game.attrs["id"]
        table = game.find("table")
        status = table.select_one("th", attrs={"class": "date-time"}).text.strip()
        home_box = parseBoxScore(table, "away")
        away_box = parseBoxScore(table, "home")

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
            {"gameId": gameId, "away": away_box, "home": home_box, "status": status}
        )

    client.send_boxscore_backend(final_format, "NBA")

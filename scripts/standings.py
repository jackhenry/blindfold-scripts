from bs4 import BeautifulSoup


def parse_nfl(html):
    soup = BeautifulSoup(html, "html.parser")
    container = soup.find(
        "div", attrs={"class": ["standings-component", "schedules" "nfl"]}
    )
    tables = container.findAll("table")

    standings = {}

    for counter, table in enumerate(tables):
        conference = table.findPreviousSibling("h4").text
        division = table.find("th", attrs={"class": "team-column"}).text.strip()
        print(division)
        header = table.find("tr", attrs={"class": "table-heading"})
        team_rows = header.findNextSiblings("tr")
        for counter, team_row in enumerate(team_rows):
            team = team_row.find("span", attrs={"class": "desktop-only"}).text
            rank = counter + 1
            wins = team_row.select_one("td.numeric-score.wins").text
            losses = team_row.select_one("td.numeric-score.losses").text
            ties = team_row.select_one("td.numeric-score.draws").text
            pointsFor = team_row.select_one("td.points-for").text
            pointsAgainst = (
                team_row.select_one("td.points-for").findNextSibling("td").text
            )
            homeRecord = team_row.select_one("td.home-record").text
            awayRecord = team_row.select_one("td.away-record").text
            divisionRecord = team_row.select_one("td.division-record").text
            conferenceRecord = team_row.select_one("td.conference-record").text
            streak = team_row.select_one("td.streak").text
            standings[team] = {
                "rank": rank,
                "conference": conference,
                "division": division,
                "wins": wins,
                "losses": losses,
                "ties": ties,
                "pointsFor": pointsFor,
                "pointsAgainst": pointsAgainst,
                "homeRecord": homeRecord,
                "awayRecord": awayRecord,
                "divisionRecord": divisionRecord,
                "conferenceRecord": conferenceRecord,
                "streak": streak,
            }


def parse_nba(html):
    soup = BeautifulSoup(html, "html.parser")
    container = soup.find(
        "div", attrs={"class": ["standings-component", "schedules" "nfl"]}
    )
    tables = container.findAll("table")
    standings = {}

    for counter, table in enumerate(tables):
        conference = table.findPreviousSibling("h4").text
        division = table.find("th", attrs={"class": "team-column"}).text.strip()
        header = table.find("tr", attrs={"class": "table-heading"})
        team_rows = header.findNextSiblings("tr")
        for counter, team_row in enumerate(team_rows):
            team = team_row.find("span", attrs={"class": "desktop-only"}).text
            rank = counter + 1
            wins = team_row.select_one("td.numeric-score.wins").text
            losses = team_row.select_one("td.numeric-score.losses").text
            winningPercentage = team_row.select_one("td.winning-pct").text
            gamesBehind = team_row.select_one("td.games-behind").text
            homeRecord = team_row.select_one("td.home-record").text
            awayRecord = team_row.select_one("td.away-record").text
            lastTen = team_row.select_one("td.last-ten").text
            streak = team_row.select_one("td.streak").text
            standings[team] = {
                "rank": rank,
                "conference": conference,
                "division": division,
                "wins": wins,
                "losses": losses,
                "winningPercentage": winningPercentage,
                "gamesBehind": gamesBehind,
                "homeRecord": homeRecord,
                "awayRecord": awayRecord,
                "lastTen": lastTen,
                "streak": streak,
            }


def parse_nhl(html):
    soup = BeautifulSoup(html, "html.parser")
    container = soup.find(
        "div", attrs={"class": ["standings-component", "schedules" "nfl"]}
    )
    tables = container.findAll("table")
    standings = {}

    for counter, table in enumerate(tables):
        conference = table.findPreviousSibling("h4").text
        division = table.find("th", attrs={"class": "team-column"}).text.strip()
        header = table.find("tr", attrs={"class": "table-heading"})
        team_rows = header.findNextSiblings("tr")
        for counter, team_row in enumerate(team_rows):
            team = team_row.find("span", attrs={"class": "desktop-only"}).text
            rank = counter + 1
            wins = team_row.select_one("td.numeric-score.wins").text
            losses = team_row.select_one("td.numeric-score.losses").text
            overtimeLosses = team_row.select_one(
                "td.numeric-score.over-time-losses"
            ).text
            teamPoints = team_row.select_one("td.numeric-score.team-points").text
            goalsFor = team_row.select_one("td.numeric-score.goals-fore").text
            goalsAgainst = team_row.select_one("td.numeric-score.goals-against").text
            goalsDifference = team_row.select_one(
                "td.numeric-score.goals-difference"
            ).text
            shootout = team_row.select_one("td.numeric-score.shootout").text
            standings[team] = {
                "rank": rank,
                "conference": conference,
                "division": division,
                "wins": wins,
                "losses": losses,
                "overtimeLosses": overtimeLosses,
                "teamPoints": teamPoints,
                "goalsFor": goalsFor,
                "goalsAgainst": goalsAgainst,
                "goalsDifference": goalsDifference,
                "shootout": shootout,
            }

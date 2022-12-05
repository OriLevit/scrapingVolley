import operator
from datetime import date
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from tqdm import tqdm


def get_leagues(link):
    soup = BeautifulSoup(link, "html.parser")
    list_items = soup.find_all("tr")
    leagues = []
    for league in list_items[1:]:
        league = league.findAll("div", {"class": "board"})
        for temp in league:
            link = f"https://www.iva.org.il/{temp.findNext('a', href=True)['href']}"
            leagues.append(link)
    return leagues


def get_title(link):
    soup = BeautifulSoup(link, "html.parser")
    title = soup.find("div", {"class": "texts"}).findNext("h1").text
    return title


def get_teams(link, team_list: list):
    soup = BeautifulSoup(link, "html.parser")
    list_items = soup.find("div", {"class": "legue-table"}).find_all("tr")
    for team in list_items[1:]:
        team_name = team.findNext("td", {"class": "sticky-col"}).findNext("a").text
        info = team.findAll()
        team_format = {
            "name": team_name[4:len(team_name)],
            "score": int(info[-1].text)
        }
        team_list.append(team_format)


def get_upcoming_games(link, game_list: list):
    soup = BeautifulSoup(link, "html.parser")
    game_container = soup.find("div", {"class": "games-table"})
    tbody = game_container.findNext("tbody")
    rows = tbody.findAll("tr")
    for row in rows:
        dates = row.findNext("td").text[1:11]
        year = int(dates[6:10])
        month = int(dates[3:5])
        day = int(dates[:2])
        date_formated = date(year=year, month=month, day=day)
        length = len(row.findNext("td").text)
        time = row.findNext("td").text
        first_team = row.findNext("td").findNext("td").findNext("td").text
        second_team = row.findNext("td").findNext("td").findNext("td").findNext("td").text
        venue = row.findNext("td").findNext("td").findNext("td").findNext("td").findNext("td").text
        game = {
            "date": date_formated,
            "time": time.strip()[(length - 7):].strip(),
            "first_team": first_team,
            "second_team": second_team,
            "venue": venue
        }
        game_list.append(game)


def print_teams(teams_list: list):
    teams_list.sort(key=operator.itemgetter('score'), reverse=True)
    t = PrettyTable(["קבוצה", "ניקוד"])
    for team in teams_list:
        t.add_row([team["name"], team["score"]])
    print(t)


def print_games(games_list: list, league):
    t = PrettyTable(["תאריך", "קבוצה ראשונה", "קבוצה שנייה", "שעה", "אולם"])
    t.title = f"משחקים ליגה {league}"
    for game in games_list:
        t.add_row([game["date"], game["first_team"], game["second_team"], game["time"], game["venue"]])
    print(t)


def get_teams_sorted(league_table):
    all_leagues_links = get_leagues(league_table)
    all_teams = []

    for link in tqdm(all_leagues_links, bar_format='{l_bar}{bar:100}', desc="Gathering teams"):
        get_teams(link, all_teams)
        return all_teams

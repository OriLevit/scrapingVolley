import operator
from urllib.request import urlopen

from prettytable import PrettyTable
import soup_manager
from tqdm import tqdm


def print_all_games(all_games: list):
    for _ in range(len(all_games)):
        print_games(all_games[_]["games"], all_games[_]["title"])


def get_games(link, league_title, all_games):
    league_games = []
    soup_manager.get_upcoming_games(urlopen(link), league_games)
    league_games.sort(key=operator.itemgetter('date'))
    league = {
        "games": league_games,
        "title": league_title
    }
    all_games.append(league)


def print_teams(teams_list: list):
    teams_list.sort(key=operator.itemgetter('score'), reverse=True)
    t = PrettyTable(["קבוצה", "ניקוד"])
    for team in teams_list:
        t.add_row([team["name"], team["score"]])
    print(t)


def print_games(games_list: list, league):
    t = PrettyTable(["תאריך", "קבוצה ראשונה", "קבוצה שנייה", "שעה", "אולם"])
    t.title = f"משחקים {league}"
    for game in games_list:
        t.add_row([game["date"], game["first_team"], game["second_team"], game["time"], game["venue"]])
    print(t)


def get_teams_sorted(league_table):
    all_leagues_links = soup_manager.get_leagues(league_table)
    all_teams = []

    for link in tqdm(all_leagues_links, bar_format='{l_bar}{bar:100}', desc="Gathering teams"):
        soup_manager.get_teams(link, all_teams)
        return all_teams

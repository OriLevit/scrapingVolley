import operator
from urllib.request import urlopen

from bs4 import BeautifulSoup


def get_leagues(link):
    soup = BeautifulSoup(link, "html.parser")
    list_items = soup.find_all("tr")
    leagues = []
    for league in list_items[1:]:
        league = league.findAll("div", {"class": "board"})
        for temp in league:
            link = f"https://www.iva.org.il/{temp.findNext('a', href=True)['href']}"
            leagues.append(urlopen(link))
    return leagues


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


def print_teams(teams_list: list):
    teams_list.sort(key=operator.itemgetter('score'), reverse=True)
    print("קבוצה                   |     נקודות  ")
    print("_________________________________________________")
    for team in teams_list:
        print(f"   {team['name']}          |        {team['score']}")

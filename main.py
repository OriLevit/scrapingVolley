from urllib.request import urlopen
from bs4 import BeautifulSoup


house1 = urlopen('https://www.iva.org.il/league.asp?LeagueId=2094&cYear=2023&lang=')
house2 = urlopen('https://www.iva.org.il/league.asp?LeagueId=2095&cYear=2023')
soup = BeautifulSoup(house1, "html.parser")
list_items = soup.find_all("tr")
teams = []

for team in list_items[1:]:
    team_name = team.findNext("td", {"class": "sticky-col"}).findNext("a").text
    info = team.findAll()
    team_formate = {
        "name": team_name[4:len(team_name)],
        "score": info[-1].text
    }
    teams.append(team_formate)

print("קבוצה                   |     נקודות  ")
print("_________________________________________________")
for team in teams[:8]:
    print(f"   {team['name']}          |        {team['score']}")
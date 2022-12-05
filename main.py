from urllib.request import urlopen
import soup_manager
from tqdm import tqdm

league_table = urlopen('https://www.iva.org.il/boards.asp')

all_leagues_links = soup_manager.get_leagues(league_table)
all_teams = []

for link in tqdm(all_leagues_links, bar_format='{l_bar}{bar:100}', desc="Gathering teams"):
    soup_manager.get_teams(link, all_teams)

soup_manager.print_teams(all_teams)


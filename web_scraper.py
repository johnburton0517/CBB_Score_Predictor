# written by John Burton
# Web scraper for sports-reference.com, college basketball advanced stats

import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.sports-reference.com/cbb/seasons/2024-advanced-school-stats.html'
opp_url = "https://www.sports-reference.com/cbb/seasons/2024-advanced-opponent-stats.html"

r = requests.get(url)
opp_r = requests.get(opp_url)

soup = BeautifulSoup(r.text, 'html.parser')
opp_soup = BeautifulSoup(opp_r.text, 'html.parser')

# get the table
table = soup.find('table', {'id': 'adv_school_stats'})
opp_table = opp_soup.find('table', {'id': 'adv_opp_stats'})

table_headers = ['School Name', 'G Overall', 'W Overall', 'L Overall','W-L% Overall', 'SRS Overall', 'SOS Overall',
                'Conf. W', 'Conf. L',
                'Home W', 'Home L',
                'Away W', 'Away L',
                'Points Tm.', 'Points Opp',
                'Pace', 'ORtg', 'FTr', '3PAr', 'TS%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'eFG%', 'TOV%', 'ORB%', 'FT/FGA']

opp_table_headers = ['School Name', 'G Overall', 'W Overall', 'L Overall','W-L% Overall', 'SRS Overall', 'SOS Overall',
                'Conf. W', 'Conf. L',
                'Home W', 'Home L',
                'Away W', 'Away L',
                'Points Tm.', 'Points Opp',
                'Pace', 'Opp. ORtg', 'Opp. FTr', 'Opp. 3PAr', 'Opp. TS%', 'Opp. TRB%', 'Opp. AST%', 'Opp. STL%', 'Opp. BLK%', 'Opp. eFG%', 'Opp. TOV%', 'Opp. ORB%', 'Opp. FT/FGA']


# scrape the table body 
table_body = table.find('tbody')
opp_table_body = opp_table.find('tbody')

# get the table rows
table_rows = table_body.find_all('tr')
opp_table_rows = opp_table_body.find_all('tr')

# get the table data
table_data = []
opp_table_data = []

for row in table_rows:
    data = []
    for td in row.find_all('td'):
        if td.text == '':
            continue
        data.append(td.text)
    table_data.append(data)

for row in opp_table_rows:
    data = []
    for td in row.find_all('td'):
        if td.text == '':
            continue
        data.append(td.text)
    opp_table_data.append(data)


# write data to a csv file
with open('cbb_advanced_stats.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(table_headers)
    writer.writerows(table_data)

with open('cbb_opponent_stats.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(opp_table_headers)
    writer.writerows(opp_table_data)
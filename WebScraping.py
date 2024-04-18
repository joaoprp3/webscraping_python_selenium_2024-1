import time 
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json

# 1. Pegar o conteúdo Html a partir da URL
url ="https://www.nba.com/stats/players/traditional?PerMode=Totals&dir=A&sort=PTS"
top10ranking = {}

rankings = {
    '3points': {'field': 'FG3M', 'label': '3PM'},
    'Points': {'field': 'PTS', 'label': 'PTS'},
    'Assistants': {'field': 'AST', 'label': 'AST'},
    'Rebounds': {'field': 'REB', 'label': 'REB'},
    'Steals': {'field': 'STL', 'label': 'STL'},
    'Blocks': {'field': 'BLK', 'label': 'BLK'},
}

def buildrank(type):

    field = rankings[type]['field']
    label = rankings[type]['label']

    driver.find_element_by_xpath(
        f"//div[@class='Crom_container__C45Ti crom-container']//table/thead/tr/th[@field='{field}']").click()

    element =  driver.find_element_by_xpath("//div[@class='Crom_container__C45Ti crom-container']//table")
    html_content = element.get_attribute('outerHTML')

    #. Parsear o conteúdo HTML - BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')

    #. Estruturaro contúdo em um Data Frame - Pandas
    df_full = pd.read_html( str(table) )[0].head(10)
    df = df_full[['Unnamed: 0', 'Player', 'Team', label]]
    df.columns = ['Pos', 'Player', 'Team', 'Total']

    #. Transformar os Dados em um Dicionário de dados Próprio
    return df.to_dict('records')

option = Options()
option.headless = True
driver = webdriver.Firefox()

driver.get(url)
time.sleep(5)


for k in rankings:
    top10ranking[k] = buildrank(k)

driver.quit()

# 5. Converter e salvar em um arquivo JSON
js = json.dumps(top10ranking)
fp = open('ranking.json', 'w')
fp.write(js)
fp.close()

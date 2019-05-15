import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import seaborn as sns



url = 'https://en.wikipedia.org/wiki/List_of_countries_by_past_and_future_population'
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')

tables = soup.find_all('table', {'class':'sortable'})

population = pd.DataFrame()
for table_dom in tables:
    headers = []
    for header in table_dom.find_all('th'):
        headers.append(header.contents[0])

    data = []
    for tag_tr in table_dom.find_all('tr'):
        row = []
        row_data = tag_tr.find_all('td')
        if row_data:
            for index in xrange(len(row_data)):
                if index == 0:
                    row.append(row_data[index].find('a').contents[0])
                else:
                    row.append(row_data[index].contents[0])

        if row:
                data.append(row)

    table_data = pd.DataFrame.from_records(np.array(data[:-1], dtype=object), columns = headers)

    population = pd.concat([population, table_data], axis = 1)

cols = [c for c in population.columns if c[0]== '%']
population = population.drop(columns = cols, axis = 1)
population = population.T.drop_duplicates().T
population['country_name'] = population['Country (or dependent territory)']
population = population.set_index('country_name')
population = population.drop(columns=['Country (or dependent territory)'], axis=1)
population = population.astype(str)
population = population.replace({',': ''}, regex=True)
population = population.astype(int)

import matplotlib.ticker as tkr
from collections import defaultdict

world_population = defaultdict()
for col in population.columns:
    world_population[col] = population[col].sum()

world_population = pd.DataFrame(data=world_population, index=['World'])

world = world_population.loc['World']
plt.plot(world.index, world / 1000000, label=world.name)
plt.xticks(rotation=45)
plt.ylim(ymin=0)
plt.xlabel('Year')
plt.ylabel('# People (billions)')
plt.title('World population in general from 1950 - 2050')
plt.show()

# sns.set_context('talk')

# pop_1950 = round(world_population['1950']/1000000, 2)
# pop_2015 = round(world_population['2015']/1000000, 2)
# pop_2050 = round(world_population['2050']/1000000, 2)
# ax = sns.barplot(x=['1950', '2015', '2050'],
#                  y=[pop_1950, pop_2015, pop_2050])


# world_population.plot(color='red', xticks = world, yticks = year)
# plt.title('World population in general from 1950 - 2050')
# plt.xlabel('Year')
# plt.ylabel('# People (billions)')
# plt.show()




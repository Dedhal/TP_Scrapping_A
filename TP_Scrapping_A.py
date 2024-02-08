from tkinter.ttk import Separator
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

url = 'https://apolloarchive.com/aparch_crews.html'

res = requests.get(url)

# execute JavaScript

soup = BeautifulSoup(res.content, 'html.parser')

print(soup.prettify())

# Extract the table
table = soup.find_all('table')[0]

titles = table.find_all('th')

print(titles[0])

titles = titles[1:]

for i, title in enumerate(titles):
    print(i, title)

# traite le titre de la première colonne
titles[0].font.decompose()
titles[0] = str(titles[0]).replace('<br/>', ' ')
titles[0] = BeautifulSoup(titles[0], 'html.parser').text
titles[0] = titles[0].strip()

# traite le titre de la deuxième colonne
titles[1] = titles[1].font
titles[1] = str(titles[1]).split('<br/>')
titles[1] = [BeautifulSoup(title, 'html.parser').text for title in titles[1]]

# traite le titre de la troisième colonne
titles[2] = titles[2].find('font', {'size': '-1'}).text

# développe les colonnes
titles[0] = [titles[0]]
titles[2] = [titles[2]]
titles = sum(titles, [])

print(titles)

# cherche les cases de la table
content = table.find_all('td')

print('-'*50)

print(content)

print('-'*50)


tmp = []
tmp_crew = []
tmp_backup = []

# formatage des données
for i, c in enumerate(content):
    if i % 3 == 0:
        tmp.append(c.text.replace('\n', ' ').strip())
    elif i % 3 == 1:
        for cleaned in c.find_all('font', {'size': '-2'}):
            cleaned.extract()
        tmp_ = c.find_all('font', {'size': '-1'})
        for i, t in enumerate(tmp_):
            tmp_[i] = t.text.strip().split('\n')
            for e in tmp_[i]:
                if e == '':
                    tmp_[i].remove(e)
                else:
                    tmp_[i] = [e.strip() for e in tmp_[i]]
                    
        tmp_crew.append(tmp_)
    else:
        tmp_ = c.find('font', {'size': '-2'})
        tmp_ = tmp_.get_text(separator='\n')
        tmp_ = tmp_.split('\n')
        
        tmp_ = [e.split('<font size="-2">')[0].strip() for e in tmp_]
        
        for e in tmp_:
            if e == '' or '(deceased)' in e:
                tmp_.remove(e)
            else:
                tmp_ = [e.strip() for e in tmp_]
                
        tmp_backup.append(tmp_)
        
for i, t in enumerate(tmp_crew):
    tmp_crew[i] = sum(t, [])
    
for i, t in enumerate(tmp_backup):
    for j, e in enumerate(t):
        if e == '':
            tmp_backup[i].pop(j)

print('-'*50)

print(tmp)
print(tmp_crew)
print(tmp_backup)

print('-'*50)

res_dict = []

# création du dictionnaire final
for n, c, b in zip(tmp, tmp_crew, tmp_backup):
    res_dict.append({titles[0]: n, "Prime Crew": {titles[1]: c[0], titles[2]: c[1], titles[3]: c[2]}, titles[4]: b})
    
print(res_dict)

# sauvegarde du dictionnaire
with open('apollo_missions.json', 'w') as f:
    json.dump(res_dict, f, indent=4)



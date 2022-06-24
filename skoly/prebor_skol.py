# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# @author jmacura 2018
from csv import reader
from pprint import pprint
import sys

# Parse command line params
usage = """Pouziti: prebor_skol.py -f "soubor.csv"
Moznosti:
  -f "Prebor2018vysl.csv"  Cesta k souboru s vysledky
"""

fname = "testovaci_zavod_vysledky.csv"
if len(sys.argv) == 3:
     if(str(sys.argv[1]) == '-f'):
         fname = sys.argv[2]
else:
    print(usage)
    quit()

def printRes(category):
    fh.write("{}  {:<20} {:>41} {:>10}\n".format("Pořadí", "Název školy", "Body", "Čas"))
    for i,t in enumerate(category):
        #fh.write(" {:>3}    {:<40} {:<15} {:>4}\n".format(i+1, t[1], teams[t[1]], t[0]))               
        fh.write(" {:>3}    {:<40} {:<15} {:>4} {:>11}\n".format(i+1, t[1], teams[t[1]], t[0], t[0])) 
        #fh.write(" {:>3}    {:<40} {:<15} {:>4}\n".format(i+1, t[1], teams[t[1]], teams[t[2]], t[0]))               


# Nacteni vstupnich dat
i = -1
headers = []
data = []
important = ["Surname", "First name", "Time", "Classifier", "City", "Short", "Pl"]
with open(fname) as fh:
    for row in reader(fh, delimiter=";"):
        i += 1
        if i == 0:
            for cell in row:
                headers.append(cell)
        else:
            #print("==={}===".format(i))
            row_dict = {}
            for j,cell in enumerate(row):
                #print(headers[j])
                #print(len(cell.strip()), cell)
                if len(cell.strip()) > 0 and headers[j] in important and headers[j] not in row_dict.keys() :
                    row_dict[headers[j]] = cell
            data.append(row_dict.copy())
            #print(row_list[headers[57]])
        #if i > 5:
            #break
#pprint(data)
no_racers = len(data)
print("Nacteno {} zavodniku".format(no_racers))

# Ulozeni skol do slovniku spolu s jejich mesty
teams = {}
for x in data:
    #if x['City'] not in teams.keys():        
        #teams[x['City']] = x['City'] if 'City' in x.keys() else ""
        teams[x['City']] = ""
print("Nalezeno {} škol".format(len(teams.keys())))

#pprint(teams)

# Ulozeni kategorii do seznamu
cats = []
for x in data:
    if x['Short'] not in cats:
        cats.append(x['Short'])
print("Nalezeno {} kategorii".format(len(cats)))

# Kategorie vcetne jejich obsazeni
team_num = {cat : [] for cat in cats} # vytvoreni prazdneho slovniku
for x in data:
    cat = x['Short']
    team = x['City']
    if team not in team_num[cat]:
        team_num[cat].append(team)

# Zjisteni obsazenosti jednotlivych kategorii pocitanych spolecne pro vychozi bodovou znamku
team_max_3 = 0
team_max_5 = 0
team_max_79 = 0
team_max_S = 0
team_max = 0
max_cat = None
for x in team_num.keys():    
   if (x == "D3" or x == "H3") and (len(team_num[x]) > team_max_3):         
          team_max_3 = len(team_num[x])
          
   if (x == "D5" or x == "H5") and (len(team_num[x]) > team_max_5):         
          team_max_5 = len(team_num[x])                                        
   
   if (x == "D7" or x == "H7" or x == "D9" or x == "H9") and (len(team_num[x]) > team_max_79):         
          team_max_79 = len(team_num[x])
          
   if (x == "DS" or x == "HS") and (len(team_num[x]) > team_max_S):         
          team_max_S = len(team_num[x])                   
  
   if len(team_num[x]) > team_max:
          team_max = len(team_num[x])
          max_cat = x

          
print("Maximum skol je v kategorii {}: {} skol".format(max_cat, team_max))                            
print("Maximum skol v kategorii DH3: {} skol".format(team_max_3))
print("Maximum skol v kategorii DH5: {} skol".format(team_max_5))
print("Maximum skol v kategorii DH79: {} skol".format(team_max_79))
print("Maximum skol v kategorii DHS: {} skol".format(team_max_S))

prev_place = 0
points_mem = 0
equ_cnt = 0
# Vypocet bodu u zavodniku
data = [x for x in data if x['Classifier'] == '0'] # vyhodit DISK zavodniky, uz nejsou potreba
for cat in cats:
    team_score = {t: 0 for t in teams.keys()}
    points = 0
    if cat == "D3" or cat == "H3":
      points = team_max_3*2
    elif cat == "D5" or cat == "H5":
      points = team_max_5*2
    elif cat == "D7" or cat == "H7" or cat == "D9" or cat == "H9":
      points = team_max_79*2
    elif cat == "DS" or cat == "HS":
      points = team_max_S*2

    for x in data:
        if x['Short'] == cat:
            x['Time']=sum(x * int(t) for x, t in zip([3600, 60, 1], x['Time'].split(":"))) # prepocitat cas na sekundy                                                      
            if x['Pl'] == prev_place : 
               equ_cnt += 1 # pocitej zavodniky se stejnym umistenim
            else :
               equ_cnt = 0
            if team_score[x['City']] < 2:
                if x['Pl'] == prev_place and equ_cnt > 0:
                   x['Points'] = points_mem
                else : 
                   x['Points'] = points
                team_score[x['City']] += 1
                points_mem = x['Points']; # uloz body pro prideleni zavodnikum se stejnym umistenim
                points -= 1
                #pprint(x)
                #pprint(prev_place)                
            else: 
               if equ_cnt == 0:               
                  points_mem = points;  # uloz body pro prideleni zavodnikum se stejnym umistenim
               x['Points'] = 0            
            prev_place = x['Pl']
            #pprint(x)
            #pprint(prev_place)
            #pprint(points_mem)
            #pprint(points)
            #pprint(equ_cnt)
#pprint(data)

# Vypocet bodu u druzstev
hd3 = {}
hd5 = {}
hd79 = {}
hd7 = {}
hd9 = {}
hds = {}
for x in data:
    if x['Short'] == "D3" or x['Short'] == "H3":
        if x['City'] in hd3.keys():
            hd3[x['City']] += x['Points']
        else:
            hd3[x['City']] = x['Points']
    elif x['Short'] == "D5" or x['Short'] == "H5":
        if x['City'] in hd5.keys():
            hd5[x['City']] += x['Points']
        else:
            hd5[x['City']] = x['Points']    
            
    elif x['Short'] == "D7" or x['Short'] == "H7":
        if x['City'] in hd7.keys():
            hd7[x['City']] += x['Points']
        else:
            hd7[x['City']] = x['Points']
            
    elif x['Short'] == "D9" or x['Short'] == "H9":
        if x['City'] in hd9.keys():
            hd9[x['City']] += x['Points']
        else:
            hd9[x['City']] = x['Points']            
                        
    elif x['Short'] == "DS" or x['Short'] == "HS":
        if x['City'] in hds.keys():
            hds[x['City']] += x['Points']
        else:
            hds[x['City']] = x['Points']
    #else:
        #print("Neznámá kategorie {} u závodníka/ice {} {}".format(x['Short'], x['First name'], x['Surname']))

    if x['Short'] == "D7" or x['Short'] == "H7" or x['Short'] == "D9" or x['Short'] == "H9":
        if x['City'] in hd79.keys():
            hd79[x['City']] += x['Points']
        else:
            hd79[x['City']] = x['Points']
        
#pprint(hd3)
#pprint(hd5)
#pprint(hd7)
#pprint(hd9)
#pprint(hd79)
#pprint(hds)

# Serazeni skol podle bodu
hd3i = sorted([(hd3[x], x) for x in hd3], reverse = True)
#pprint(hd3i)
hd5i = sorted([(hd5[x], x) for x in hd5], reverse = True)
#pprint(hd5i)
hd79i = sorted([(hd79[x], x) for x in hd79], reverse = True)
#pprint(hd79i)
hd7i = sorted([(hd7[x], x) for x in hd7], reverse = True)
#pprint(hd7i)
hd9i = sorted([(hd9[x], x) for x in hd9], reverse = True)
#pprint(hd9i)
hdsi = sorted([(hds[x], x) for x in hds], reverse = True)
#pprint(hdsi)

# Vypis vysledku do souboru
with open("vysledky_skoly.txt", 'w', encoding="utf-8") as fh:
    fh.write("{} závodníků\n{} škol\n{} kategorií\n".format(no_racers, len(teams.keys()), len(cats)))
    #fh.write("Nejvíce škol v jedné kategorii je {} (kat. {})\n".format(team_max, max_cat))    
    fh.write("Maximum bodů v kategorii DH3: {}\n".format(team_max_3*2))
    fh.write("Maximum bodů v kategorii DH5: {}\n".format(team_max_5*2))
    fh.write("Maximum bodů v kategorii DH79: {}\n".format(team_max_79*2))
    fh.write("Maximum bodů v kategorii DHS: {}\n".format(team_max_S*2))
    fh.write("\n==== D3 + H3 ====\n")
    printRes(hd3i)
    fh.write("\n==== D5 + H5 ====\n")
    printRes(hd5i)
    fh.write("\n==== D7 + H7 ====\n")
    printRes(hd7i)
    fh.write("\n==== D9 + H9 ====\n")
    printRes(hd9i)    
    fh.write("\n==== D7 + H7 + D9 + H9 ====\n")
    printRes(hd79i)
    fh.write("\n==== DS + HS ====\n")
    printRes(hdsi)
print("\nVysledky preboru ulozeny do souboru \"vysledky_skoly.txt\"")


with open("vysledky_body.csv", 'w', encoding="utf-8") as fhb:
    fhb.write("Kategorie;Jméno;Škola;Pořadí;Body;Čas\n".format(x['Short'],x['Surname'], x['First name'], x['City'],x['Points'],x['Time']))
    for x in data:
       #if (x['Points'] > 0):                           
         fhb.write("{}; {} {};{};{};{};{}\n".format(x['Short'],x['Surname'], x['First name'], x['City'],x['Pl'],x['Points'], x['Time']))

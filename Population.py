import json
import requests
import os
import sqlite3

API_KEY = "b9d13880c708393576c4e77042fc6643e4fb0be8"

def create_request_url(city_num, state_num):
    url = f"https://api.census.gov/data/2020/dec/pl?get=P1_001N&for=place:{city_num}&in=state:{state_num}&key={API_KEY}"
    return url

def create_population_dict():
    cityData_list = [("New York","New York","36","51000") , ("Los Angeles","California", "06", "44000") , ("Seattle","Washington","53","63000") , ("Chicago","Illinois","17","14000") , ("Houston","Texas","48","35000") , ("Dallas","Texas","48","19000") , ("Austin","Texas","48","05000") , ("San Francisco","California","06","67000") , ("Denver","Colorado","08","20000"), ("Boston","Massachusetts","25","07000") , ("Cincinnati","Ohio","39","15000") , ("Miami","Florida","12","45000") , ("San Diego","California","06","66000") , ("Tucson","Arizona","04","77000") , ("Salt Lake City","Utah","49","67000"), ("Urban Honolulu", "Hawaii","15","71550") , ("Portland", "Oregon","41","59000") , ("Detroit","Michigan","26","22000") , ("Sacramento","California","06","64000") , ("San Jose","California","06","68000") , ("New Orleans","Louisiana","22","55000") , ("Atlanta","Georgia","13","04000") , ("Minneapolis","Minnesota","27","43000") , ("Orlando","Florida","12","53000") , ("Phoenix","Arizona","04","55000") , ("Erick city", "Oklahoma","40","24200") , ("Erin Springs town", "Oklahoma","40","24300") , ("Etowah town", "Oklahoma","40","24460") , ("Etta CDP", "Oklahoma","40","24500") , ("Eufaula city", "Oklahoma","40","24650") , ("Evening Shade CDP", "Oklahoma","40","24762") , ("Fairfax town", "Oklahoma","40","24850") , ("Fairfield CDP", "Oklahoma","40","24875") , ("Fairland town", "Oklahoma","40","24900") , ("Fairmont town", "Oklahoma","40","24950") , ("Fair Oaks town", "Oklahoma","40","25000") , ("Fairview city", "Oklahoma","40","25100") , ("Fallis town", "Oklahoma","40","25250") , ("Fanshawe town", "Oklahoma","40","25400") , ("Fargo town", "Oklahoma","40","25450") , ("Faxon town","Oklahoma","40","25650") , ("Fay CDP", "Oklahoma","40","25700") , ("Felt CDP", "Oklahoma","40","25850") , ("Finley CDP", "Oklahoma","40","26000") , ("Fittstown CDP", "Oklahoma","40","26200") , ("Fitzhugh town", "Oklahoma","40","26250") , ("Fletcher town", "Oklahoma","40","26350") , ("Flint Creek CDP", "Oklahoma","40","26415") , ("Flute Springs CDP", "Oklahoma","40","26525") , ("Foraker town", "Oklahoma","40","26750") , ("Forest Park town", "Oklahoma","40","26850") , ("Forgan town", "Oklahoma","40","26900") , ("Fort Cobb town", "Oklahoma","40","27100") , ("Fort Coffee town", "Oklahoma","40","27150") , ("Fort Gibson town", "Oklahoma","40","27200") , ("Fort Supply town", "Oklahoma","40","27350") , ("Fort Towson town","Oklahoma","40","27400") , ("Foss town", "Oklahoma","40","27450") , ("Foster town", "Oklahoma","40","27500") , ("Fox CDP", "Oklahoma","40","27550") , ("Foyil town", "Oklahoma","40","27600") , ("Francis town", "Oklahoma","40","27650") , ("Frederick city", "Oklahoma","40","27800") , ("Freedom town", "Oklahoma","40","27850") , ("Friendship town", "Oklahoma","40","27900") , ("Gage town", "Oklahoma","40","28250") , ("Gans town", "Oklahoma","40","28350") , ("Garber city", "Oklahoma","40","28500") , ("Garvin town", "Oklahoma","40","28700") , ("Gate town", "Oklahoma","40","28800") , ("Geary city", "Oklahoma","40","28900") , ("Gene Autry town", "Oklahoma","40","28950") , ("Geronimo town", "Oklahoma","40","29100") , ("Gerty town", "Oklahoma","40","29150") , ("Gideon CDP", "Oklahoma","40","29300") , ("Glencoe town", "Oklahoma","40","29400") , ("Glenpool city", "Oklahoma","40","29600") , ("Golden CDP", "Oklahoma","40","29800") , ("Goldsby town", "Oklahoma","40","29850") , ("Goltry town", "Oklahoma","40","29900") , ("Goodwell town", "Oklahoma","40","30200") , ("Gore town", "Oklahoma","40","30300") , ("Gotebo town", "Oklahoma","40","30350") , ("Akron village", "Michigan","26","00700") , ("Alanson village", "Michigan","26","00860") , ("Alba CDP", "Michigan","26","00900") , ("Albion city", "Michigan","26","00980") , ("Alden CDP", "Michigan","26","01060") , ("Algonac city", "Michigan","26","01180") , ("Allegan city", "Michigan","26","01260") , ("Allen village", "Michigan","26","01300") , ("Allendale CDP", "Michigan","26","01340") , ("Allen Park city", "Michigan","26","01380") , ("Alma city", "Michigan","26","01540") , ("Almont village", "Michigan","26","01660") , ("Alpena city", "Michigan","26","01740") , ("Alpha village", "Michigan","26","01800") , ("Manistee city", "Michigan","26","50720") , ("Manistee Lake CDP", "Michigan","26","50755") , ("Stronach CDP", "Michigan","26","76820") , ("Fountain village", "Michigan","26","29940")]

    population_dict = {}
    id_count = 0
    for num in range(0,len(cityData_list)):
        url = create_request_url(cityData_list[num][3], cityData_list[num][2])
        r = requests.get(url)
        info = json.loads(r.text)
        population = info[1][0]
        population_dict[id_count] = population
        id_count += 1
    print(population_dict)
    return population_dict


def AV_create_database(population_dictionary,cur,conn):

    cur.execute("DROP TABLE IF EXISTS CityPopulations")
    cur.execute("CREATE TABLE IF NOT EXISTS CityPopulations (city TEXT,population INTEGER)")
    for item in population_dictionary:
        cur.execute("INSERT INTO CityPopulations (city,population) VALUES (?,?)",(item,population_dictionary.get(item)))
    conn.commit()


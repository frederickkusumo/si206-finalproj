import json
import requests
import os
import sqlite3

API_KEY = "b9d13880c708393576c4e77042fc6643e4fb0be8"

def create_request_url(city_num, state_num):
    url = f"https://api.census.gov/data/2020/dec/pl?get=P1_001N&for=place:{city_num}&in=state:{state_num}&key={API_KEY}"
    return url

def create_population_dict():
    cityData_list = [("New York","New York","36","51000") , ("Los Angeles","California", "06", "44000") , ("Seattle","Washington","53","63000") , ("Chicago","Illinois","17","14000") , ("Houston","Texas","48","35000") , ("Dallas","Texas","48","19000") , ("Austin","Texas","48","05000") , ("San Francisco","California","06","67000") , ("Denver","Colorado","08","20000"), ("Boston","Massachusetts","25","07000") , ("Cincinnati","Ohio","39","15000") , ("Miami","Florida","12","45000") , ("San Diego","California","06","66000") , ("Tucson","Arizona","04","77000") , ("Salt Lake City","Utah","49","67000"), ("Urban Honolulu", "Hawaii","15","71550") , ("Portland", "Oregon","41","59000") , ("Detroit","Michigan","26","22000") , ("Sacramento","California","06","64000") , ("San Jose","California","06","68000") , ("New Orleans","Louisiana","22","55000") , ("Atlanta","Georgia","13","04000") , ("Minneapolis","Minnesota","27","43000") , ("Orlando","Florida","12","53000") , ("Phoenix","Arizona","04","55000")]
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


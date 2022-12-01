import os
import sqlite3
import json
import api
import homeprice

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def read_json(cache_filename):
    try:
        with open(cache_filename,'r') as f:
            return json.loads(f.read())
    except:
        return {}

def write_json(cache_filename, dict):
    with open(cache_filename, 'w') as f:
        f.write(json.dumps(dict, indent = 4))

if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cache_filename = dir_path + '/' + "cache_file.json"
    city_list=['New York', 'Los Angeles', 'Seattle', 'Chicago', 'Houston', 'Dallas', 'Austin', 'San Francisco', 'Denver', 'Boston', 'Cincinnati', 'Miami', 'San Diego', 'Tucson', 'Salt Lake City', 'Honolulu', 'Portland', 'Detroit', 'Sacramento', 'San Jose', 'New Orleans', 'Atlanta', 'Minneapolis', 'Orlando', 'Phoenix']
    [api.get_data_using_cache(list, cache_filename) for list in city_list]
    cur, conn = setUpDatabase('city_id.db')
    api.create_cities_table(cur, conn)
    api.add_AirQ_from_json(city_list,'cache_file.json', cur, conn)
    cities = ['NewYork', 'LosAngeles', 'Seattle', 'Chicago', 'Houston', 'Dallas', 'Austin', 'SanFrancisco', 'Denver', 
        'Boston', 'Cincinnati', 'Miami', 'SanDiego', 'Tucson', 'SaltLakeCity', 'Honolulu', 'Portland', 'Detroit', 
        'Sacramento', 'SanJose', 'NewOrleans', 'Atlanta', 'Minneapolis', 'Orlando', 'Phoenix']
        
    data = homeprice.get_detailed_info(cities)
    homeprice.add_prices_from_info(cur, conn, data)
    avg = homeprice.avgprices(cur, conn, data)
    homeprice.tocsv(avg, 'average_home_price.csv')

    x = api.joinData(cur,conn)
    api.write_csv(x,"AirQuailyAvg.csv")
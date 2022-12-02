import os
import sqlite3
import json
import api
import homeprice
import plotly.express as px
import plotly.graph_objects as go
import Population

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
    avg = homeprice.avgprices(cur, conn, "home_prices", "Home_Price", "Home_Price.city_id")
    homeprice.tocsv(avg, 'average_home_price.csv')
    cities_list = []
    avgprice_list = []
    api.read_csvTo2list("average_home_price.csv",cities_list,avgprice_list)

    x = homeprice.avgprices(cur,conn,"pm25","Air_quality", "Air_quality.city_id")
    api.write_csv(x,"AirQuailyAvg.csv")
    city_list=[]
    aq_list=[]
    api.read_csvTo2list("AirQuailyAvg.csv",city_list,aq_list)

    
    fig = px.bar(x=city_list, y=avgprice_list, color=aq_list, color_continuous_scale='bluered')
    fig.show()

    api.graph2(cur,conn)

    population_dictionary = Population.create_population_dict()
    Population.AV_create_database(population_dictionary,cur,conn)

import os
import sqlite3
import json
import api
import homeprice
import plotly.express as px
import plotly.graph_objects as go

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
    cities_list = []
    avgprice_list = []
    api.read_csvTo2list("average_home_price.csv",cities_list,avgprice_list)

    # x = api.joinDataAVG(cur,conn)
    # api.write_csv(x,"AirQuailyAvg.csv")
    # city_list=[]
    # aq_list=[]
    # api.read_csvTolist("AirQuailyAvg.csv",city_list,aq_list)

    
    # fig = px.bar(x=city_list, y=aq_list, color=aq_list, color_continuous_scale='bluered')
    # fig.show()

    #Graph Two (NY-LA)
    v = api.NYjoinData(cur,conn)
    api.write_csv3(v,"NYAirQuailyDaily.csv")
    NY_city_list=[]
    NY_date_list=[]
    NY_aq_list=[]
    api.read_csvTo3list("NYAirQuailyDaily.csv",NY_city_list,NY_date_list,NY_aq_list)

    v = api.LAjoinData(cur,conn)
    api.write_csv3(v,"LAAirQuailyDaily.csv")
    LA_city_list=[]
    LA_date_list=[]
    LA_aq_list=[]
    api.read_csvTo3list("LAAirQuailyDaily.csv",LA_city_list,LA_date_list,LA_aq_list)

    NYdifLA_list=[]
    for i in range(len(NY_city_list)):
        different = NY_aq_list[i]-LA_aq_list[i]
        NYdifLA_list.append(different)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=NY_date_list, y=NY_aq_list))
    fig.add_trace(go.Scatter(x=LA_date_list, y=LA_aq_list))
    fig.add_trace(go.Scatter(x=LA_date_list, y=NYdifLA_list))
    fig.show()
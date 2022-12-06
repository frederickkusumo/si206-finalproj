import os
import sqlite3
import api
import homeprice
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import Population

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

if __name__ == '__main__':
    # try:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cache_filename = dir_path + '/' + "cache_file.json"
    city_list=['New York', 'Los Angeles', 'Seattle', 'Chicago', 'Houston', 'Dallas', 'Austin', 'San Francisco', 'Denver', 'Boston', 'Cincinnati', 'Miami', 'San Diego', 'Tucson', 'Salt Lake City', 'Honolulu', 'Portland', 'Detroit', 'Sacramento', 'San Jose', 'New Orleans', 'Atlanta', 'Minneapolis', 'Orlando', 'Phoenix']

    lst = [api.get_data_using_cache(list) for list in city_list]
    cur, conn = setUpDatabase('city_id.db')
    api.create_cities_table(cur, conn)
    api.add_AirQ_from_json(city_list,lst, cur, conn)

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
    
    fig1 = px.bar(x=cities_list, y=avgprice_list)
    fig1.update_layout(title="Average Home Prices", xaxis_title="Cities", yaxis_title="Home Prices")
    
    x = homeprice.avgprices(cur,conn,"pm25","Air_quality", "Air_quality.city_id")
    api.write_csv(x,"AirQuailyAvg.csv")
    city_list=[]
    aq_list=[]
    api.read_csvTo2list("AirQuailyAvg.csv",city_list,aq_list)
    
    # fig2 = px.bar(x=city_list, y=avgprice_list, color=aq_list, color_continuous_scale='bluered')
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig2.add_trace(go.Bar(x=city_list, y=avgprice_list, name="yaxis values"),secondary_y=False)
    fig2.add_trace(go.Scatter(x=city_list, y=aq_list, name="yaxis2 values"),secondary_y=True,)
    # fig2.update_layout(title="Average Air Quality vs Average Home Prices", xaxis_title="Cities", yaxis_title="Home Prices")
    fig2.update_layout(title_text="Average Air Quality vs Average Home Prices")
    fig2.update_xaxes(title_text="Cities")
    fig2.update_yaxes(title_text="Average Home Price", secondary_y=False)
    fig2.update_yaxes(title_text="Average AQI", secondary_y=True)

    fig3=api.graph2(cur,conn)
        
    population_tup_list = Population.create_population_dict()
    Population.AV_create_database(population_tup_list,cur,conn)
    population_CSV_data = Population.AV_csv_data(cur)
    Population.AV_write_csv(population_CSV_data, 'CityPopulation.csv')
    pop_list = []
    city = []
    api.read_csvTo2list("CityPopulation.csv",city,pop_list)

    fig4 = make_subplots(specs=[[{"secondary_y": True}]])
    fig4.add_trace(go.Bar(x=city_list, y=avgprice_list, name="yaxis values"),secondary_y=False)
    fig4.add_trace(go.Bar(x=city_list, y=pop_list, name="yaxis2 values"), secondary_y=True,)
    fig4.update_layout(title_text="Average Home Price vs Population")
    fig4.update_xaxes(title_text="Cities")
    fig4.update_yaxes(title_text="Average Home Price", secondary_y=False)
    fig4.update_yaxes(title_text="Population", secondary_y=True)

    fig5 = px.bar(x=cities_list, y=pop_list)
    fig5.update_layout(title="Populations", xaxis_title="Cities", yaxis_title="Population")

    if fig1 and fig2 and fig3 and fig4 and fig5:
        fig1.show()
        fig2.show()
        fig3.show()
        fig4.show()
        fig5.show()
    # except:
    #     print("TRY AGAIN!")
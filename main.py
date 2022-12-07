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
    dir_path = os.path.dirname(os.path.realpath(__file__))
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
    
    x = homeprice.avgprices(cur,conn,"pm25","Air_quality", "Air_quality.city_id")
    api.write_csv(x,"AirQuailyAvg.csv")
    city_list=[]
    aq_list=[]
    api.read_csvTo2list("AirQuailyAvg.csv",city_list,aq_list)
    
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    fig1.add_trace(go.Bar(x=city_list, y=avgprice_list, name="Average Home Price", marker_color='lightslategrey'),secondary_y=False)
    fig1.add_trace(go.Scatter(x=city_list, y=aq_list, name="Average AQI", marker=dict(size=10), mode='markers',marker_color='crimson'),secondary_y=True,)
    fig1.update_layout(title_text="Average Air Quality vs Average Home Prices")
    fig1.update_xaxes(title_text="Cities")
    fig1.update_yaxes(title_text="Average Home Price", secondary_y=False)
    fig1.update_yaxes(title_text="Average AQI", secondary_y=True)

    fig2=api.graph2(cur,conn)
        
    population_tup_list = Population.create_population_dict()
    Population.AV_create_database(population_tup_list,cur,conn)
    population_CSV_data = Population.AV_csv_data(cur)
    Population.AV_write_csv(population_CSV_data, 'CityPopulation.csv')
    pop_list = []
    city = []
    api.read_csvTo2list("CityPopulation.csv",city,pop_list)

    fig3= (go.Figure(
    data=[
        go.Bar(name='Average Home Price', x=city_list, y=avgprice_list, yaxis='y', marker_color='lightslategrey', offsetgroup=1),
        go.Bar(name='Average AQI', x=city_list, y=pop_list, yaxis='y2', marker_color='crimson', offsetgroup=2)
    ],
    layout={
        'xaxis':  {'title': 'Cities'},
        'yaxis': {'title': 'Average Home Price'},
        'yaxis2': {'title': 'Population', 'overlaying': 'y', 'side': 'right'}
    }
    ))
    fig3.update_layout(title_text="Average Home Price vs Population", barmode='group')

    d = dict(zip(cities_list, pop_list))
    sd = sorted(d.items(), key = lambda x: x[1])
    c = []
    p = []
    for i in sd:
        c.append(i[0])
        p.append(i[1])
    fig4 = px.bar(x=c, y=p)
    fig4.update_layout(title="Populations", xaxis_title="Cities", yaxis_title="Population")

    fig5 = make_subplots(specs=[[{"secondary_y": True}]])
    fig5.add_trace(go.Bar(x=city_list, y=pop_list, name="Population", marker_color='lightslategrey'),secondary_y=False)
    fig5.add_trace(go.Scatter(x=city_list, y=aq_list, name="Average AQI", marker=dict(size=10), mode='markers',marker_color='crimson'),secondary_y=True,)
    fig5.update_layout(title_text="Average Air Quality vs Population")
    fig5.update_xaxes(title_text="Cities")
    fig5.update_yaxes(title_text="Population", secondary_y=False)
    fig5.update_yaxes(title_text="Average AQI", secondary_y=True)

    if fig1 and fig2 and fig3 and fig4 and fig5:
        fig1.show()
        fig2.show()
        fig3.show()
        fig4.show()
        fig5.show()
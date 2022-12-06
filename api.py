import requests
import json
import csv
import plotly.express as px
import plotly.graph_objects as go

def get_request_url(list):
    url = f'https://api.waqi.info/feed/{list}/?token=3a04f5d06b3d0ec8317f0e97d4a6054a4a3d01fb'
    return url

def get_data_using_cache(list):
    dict = {}
    url = get_request_url(list)
    print(f"Fetching data for {list}")
    try:
        x = requests.get(url).text
        # print(x)
        y = json.loads(x)
        # print(y)
        if y["status"] == "ok":
            dict[url] = y["data"]
            return dict.get(url)
        else:
            print("No list found for list name provided")
            return None
    except:
        print("Exception")
        return None

def create_cities_table(cur, conn):

    cities = ['New York', 'Los Angeles', 'Seattle', 'Chicago', 'Houston', 'Dallas', 'Austin', 'San Francisco', 'Denver', 'Boston', 'Cincinnati', 'Miami', 'San Diego', 'Tucson', 'Salt Lake City', 'Honolulu', 'Portland', 'Detroit', 'Sacramento', 'San Jose', 'New Orleans', 'Atlanta', 'Minneapolis', 'Orlando', 'Phoenix']

    cur.execute("DROP TABLE IF EXISTS Cities")
    cur.execute("CREATE TABLE Cities (id INTEGER PRIMARY KEY, city TEXT)")
    for i in range(len(cities)):
        cur.execute("INSERT INTO Cities (id,city) VALUES (?,?)",(i,cities[i]))
    conn.commit()

def add_AirQ_from_json(list,data, cur, conn):
    dic = {}
    raw_name_list = []
    for n in data:
        raw_name = n["city"]["name"]
        raw_name_list.append(raw_name)
        dic[raw_name]={}

        for i in n["forecast"]["daily"]["pm25"]:
            raw_pm25 = i['avg']
            raw_date = i['day']
            dic[raw_name].update({raw_date:raw_pm25})
    data = []
    for i in dic:
        print(i)
        for name in list:
            if name in i:
                raw_name = str(list.index(name))
            elif i == "Chi_sp, Illinois, USA":
                raw_name = '3'
            elif i == "CAMP, Colorado, USA":
                raw_name = '8'
            elif i == "Taft, Ohio, USA":
                raw_name = '10'
            elif i == "Geronimo, Pima County, USA":
                raw_name = '13'
            elif i == "Windsor":
                raw_name = '17'
            elif i == "United Ave., Georgia, USA":
                raw_name = '21'
            elif i == "Lake Isle Estates - Winter Park, Orange, Florida, USA":
                raw_name = '23'
        for date,aq in dic[i].items():
            new = [raw_name,date,aq]
            data.append(new)
    cur.execute('create table if not exists Air_quality(id INTEGER PRIMARY KEY, city_id TEXT, date TEXT, pm25 INTEGER)')
    try:
        count = cur.execute('SELECT id FROM Air_quality WHERE id = (SELECT MAX(id) FROM Air_quality)')
        count = cur.fetchone()
        count = count[0]
    except:
        count = 0
    id = 1
    for i in data[count:count+25]:
        var_id = id + count
        cur.execute('insert or ignore into Air_quality(id,city_id,date,pm25) values(?,?,?,?)',(var_id,i[0],i[1],i[2]))
        id += 1
    conn.commit()


def joinDataAVG(cur, conn):
    cur.execute("SELECT city, ROUND(AVG(pm25), 2) FROM Air_quality JOIN Cities ON Air_quality.city_id = Cities.id GROUP BY city_id ORDER BY citygit")
    # cur.execute("SELECT city, ROUND(AVG(home_prices), 2) FROM Home_Price JOIN Cities ON Home_Price.city_id = Cities.id GROUP BY city_id")
    x = cur.fetchall()
    return(x)


def write_csv(data, filename):
    first_row = ["City", "Avg Air Quality"]
    with open(filename, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(first_row)
        writer.writerows(data)
        
def read_csvTo2list(filename,city_list,aq_list):
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        next(reader)
        for i in reader:
            if len(i) > 0:
                city_list.append(i[0])
                aq_list.append(float(i[1]))
    #     data = list(reader)
    # for i in data[1:]:
    #     city_list.append(i[0])
    #     aq_list.append(float(i[1]))
        return city_list,aq_list 

def NYjoinData(cur, conn):
    x = cur.execute("SELECT Cities.city, Air_quality.date,Air_quality.pm25 FROM Air_quality JOIN Cities ON Air_quality.city_id = Cities.id AND Air_quality.city_id = 0")
    return x

def LAjoinData(cur, conn):
    y = cur.execute("SELECT Cities.city, Air_quality.date,Air_quality.pm25 FROM Air_quality JOIN Cities ON Air_quality.city_id = Cities.id AND Air_quality.city_id = 1")
    return y

def write_csv3(data, filename):
    first_row = ["City", "Date","Air Quality"]
    with open(filename, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(first_row)
        writer.writerows(data)

def read_csvTo3list(filename,city_list,date_list,aq_list):
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    for i in data[1:]:
        city_list.append(i[0])
        date_list.append(i[1])
        aq_list.append(float(i[2]))
    return city_list,date_list,aq_list 


def graph2(cur,conn):
    #Graph Two (NY-LA)
    v = NYjoinData(cur,conn)
    write_csv3(v,"NYAirQuailyDaily.csv")
    NY_city_list=[]
    NY_date_list=[]
    NY_aq_list=[]
    read_csvTo3list("NYAirQuailyDaily.csv",NY_city_list,NY_date_list,NY_aq_list)

    v = LAjoinData(cur,conn)
    write_csv3(v,"LAAirQuailyDaily.csv")
    LA_city_list=[]
    LA_date_list=[]
    LA_aq_list=[]
    read_csvTo3list("LAAirQuailyDaily.csv",LA_city_list,LA_date_list,LA_aq_list)

    NYdifLA_list=[]
    for i in range(len(NY_city_list)):
        different = NY_aq_list[i]-LA_aq_list[i]
        NYdifLA_list.append(different)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=NY_date_list, y=NY_aq_list,name = "NY"))
    fig.add_trace(go.Scatter(x=LA_date_list, y=LA_aq_list,name = "LA"))
    fig.add_trace(go.Scatter(x=LA_date_list, y=NYdifLA_list,name = "NYvsLA"))
    fig.update_layout(title="A week Air Quality change of NY vs LA", xaxis_title="Cities", yaxis_title="Air Quality")
    return (fig)
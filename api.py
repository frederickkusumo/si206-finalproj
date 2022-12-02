import requests
import json
import unittest
import os
import sqlite3
import main
import csv


def get_request_url(list):
    url = f'https://api.waqi.info/feed/{list}/?token=3a04f5d06b3d0ec8317f0e97d4a6054a4a3d01fb'
    # r = requests.get(url).text
    # data = json.loads(r)
    return url

def get_data_using_cache(list, cache_filename):
    '''
    Uses the passed search generate a request_url using
    the 'get_request_url' function

    If url is found in the dict return by `read_json`, prints
    "Using cache for {list}" and returns the url results

    If url is not found in the dict return by `read_json`, prints
    "Fetching data for {list}" and makes a call to Books API to
    get the data the search

    If request is successful, add the data to a dictionary (key is
    the request_url, and value is part of the results) and writes
    out the dictionary to cache using `write_json`

    Parameters
    ----------
    list: str
        a string the name of the best seller list to search in the Books API. ex: hardcover-fiction
    cache_filename: str
        the name of the file to write a cache to
    
    Returns
    -------
    url result:
        results of a url request either from the cache or website
    None:
        if search is unsuccessful
    '''
    dict = main.read_json(cache_filename)
    url = get_request_url(list)
    if url in dict:
        print(f"Using cache for {list}")
        return dict[url]
    else:
        print(f"Fetching data for {list}")
        try:
            x = requests.get(url).text
            # print(x)
            y = json.loads(x)
            # print(y)
            if y["status"] == "ok":
                dict[url] = y["data"]
                main.write_json(cache_filename,dict)
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

def add_AirQ_from_json(list,filename, cur, conn):
    # WE GAVE YOU THIS TO READ IN DATA
    f = open(filename)
    file_data = f.read()
    f.close()
    json_data = json.loads(file_data)
    dic = {}
    for i in list:
        url = get_request_url(i)
        raw_name=json_data[url]["city"]["name"]
        if i in raw_name:
            raw_name = list.index(i)
        else:
            if raw_name == "Chi_sp, Illinois, USA":
                raw_name = "3"
            elif raw_name == "CAMP, Colorado, USA":
                raw_name = "8"
            elif raw_name == "Taft, Ohio, USA":
                raw_name = "10"
            elif raw_name == "Geronimo, Pima County, USA":
                raw_name = "13"
            elif raw_name == "Windsor":
                raw_name = "17"
            elif raw_name == "United Ave., Georgia, USA":
                raw_name = "21"
            elif raw_name == "Lake Isle Estates - Winter Park, Orange, Florida, USA":
                raw_name = "23"
        dic[raw_name]={}
        for i in json_data[url]["forecast"]["daily"]["pm25"]:
            raw_pm25 = i['avg']
            raw_date = i['day']
            dic[raw_name][raw_date]=raw_pm25 
    data = []
    for i in dic:
        for n,m in dic[i].items():
            new = [i,n,m]
            data.append(new)
        # cur.execute(f'SELECT id FROM Cities WHERE city LIKE %{i}%')
    # cur.execute('create table if not exists Air_quality')
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
    # x = cur.execute("SELECT Cities.city, Air_quality.date, Air_quality.pm25, Home_Price.home_prices FROM Air_quality JOIN Cities ON Air_quality.city = Cities.id JOIN Home_Price ON Home_Price.city_id = Cities.id")
    # x = cur.execute("SELECT Cities.city, (AVG(Air_quality.pm25) FROM Air_quality where city = ) FROM Air_quality JOIN Cities ON Air_quality.city = Cities.id")
    cur.execute("SELECT CITIES.city, ROUND(AVG(Air_quality.pm25), 2) FROM Air_quality JOIN Cities ON Air_quality.city_id = Cities.id GROUP BY city_id")
    x = cur.fetchall()
    # count = 0
    # for i in x:
    #     print(i)
    #     count += 1
    #     dic[i[0]] = (dic.get(i[0], 0) + i[1])
    print("AVG:", x)
    return x

def write_csv(data, filename):
    first_row = ["City", "Avg Air Quality"]
    with open(filename, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(first_row)
        writer.writerows(data)
        
def read_csvTo2list(filename,city_list,aq_list):
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    for i in data[1:]:
        city_list.append(i[0])
        aq_list.append(float(i[1]))
    return city_list,aq_list 

def NYjoinData(cur, conn):
    x = cur.execute("SELECT Cities.city, Air_quality.date,Air_quality.pm25 FROM Air_quality JOIN Cities ON Air_quality.city = Cities.id AND Air_quality.city = 0")
    return x

def LAjoinData(cur, conn):
    y = cur.execute("SELECT Cities.city, Air_quality.date,Air_quality.pm25 FROM Air_quality JOIN Cities ON Air_quality.city = Cities.id AND Air_quality.city = 1")
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
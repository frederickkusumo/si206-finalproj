import requests
import json
import unittest
import os
import sqlite3

def read_json(cache_filename):
    try:
        with open(cache_filename,'r',encoding='utf-8') as file:
            return json.loads(file.read())
    except:
        data = {}
        return data

def get_request_url(list):
    url = f'https://api.waqi.info/feed/{list}/?token=3a04f5d06b3d0ec8317f0e97d4a6054a4a3d01fb'
    # r = requests.get(url).text
    # data = json.loads(r)
    return url

def write_json(cache_filename, dict):
    f = open(cache_filename,'w')
    data = json.dumps(dict, indent=4)
    f.write(data)
    f.close()

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
    dict = read_json(cache_filename)
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
                write_json(cache_filename,dict)
                return dict.get(url)
            else:
                print("No list found for list name provided")
                return None
        except:
            print("Exception")
            return None

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

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
        dic[raw_name]={}
        for i in json_data[url]["forecast"]["daily"]["pm25"]:
            raw_pm25 = i['avg']
            raw_date = i['day']
            dic[raw_name][raw_date]=raw_pm25
        # cur.execute(f'SELECT id FROM Cities WHERE city LIKE %{i}%')
    cur.execute('drop table if exists Air_quality')
    cur.execute('create table Air_quality(id INTEGER PRIMARY KEY, city TEXT, date TEXT, pm25 INTEGER)')
    id=0
    for i in dic:
        # cur.execute('insert into Air_quality(id,city) values(?,?)',(id,i))
        for n,m in dic[i].items():
            cur.execute('insert into Air_quality(id,city,date,pm25) values(?,?,?,?)',(id,i,n,m))
            id+=1
    conn.commit()

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cache_filename = dir_path + '/' + "cache_file.json"
    # city_list=['newyork','los angeles','seattle','Chicago','Houston']
    city_list=['New York', 'Los Angeles', 'Seattle', 'Chicago', 'Houston', 'Dallas', 'Austin', 'San Francisco', 'Denver', 'Boston', 'Cincinnati', 'Miami', 'San Diego', 'Tucson', 'Salt Lake City', 'Honolulu', 'Portland', 'Detroit', 'Sacramento', 'San Jose', 'New Orleans', 'Atlanta', 'Minneapolis', 'Orlando', 'Phoenix']
    [get_data_using_cache(list, cache_filename) for list in city_list]
    cur, conn = setUpDatabase('city_id.db')
    create_cities_table(cur, conn)
    add_AirQ_from_json(city_list,'cache_file.json', cur, conn)


main()
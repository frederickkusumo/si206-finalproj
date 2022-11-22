from xml.sax import parseString
from bs4 import BeautifulSoup
import os
import main
import json

def get_price_info(html_file):
    source_dir = os.path.dirname(__file__) 
    full_path = os.path.join(source_dir, html_file)
    file = open(full_path,'r')
    file_handle = file.read()
    file.close()

    soup = BeautifulSoup(file_handle, 'html.parser')
    price = soup.find_all('span', {'data-test':"property-card-price"})
    first_ten = [int(i.text.replace('$', '').replace(',', '').replace('+', ''))  for i in price[:9]]
    avg = round(sum(first_ten)/len(first_ten), 2)
    first_ten.append(avg)
    moreinfo = {}
    count = 1
    for i in first_ten[:-1]:
        moreinfo['home_price_'+str(count)] = i
        count += 1
    moreinfo['avg'] = first_ten[-1]
    return moreinfo

def get_detailed_info(cities):
    data = {}
    for i in cities:
        city = get_price_info('html_files/'+i+'.html')
        data[i] = city
    return data

def add_prices_from_json(cur, conn, file):
    f = open(file)
    file_data = f.read()
    f.close()
    data = json.loads(file_data)

    cur.execute('DROP TABLE IF EXISTS Home_Price')
    cur.execute('CREATE TABLE Home_Price(city_id INTEGER PRIMARY KEY, home_price_1 INTEGER, home_price_2 INTEGER, \
        home_price_3 INTEGER, home_price_4 INTEGER, home_price_5 INTEGER, home_price_6 INTEGER, \
            home_price_7 INTEGER, home_price_8 INTEGER, home_price_9 INTEGER, average_home_price NUMBER)')
    count = 0
    for i in data:
        cur.execute("INSERT INTO Home_Price (city_id, home_price_1, home_price_2, home_price_3, home_price_4, home_price_5, \
            home_price_6, home_price_7, home_price_8, home_price_9, average_home_price) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (count, data[i]['home_price_1'], data[i]['home_price_2'], data[i]['home_price_3'], data[i]['home_price_4'], \
                data[i]['home_price_5'], data[i]['home_price_6'], data[i]['home_price_7'], data[i]['home_price_8'], \
                    data[i]['home_price_9'], data[i]['avg']))
        count += 1
    conn.commit()

if __name__ == '__main__':
    cities = ['NewYork', 'LosAngeles', 'Seattle', 'Chicago', 'Houston', 'Dallas', 'Austin', 'SanFrancisco', 'Denver', 
        'Boston', 'Cincinnati', 'Miami', 'SanDiego', 'Tucson', 'SaltLakeCity', 'Honolulu', 'Portland', 'Detroit', 
        'Sacramento', 'SanJose', 'NewOrleans', 'Atlanta', 'Minneapolis', 'Orlando', 'Phoenix']
    data = get_detailed_info(cities)
    main.write_json('prices_dataset.json', data)
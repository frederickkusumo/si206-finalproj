from xml.sax import parseString
from bs4 import BeautifulSoup
import os
import csv

def get_price_info(html_file):
    source_dir = os.path.dirname(__file__) 
    full_path = os.path.join(source_dir, html_file)
    file = open(full_path,'r')
    file_handle = file.read()
    file.close()

    soup = BeautifulSoup(file_handle, 'html.parser')
    price = soup.find_all('span', {'data-test':"property-card-price"})
    first_ten = [int(i.text.replace('$', '').replace(',', '').replace('+', ''))  for i in price[:9]]
    # avg = round(sum(first_ten)/len(first_ten), 2)
    # first_ten.append(avg)
    return first_ten

def get_detailed_info(cities):
    data = []
    city_id = 0
    for i in cities:
        city = get_price_info('html_files/'+i+'.html')
        for x in city:
            new = (city_id, x)
            data.append(new)
        city_id += 1
    return data

def add_prices_from_info(cur, conn, data):
    cur.execute('CREATE TABLE IF NOT EXISTS Home_Price (id INTEGER PRIMARY KEY, city_id INTEGER, home_prices INTEGER)')
    try:
        count = cur.execute('SELECT id FROM Home_Price WHERE id = (SELECT MAX(id) FROM Home_Price)')
        count = cur.fetchone()
        count = count[0]
    except:
        count = 0
    id = 1
    for i in data[count:count+25]:
        var_id = id + count
        cur.execute("INSERT OR IGNORE INTO Home_Price (id, city_id, home_prices) VALUES (?,?,?)", (var_id, i[0], i[1]))
        id += 1
    conn.commit()

def avgprices(cur, conn, data):
    cur.execute("SELECT city, ROUND(AVG(home_prices), 2) FROM Home_Price JOIN Cities ON Home_Price.city_id = Cities.id GROUP BY city_id")
    rows = cur.fetchall()
    return rows

def tocsv(data, file):
    with open(file, 'w') as f:
        writer = csv.writer(f)
        header = ['Cities', 'avg_home_price']
        writer.writerow(header)
        for info in data:
            writer.writerow(info)

if __name__ == '__main__':
    cities = ['NewYork', 'LosAngeles', 'Seattle', 'Chicago', 'Houston', 'Dallas', 'Austin', 'SanFrancisco', 'Denver', 
        'Boston', 'Cincinnati', 'Miami', 'SanDiego', 'Tucson', 'SaltLakeCity', 'Honolulu', 'Portland', 'Detroit', 
        'Sacramento', 'SanJose', 'NewOrleans', 'Atlanta', 'Minneapolis', 'Orlando', 'Phoenix']
    data = get_detailed_info(cities)
    # add_prices_from_info(data)
    # main.write_json('prices_dataset.json', data)
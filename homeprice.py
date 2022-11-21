from xml.sax import parseString
from bs4 import BeautifulSoup
import os
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

def write_json(filename, data):
    with open(filename, 'w') as f:
        f.write(json.dumps(data, indent = 4))

def add_to_sql():
    pass

if __name__ == '__main__':
    cities = ['NewYork', 'LosAngeles', 'Seattle', 'Chicago', 'Houston', 'Dallas', 'Austin', 'SanFrancisco', 'Denver', 
        'Boston', 'Cincinnati', 'Miami', 'SanDiego', 'Tucson', 'SaltLakeCity', 'Honolulu', 'Portland', 'Detroit', 
        'Sacramento', 'SanJose', 'NewOrleans', 'Atlanta', 'Minneapolis', 'Orlando', 'Phoenix']
    data = get_detailed_info(cities)
    write_json('Frederick/cities_dataset.json', data)
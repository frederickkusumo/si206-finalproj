import json
import unittest
import os
import requests
import extracode


API_KEY = "b9d13880c708393576c4e77042fc6643e4fb0be8"


def get_request_url(city_num, state_num):
    #city_num = int(city_num)
    #state_num = int(state_num) May run into trouble with state ids that begin with 0. If state_num is an int it drops the 0 from the front
    url = f"https://api.census.gov/data/2020/dec/pl?get=P1_001N&for=consolidated%20city:{city_num}&in=state:{state_num}&key={API_KEY}"

    return url
def get_data_using_cache(city, city_id, state_id, cache_filename):

    url = get_request_url(city_id, state_id)
    d = extracode.read_json(cache_filename)
    if url in d:
        print(f'Using cache for {city}')
        return d[url]
    else:
        print(f"Fetching data for {city}")
        try:
            r = requests.get(url)
            info = json.loads(r.text)
            print(r)
            if info['status'] == 'OK':
                d[url] = info['results']
                extracode.write_json(cache_filename,d)
                return d.get(url)
            else:
                print("No list found for list name provided")
                return None
        except:
            print("Exception")
            return None

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    city_cache_file = dir_path + '/' + "cache_citypopulations.json"
    cityData_list = [("New York","New York","36","51000") , ("Los Angeles","California", "06", "44000") , ("Seattle","Washington","53","63000") , ("Chicago","Illinois","17","14000") , ("Houston","Texas","48","35000") , ("Dallas","Texas","48","19000") , ("Austin","Texas","48","05000") , ("San Francisco","California","06","67000") , ("Denver","Colorado","08","20000"), ("Boston","Massachusetts","25","07000") , ("Cincinnati","Ohio","39","15000") , ("Miami","Florida","12","45000") , ("San Diego","California","06","66000") , ("Tucson","Arizona","04","77000") , ("Salt Lake City","Utah","49","67000"), ("Urban Honolulu", "Hawaii","15","71550") , ("Portland", "Oregon","41","59000") , ("Detroit","Michigan","26","22000") , ("Sacramento","California","06","64000") , ("San Jose","California","06","68000") , ("New Orleans","Louisiana","22","55000") , ("Atlanta","Georgia","13","04000") , ("Minneapolis","Minnesota","27","43000") , ("Orlando","Florida","12","53000") , ("Phoenix","Arizona","04","55000")]

    for num in range(0,len(cityData_list)):
        #API_URL = get_request_url(cityData_list[num][3], cityData_list[num][2])
        get_data_using_cache(cityData_list[num][0],cityData_list[num][3], cityData_list[num][2],city_cache_file)


main()



from xml.sax import parseString
from bs4 import BeautifulSoup
import os

def get_price_info(html_file):
    source_dir = os.path.dirname(__file__) 
    full_path = os.path.join(source_dir, html_file)
    file = open(full_path,'r')
    file_handle = file.read()
    file.close()

    soup = BeautifulSoup(file_handle, 'html.parser')
    price = soup.find_all('span', {'data-test':"property-card-price"})
    prices = [int(i.text.strip('$ ')) for i in price]
    first_ten = prices[:10]
    avg = round(sum(first_ten)/len(first_ten), 2)
    first_ten.append(avg)
    return first_ten

def get_detailed_info(html_file):
    pass

if __name__ == '__main__':
    la = get_price_info("html_files/LA.html")
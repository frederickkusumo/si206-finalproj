import os
import sqlite3
import json

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def read_json(cache_filename):
    try:
        with open(cache_filename,'r') as f:
            return json.loads(f.read())
    except:
        return {}

def write_json(cache_filename, dict):
    with open(cache_filename, 'w') as f:
        f.write(json.dumps(dict, indent = 4))
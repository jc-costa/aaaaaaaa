import json
import os
from pathlib import Path
import csv 

five_keys = ["marca", "modelo", "sistema operacional", "processador", "cor"]

homedir = str(Path.home())
download_folder = os.path.join(homedir, 'Desktop/Projeto-Recuperacao-de-Informacao')

path = os.path.join(download_folder, 'extractor/results')

filelist = [os.path.join(path, file) for file in os.listdir(path)]
filenames = os.listdir(path)

#using five keys to create a csv file
def create_csv(json_file, keys):
    with open(json_file, 'r') as f:
        data = json.load(f)
    #create a csv file
    with open('csv_file1.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        #write the keys
        writer.writerow(keys)
        #write the values in the csv file
        writer.writerow([data[key] for key in keys])

for filename, filepath in zip(filenames, filelist):
    try:
        with open(filepath, encoding='utf-8') as info_json:
            data = json.load(info_json)
            create_csv(data, five_keys)
    except:
        pass

#creating a csv with five keys in which the keys are columns and the values are rows
#using five keys to create a csv file from json file
#

#rename the keys in json file
def rename_key(json_file, key, new_key):  
    with open(json_file, 'r') as f:
        #load the json file
        data = json.load(f)
    #rename the key
    data[new_key] = data.pop(key)
    with open(json_file, 'w') as f:
        #dump the json file
        json.dump(data, f, indent=4)
        
five_keys = ["marca", "modelo", "sistema operacional", "processador", "cor"]




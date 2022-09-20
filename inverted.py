import os
import json
import pathlib as pl
import csv 

#path to the folder
path = pl.Path.home() / "Desktop/Projeto-Recuperacao-de-Informacao/extractor/results"

#list of files in the folder
files = os.listdir(path)

def rename_key(json_file, key, new_key):  
    with open(json_file, 'r') as f:
        #load the json file
        data = json.load(f)
    #rename the key
    data[new_key] = data.pop(key)
    with open(json_file, 'w') as f:
        #dump the json file
        json.dump(data, f, indent=4)

''' #loop through the files
for file in files:
    #open the file
    with open(path / file, "r") as f:
        #load the json file
        data = json.load(f)
        #print the data
        try:
            data = rename_key(path / file, "memoria ram:", "memoria:")
        except:
            pass
        #print(data)  '''
        
five_keys = ["marca", "modelo", "sistema operacional", "processador", "cor"]

#create a csv file from the json file in which the keys are the columns and the values are the rows

#open the csv file
with open("extractor.csv", "w") as f:
    #create a writer object
    writer = csv.writer(f)
    #write the header
    writer.writerow(five_keys)
    #loop through the files
    for file in files:
        #open the file
        with open(path / file, "r") as f:
            #load the json file
            data = json.load(f)
            #print the data
            ''' try:
                data = rename_key(path / file, "memoria ram:", "memoria:")
            except:
                pass '''
            #print(data)
            #create a list
            row = []
            #loop through the keys
            for key in five_keys:
                #append the values to the list
                row.append(data[key])
                print(data[key])
            #write the row
            writer.writerow(row)


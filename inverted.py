import pandas as pd
from pathlib import Path
import pickle
import json
import os
import csv 

five_keys = ["marca", "modelo", "sistema operacional", "processador", "cor"]

homedir = str(Path.home())
download_folder = os.path.join(homedir, 'Desktop/Projeto-Recuperacao-de-Informacao')

path = os.path.join(download_folder, 'extractor/results')

filelist = [os.path.join(path, file) for file in os.listdir(path)]
filenames = os.listdir(path)

appended_data = []

for filename, filepath in zip(filenames, filelist):
    try:
        with open(filepath, encoding='utf-8') as info_json:
            data = json.load(info_json)
            #select data using five keys and create a csv file
            data = {key: data[key] for key in five_keys}
            #create a pandas dataframe from dicionaries in a for loop
            df = pd.DataFrame(data, index=[0])
            #append the dataframes
            appended_data.append(df)
            #print(type(data))            
    except:
        pass

#create a csv from a list of pandas dataframes
def create_csv_from_list(list_of_dataframes):
    with open('csv_file2.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        #write the keys
        writer.writerow(list_of_dataframes[0].keys())
        #write the values in the csv file
        for df in list_of_dataframes:
            writer.writerow(df.values[0])

#concatenate the dataframes
appended_data = pd.concat(appended_data, ignore_index=True)
print(appended_data)
#create csv from pandas dataframe
appended_data.to_csv('csv_file4.csv', index=False)

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

#inverted index with the frequency of the term from a csv file
def inverted_index_with_frequency(csv_file):
    #read the csv file
    df = pd.read_csv(csv_file)
    #create a dictionary
    inverted_index = {}
    #iterate over the rows in the dataframe
    for index, row in df.iterrows():
        #iterate over the columns in the dataframe
        for column in df:
            #get the value in the cell
            value = row[column]
            #if the value is not null
            if pd.notnull(value):
                #if the value is not in the dictionary
                if value not in inverted_index:
                    #add the value in the dictionary
                    inverted_index[value] = {}
                #if the index of the row is not in the dictionary
                if index not in inverted_index[value]:
                    #add the index of the row in the dictionary
                    inverted_index[value][index] = 1
                else:
                    #add the frequency of the term
                    inverted_index[value][index] += 1
    #return the dictionary
    return inverted_index

inverted_index = inverted_index_with_frequency('csv_file4.csv')

#save the inverted index in a json file
#save_inverted_index(inverted_index, 'inverted_index.json')

#save inverted index in a binary file
with open('inverted_index.bin', 'wb') as f:
    pickle.dump(inverted_index, f)



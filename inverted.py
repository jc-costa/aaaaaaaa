import pandas as pd
from pathlib import Path
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
            #print(data)
            #create a pandas dataframe from dicionaries in a for loop
            df = pd.DataFrame(data, index=[0])
            #append the dataframes
            appended_data.append(df)
            #print(type(data))            
    except:
        pass
    
#tokenize list of value by hifen
def tokenize_hifen(value):
    #create a list
    list_of_values = []
    #iterate over the list
    for v in value:
        #if the value has hifen
        if '-' in v:
            #split the value
            v = v.split('-')
            #iterate over the list
            for i in v:
                #add the value in the list
                list_of_values.append(i)
        else:
            #add the value in the list
            list_of_values.append(v)
    #return the list
    return list_of_values

#tokanize values in a csv file
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
                #split the value in a list
                value = value.split()
                #tokenize the value by hifen
                value = tokenize_hifen(value)
                #iterate over the list
                for term in value:
                    term = term+"_"+column
                    #if the term is not in the dictionary
                    if term not in inverted_index:
                        #add the term in the dictionary
                        inverted_index[term] = {}
                    #if the index of the row is not in the dictionary
                    if index not in inverted_index[term]:
                        #add the index of the row in the dictionary
                        inverted_index[term][index] = 1
                    else:
                        #add the frequency of the term
                        inverted_index[term][index] += 1
    #return the dictionary
    return inverted_index

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
#print(appended_data)
#create csv from pandas dataframe
appended_data.to_csv('csv_file4.csv', index=False)

#renaming the keys in json file
def rename_key(json_file, key, new_key):  
    with open(json_file, 'r') as f:
        #load the json file
        data = json.load(f)
    #rename the key
    data[new_key] = data.pop(key)
    with open(json_file, 'w') as f:
        #dump the json file
        json.dump(data, f, indent=4)

#save inverted index in a json
def save_inverted_index_json(inverted_index):
    #open the json file
    with open('inverted_index.json', 'w') as f:
        #dump the inverted index in the json file
        json.dump(inverted_index, f, indent=4)

inverted_index = inverted_index_with_frequency('csv_file4.csv')

save_inverted_index_json(inverted_index)

#save a dictionary in a binary file 
def save_inverted_index_binary(inverted_index):
    #open the binary file
    with open('inverted_index_without_compreesion.bin', 'wb') as f:
        #write the inverted index in the binary file
        f.write(str(inverted_index).encode('utf-8'))
    f.close()

#save inverted index in a binary file

index_without = save_inverted_index_binary(inverted_index)

#load a dictionary from a binary file 
def load_inverted_index_binary():
    #open the binary file
    with open('inverted_index_without_compreesion.bin', 'rb') as f:
        #read the inverted index from the binary file
        inverted_index = f.read().decode('utf-8')
    f.close()
    #return the inverted index
    return inverted_index

#compress dictionary into binary file using variable byte encoding
def compress_dictionary_vbe(dictionary):
    with open('inverted_index_dic_vbe.bin', 'wb') as f:
        #write the length of the dictionary
        f.write(len(dictionary).to_bytes(4, byteorder='big'))
        #iterate over the dictionary
        for key, value in dictionary.items():
            #write the length of the key
            f.write(len(key).to_bytes(4, byteorder='big'))
            #write the key
            f.write(key.encode('utf-8'))
            #write the length of the value
            f.write(len(value).to_bytes(4, byteorder='big'))
            #iterate over the value
            for key2, value2 in value.items():
                #write the length of the key
                f.write(len(str(key2)).to_bytes(4, byteorder='big'))
                #write the key
                f.write(str(key2).encode('utf-8'))
                #write the length of the value
                f.write(len(str(value2)).to_bytes(4, byteorder='big'))
                #write the value
                f.write(str(value2).encode('utf-8'))
    f.close()

compress_dictionary_vbe(inverted_index)

#load a dictionary from a binary file encoded with variable byte encoding
def load_dictionary_vbe():
    #open the binary file
    with open('inverted_index_dic_vbe.bin', 'rb') as f:
        #read the length of the dictionary
        length = int.from_bytes(f.read(4), byteorder='big')
        #create a dictionary
        dictionary = {}
        #iterate over the length of the dictionary
        for i in range(length):
            #read the length of the key
            length_key = int.from_bytes(f.read(4), byteorder='big')
            #read the key
            key = f.read(length_key).decode('utf-8')
            #read the length of the value
            length_value = int.from_bytes(f.read(4), byteorder='big')
            #create a dictionary
            dictionary[key] = {}
            #iterate over the length of the value
            for j in range(length_value):
                #read the length of the key
                length_key2 = int.from_bytes(f.read(4), byteorder='big')
                #read the key
                key2 = f.read(length_key2).decode('utf-8')
                #read the length of the value
                length_value2 = int.from_bytes(f.read(4), byteorder='big')
                #read the value
                value2 = f.read(length_value2).decode('utf-8')
                #add the key and value in the dictionary
                dictionary[key][key2] = value2
    f.close()
    #return the dictionary
    return dictionary

query_vbe = load_dictionary_vbe()

##print(query_vbe)

''' #given a key and a dictionary, return a list with the key and the value
def get_key_value(key, dictionary):
    #create a list
    list_key_value = []
    #iterate over the dictionary
    for key2, value2 in dictionary.items():
        #if the key is equal to the key in the dictionary
        if key == key2:
            #add the key and the value in the list
            list_key_value.append(key2)
            list_key_value.append(value2)
    #return the list
    return list_key_value

teste = get_key_value('ate_processador', query_vbe)
print(teste) '''

#given a key and a dictionary, return the value
def get_value(key, dictionary):
    #iterate over the dictionary
    for key2, value2 in dictionary.items():
        #if the key is equal to the key in the dictionary
        if key == key2:
            #return the value
            return value2

teste = get_value('ate_processador', query_vbe)
print(teste)

import os.path

import pandas as pd

movie = pd.read_csv('database_1000/movie.csv')[['name']]
actor = pd.read_csv('database_1000/actor.csv')[['name', 'english_name']]
actor['name'] = actor['name'].str.strip()
actor['english_name'] = actor['english_name'].str.strip()
genre = pd.read_csv('database_250/genre.csv')[['name']]

# print(len(movie), movie.iloc[1]['name'])
# print(len(actor), actor.iloc[1]['name'], actor.iloc[1]['english_name'])
# print(len(genre), genre.iloc[1]['name'])

output_folder = './database_1000'

with open(f'{output_folder}/userdict_1000.txt', mode='w', encoding='utf-8') as f:
    for i in range(len(movie)):
        f.write(f'{movie.iloc[i]["name"]} nm\n')
    for i in range(len(actor)):
        f.write(f'{actor.iloc[i]["name"].replace("·", "")} nr\n')
        if type(actor.iloc[i]["english_name"]) == str:
            f.write(f'{actor.iloc[i]["english_name"].replace(" ", "")} nr\n')
        else:
            f.write(f'{str(actor.iloc[i]["english_name"]).replace(" ", "")} nr\n')
    for i in range(len(genre)):
        f.write(f'{genre.iloc[i]["name"]} ng\n')


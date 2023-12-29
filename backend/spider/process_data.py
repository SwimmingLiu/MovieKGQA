import pandas as pd

data_folder = './origin_data'
output_folder = './database_1000'


# =================  movie
def gen_movie():
    movie_column = ['id', 'name', 'rating', 'release_date', 'genre', 'director', 'image', 'introduction']
    movie = pd.read_csv(f'{data_folder}/movie_file.csv', header=None)
    movie.columns = movie_column
    movie['name'] = movie['name'].str.strip()

    # movie_column = ['id', 'name', 'introduction', 'rating', 'release_date', 'image']
    movie_final = movie[['id', 'name', 'introduction', 'rating', 'release_date', 'image']]
    movie_final.to_csv(f'{output_folder}/movie.csv', encoding='utf-8', index=False)


# =================  actor
def gen_actor():
    actor_column = ['id', 'name', 'gender', 'birthday', 'deathday', 'birthplace', 'image', 'biography', 'movie_id']
    actor = pd.read_csv(f'{data_folder}/actor_file.csv', header=None)
    actor.columns = actor_column

    actor[['name', 'english_name']] = actor['name'].str.split(n=1, expand=True)
    actor['name'] = actor['name'].str.strip()
    actor['english_name'] = actor['english_name'].str.strip()

    actor_column = ['id', 'name', 'english_name', 'birthplace', 'biography', 'birthday', 'deathday', 'image']
    actor_final = actor[actor_column]
    actor_final.loc[actor_final['deathday'].isna(), 'deathday'] = '\\N'

    actor_final.loc[:, 'name'] = actor_final['name'].str.replace("、", '')
    actor_final.loc[:, 'name'] = actor_final['name'].str.replace("·", '')
    actor_final.loc[:, 'birthplace'] = actor_final['birthplace'].str.strip('\'"')
    actor_final.loc[:, 'birthplace'] = actor_final['birthplace'].str.replace('[“”‘’\"]', '', regex=True)
    actor_final.loc[:, 'birthplace'] = actor_final['birthplace'].str.strip('"')
    actor_final.loc[:, 'birthday'] = actor_final['birthday'].str.strip('\'"')
    actor_final.loc[:, 'birthday'] = actor_final['birthday'].str.replace('"', '')
    actor_final = actor_final.drop_duplicates(subset=['name'])
    actor_final.to_csv(f'{output_folder}/actor.csv', index=False, encoding='utf-8')


# =================  genre  genre_column = ['id', 'name']
def gen_genre():
    movie_column = ['id', 'name', 'rating', 'release_date', 'genre', 'director', 'image', 'introduction']
    movie = pd.read_csv(f'{data_folder}/movie_file.csv', header=None)
    movie.columns = movie_column
    movie['name'] = movie['name'].str.strip()
    movie = movie[['id', 'genre']]
    # print(movie.head())
    # 将包含列表的字符串转换为实际的列表
    movie['genre'] = movie['genre'].apply(eval)
    # 使用 explode() 方法将列表中的元素展开成新行
    df_exploded = movie.explode('genre')
    # 使用 unique() 方法统计不重复的项
    unique_genres = df_exploded['genre'].unique()
    # print(unique_genres)
    data = {'id': [i for i in range(len(unique_genres))],
            'name': unique_genres}
    genre_column = pd.DataFrame(data)
    genre_column.to_csv(f'{output_folder}/genre.csv', index=False)


# movie_genre_column = ['movie_id', 'genre_id']
# =================  movie -> genre
def gen_movie_genre():
    movie_column = ['id', 'name', 'rating', 'release_date', 'genre', 'director', 'image', 'introduction']
    movie = pd.read_csv(f'{data_folder}/movie_file.csv', header=None)
    movie.columns = movie_column
    movie['genre'] = movie['genre'].apply(eval)
    movie_exploded = movie.explode('genre')
    movie_exploded = movie_exploded[['id', 'genre']]

    genre = pd.read_csv(f'{output_folder}/genre.csv')

    final_data = pd.merge(movie_exploded, genre, left_on='genre', right_on='name', how='left', suffixes=('_movie', '_genre'))
    movie_genre_column = final_data[['id_movie', 'id_genre']]

    # print(movie_genre_column.head())
    movie_genre_column.columns = ['movie_id', 'genre_id']
    movie_genre_column.to_csv(f'{output_folder}/movie_genre.csv', index=False)


# actor_movie_column = ['actor_id', 'movie_id']
# =====================  actor_movie_column
def gen_actor_movie():
    actor_column = ['id', 'name', 'gender', 'birthday', 'deathday', 'birthplace', 'image', 'biography', 'movie_id']
    actor = pd.read_csv(f'{data_folder}/actor_file.csv', header=None)
    actor.columns = actor_column
    actor = actor[['id', 'movie_id']]
    actor.columns = ['actor_id', 'movie_id']
    actor.to_csv(f'{output_folder}/actor_movie.csv', index=False)


if __name__ == '__main__':
    # gen_movie()
    gen_actor()
    # gen_genre()
    # gen_movie_genre()
    # gen_actor_movie()

import csv
import re

import requests
from bs4 import BeautifulSoup


class Movie:
    """
        Movie Object
    """
    total_movies = 0

    def __init__(self):
        self.id = Movie.total_movies
        Movie.total_movies += 1

        self.imgUrl = None
        self.name = None
        self.rating = None
        self.introduction = None
        self.releaseDate = []

        self.genre = []
        self.director = None
        self.actor = []

    def to_csv(self):
        return [self.id, self.name, self.rating, self.releaseDate, self.genre, self.director, self.imgUrl, self.introduction]


class Actor:
    """
        演员
    """
    total_actors = 0

    def __init__(self):
        self.id = Actor.total_actors
        Actor.total_actors += 1

        self.imgUrl = None
        self.name = None
        self.gender = None
        self.birth = None
        self.birthplace = None
        self.death = None
        self.biography = None

    def to_csv(self, movie_id):
        return [self.id, self.name, self.gender, self.birth, self.death, self.birthplace, self.imgUrl, self.biography, movie_id]


target_url = 'https://movie.douban.com/top250'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
}


# response = requests.get(url=target_url, headers=headers)
# html = response.text
#
# # 将文本内容保存到本地文件
# with open('douban-top250.htmlhtml', 'w', encoding='utf-8') as file:
#     file.write(html)

# status_code = response.status_code
# status_code = 200


def analysisDoubanTop250part25(html: requests.Response.text):
    """
    一页电影列表 25部
    :param html:
    :return: 一页电影中的所有电影详情url
    """
    soup = BeautifulSoup(html, 'html.parser')

    movies_info = soup.find('ol', class_='grid_view')
    image_list = movies_info.findAll(class_='pic')
    movies_url = []
    for image in image_list:
        a = image.findNext('a')
        movie_url = a['href']
        movies_url.append(movie_url)

    return movies_url


def analysisActor(html: requests.Response.text, movie: Movie):
    """
    单个演员
    :param html:
    :param movie:  演员信息 追加到这里面
    """
    # self.id = None
    # self.name = None
    # self.gender = None
    # self.birth = None
    # self.death = None
    # self.biography = None
    actor = Actor()

    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find('div', id='content')

    # 追加img
    imgUrl = content.find('div', class_='pic').find('img')['src']
    actor.imgUrl = imgUrl

    name = content.find_next('h1').text.strip()
    actor.name = name

    li_list = content.find('div', class_='info').find_all('li')
    for li in li_list:
        # gender
        if li.find_next('span').text.strip() == '性别':
            gender = li.text.split(':')[1].replace('\n', '').strip()
            actor.gender = gender
        if li.find_next('span').text.strip() == '出生日期':
            birth = li.text.split(':')[1].replace('\n', '').strip()
            actor.birth = birth

        if li.find_next('span').text.strip() == '生卒日期':
            date = li.text.split(':')[1].replace('\n', '').replace(' ', '').split('至')
            birth = date[0]
            death = date[1]
            actor.birth = birth
            actor.death = death

        if li.find_next('span').text.strip() == '出生地':
            birthplace = li.text.split(':')[1].replace('\n', '').strip()
            actor.birthplace = birthplace

    biographyEl = content.find('span', class_='short')

    bi = content.find('div', id='intro', class_='mod').find('div', class_='bd').find('span', class_='all hidden')
    if bi is not None:
        bi = bi.text.replace('<br>', '').replace("\n", '').strip()
    if biographyEl is not None:
        biography = replace_multiple_spaces(biographyEl.text.replace('<br>', '').replace("\n", '').strip())
    else:
        biography = replace_multiple_spaces(content.find('div', id='intro', class_='mod')
                                            .find('div', class_='bd').text
                                            .replace('<br>', '').replace("\n", '').strip())

    if bi is not None:
        actor.biography = bi
    else:
        actor.biography = biography

    movie.actor.append(actor)
    # 打印对象的属性信息
    # for key, value in actor.__dict__.items():
    #     print(f"{key}: {value}")


def replace_multiple_spaces(string):
    # 使用正则表达式将多个连续空格替换为一个空格
    pattern = re.compile(r'\s+')
    replaced_string = re.sub(pattern, ' ', string)
    return replaced_string


def analysisMovie(html: requests.Response.text, movie: Movie):
    """
        单部电影
    :param html:
    :param movie:
    """
    soup = BeautifulSoup(html, 'html.parser')
    # 23-12-10 追加imgUrl
    imgUrl = soup.find('div', {'id': 'content'}).find('div', {'id': 'mainpic'}).find('img')['src'].strip()
    movie.imgUrl = imgUrl
    # movie name
    title = soup.find('head').find('title').text.strip().split("(")[0]
    movie.name = title
    # movie rating
    rating = soup.find(class_='ll rating_num').text
    movie.rating = rating
    # movie introduction
    spanBox = soup.find(class_='related-info').find(class_='indent').find_all('span')
    introduction = None
    for span in spanBox:
        if span.get('property') == 'v:summary':
            introduction = replace_multiple_spaces(span.text.replace('<br>', '').replace('\n', '').strip())

    intro = soup.find(class_='related-info').find(class_='indent').find(class_='all hidden')
    if intro:
        intro = replace_multiple_spaces(intro.text.replace('<br>', '').replace('\n', '').strip())
        movie.introduction = intro
    else:
        movie.introduction = introduction

    movie_subject = soup.find('div', class_='subject clearfix')
    spanBox = movie_subject.find_all('span')
    for span in spanBox:
        # movie releaseDate
        if span.get('property') == 'v:initialReleaseDate':
            movie.releaseDate.append(span.text)
        # movie genre
        if span.get('property') == 'v:genre':
            movie.genre.append(span.text)

    li_list = soup.find('ul', class_='celebrities-list from-subject __oneline').find_all('li')
    for li in li_list:
        personName = li.find_all('span')[0].find('a').text.strip()
        roleName = li.find_all('span')[1].text.strip()
        # 导演
        if roleName == '导演':
            movie.director = personName
            continue
        # 演员
        a_url = li.find_next('a').get('href')
        response = requests.get(url=a_url, headers=headers)
        if response.status_code == 200:
            print(f'抓取演员页面成功')
            actor_html = response.text

            # 将文本内容保存到本地文件
            # with open('actor.html', 'r', encoding='utf-8') as file:
            #     file.read()
            # file.write(actor_html)

            analysisActor(actor_html, movie)
        else:
            print(f'status_code is {response.status_code}')

    # 打印对象的属性信息
    # for key, value in movie.__dict__.items():
    #     print(f"{key}: {value}")


def printMovieInfo(_movie: Movie):
    """
     打印对象的属性信息
    """
    for key, value in _movie.__dict__.items():
        if key == 'actor':
            print('[ ')
            for actor in value:
                for key1, value1 in actor.__dict__.items():
                    print(f"{key1}: {value1}")
            print(' ]')
            continue
        print(f"{key}: {value}")


# 将电影信息写入CSV文件
def write_movies_to_csv(movies, movie_file_name, actor_file_name):
    # return [self.id, self.name, self.rating, self.releaseDate, self.genre, self.director, self.introduction]
    with open(movie_file_name, 'a', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        # writer.writerow(['id', 'name', 'rating', 'releaseDate', 'genre', 'director', 'introduction'])
        for movie in movies:
            writer.writerow(movie.to_csv())
            for actor in movie.actor:
                write_actors_to_csv(actor, movie.id, actor_file_name)


def write_actors_to_csv(actor, movie_id, filename):
    # [self.id, self.name, self.gender, self.birth, self.death, self.biography, movie_id]
    with open(filename, 'a', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        # writer.writerow(['Name', 'Age', 'Gender'])
        writer.writerow(actor.to_csv(movie_id))


if __name__ == '__main__':
    # https://movie.douban.com/top250?start=75&filter=
    # 遍历Top250的所有页面
    for idx in range(10):
        if idx == 0:
            target_url = 'https://movie.douban.com/top250'
        else:
            target_url = f'https://movie.douban.com/top250?start={25 * idx}&filter='
        response = requests.get(url=target_url, headers=headers)
        html = response.text
        if response.status_code == 200:
            print(f'抓取part25页面成功')
            # with open("douban-top250.html", "r", encoding="utf-8") as file:
            #     html = file.read()
            # 解析Top250网页的一页 => 每个具体电影的url链接
            movies_url = analysisDoubanTop250part25(html)

            movies_list = []
            for movie_url in movies_url:
                movie = Movie()
                res = requests.get(url=movie_url, headers=headers)
                if res.status_code == 200:
                    print(f'抓取电影页面成功')
                    movie_html = res.text
                    # with open('movie.html', 'r', encoding='utf-8') as file:
                    #     # file.write(movie_detail.text)
                    #     movie_html = file.read()
                    #
                    analysisMovie(movie_html, movie)

                    movies_list.append(movie)
                    # break
                else:
                    print(f'status_code {res.status_code}')

            movie_file_name = 'movie_file_1000.csv'
            actor_file_name = 'actor_file_1000.csv'
            write_movies_to_csv(movies_list, movie_file_name, actor_file_name)

            print(f'解析第{idx + 1}页结束')
            # break

        # with open('actor.html', 'r', encoding='utf-8') as file:
        #     actor_html = file.read()
        #     # file.write(actor_html)
        #
        # analysisActor(actor_html, movie)

        else:
            print('response is not 200')

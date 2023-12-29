import os

from neo4j import GraphDatabase


class Database:
    """
    Neo4j 数据库访问层。

    管理数据库连接的生命周期，并提供查询接口。
    """

    def __init__(self):
        uri = 'bolt://localhost:7687/neo4j'
        user = 'neo4j'
        password = 'wl070919'

        try:
            self._driver = GraphDatabase.driver(uri, auth=(user, password))
            self._session = self._driver.session()
        except Exception as e:
            raise Exception("数据库连接失败") from e

    def close(self):
        try:
            self._session.close()
            self._driver.close()
        except Exception as e:
            raise Exception("数据库断开失败") from e

    def find_one(self, query: str, **parameters):
        result = self._session.run(query, parameters).single()
        return result.value() if result else None

    def find_many(self, query: str, **parameters):
        return self._session.run(query, parameters).value()

    def find_movie_img(self, query: str, **parameters):
        result = self._session.run(query, parameters)
        # 提取结果
        introduction = None
        image = None
        for record in result:
            introduction = record['m.introduction']
            image = record['m.image']
        return {'introduction': introduction,
                'image': image}

    def find_actor_img(self, query: str, **parameters):
        result = self._session.run(query, parameters)
        # 提取结果
        biography = None
        image = None
        for record in result:
            biography = record['a.biography']
            image = record['a.image']

        if biography is not None:
            return {'introduction': biography,
                    'image': image}
        else:
            return None


if __name__ == "__main__":
    # import dotenv
    #
    # dotenv.load_dotenv()

    database = Database()
    genres = database.find_actor_img(
        """
            MATCH (a:Actor)
            WHERE a.name = $actor_name
            RETURN a.biography, a.image
            Limit 1
        """,
        actor_name="葛优",
    )

    database.close()

    print(genres)

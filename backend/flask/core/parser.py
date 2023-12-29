import os

import jieba
import jieba.posseg as jp

# print(os.getcwd())
# USERDICT_PATH = os.path.join("..\\data", "userdict.txt")
USERDICT_PATH = 'data\\userdict.txt'

jieba.setLogLevel("ERROR")
jieba.load_userdict(USERDICT_PATH)


# 成龙 是 谁 ？   =》 关于演员的介绍  问题分类
# 拿到key ‘成龙’ ！词性！

class Parser:
    """
    语句解析器。

    从语句中解析出演员、电影和类型。
    """

    def __init__(self, sentence: str):
        self._pairs = jp.lcut(sentence)

        print(self._pairs)

    def _get_words_by_flag(self, flag: str):
        return [pair.word for pair in self._pairs if pair.flag == flag]

    @property
    def actors(self):
        return self._get_words_by_flag("nr")

    @property
    def movies(self):
        return self._get_words_by_flag("nm")

    @property
    def genres(self):
        return self._get_words_by_flag("ng")


if __name__ == "__main__":
    while True:
        sentence = input("请输入语句：").strip()
        parser = Parser(sentence)   # pair 先用jieba库进行分词操作
        print(f"解析成分：演员={parser.actors}，电影={parser.movies}，类型={parser.genres}")

import jieba
from jieba import posseg
from sklearn.feature_extraction.text import TfidfVectorizer


def jiebaTest():
    USERDICT_PATH = "userdict.txt"  # xxx 词性 格式的文件

    jieba.setLogLevel("ERROR")
    jieba.load_userdict(USERDICT_PATH)

    sentence = "成龙演了什么喜剧？"

    # 使用jieba.posseg 进行词性标注，提前 导入演员、电影和题材 所指定的词性
    pairs = posseg.lcut(sentence)
    print(pairs)


# 进行文本分类时，使用jieba.cut 进行分词能够提升分类效果！
# 已测试

# TF-IDF 词频TF-逆向文档频率IDF        逆向文档频率IDF为了惩罚无意义的词，例如的、了、我们、都 等等...
# 词频表示词出现的次数， 逆向文档频率是衡量一个词在整个文本集合中的重要程度  IDF = log(N/n) N=总的文档数，n=词出现的文档数
# 若n非常常见，极端N=n => log1 = 0 若 n = N/2 => log2 > 0  n出现的越少，越有区别性
# TF-IDF = TF x IDF  作用：一个词预测主题的能力
def tfidfTest():
    texts = ["大大 小小 大大 大大 嘻嘻 哈哈 梦想 张三", "小小 大大 大大 大大 哈哈 嘻嘻 李四", "嘻嘻 哈哈 小小 大大 大大 大大 王五"]
    # texts = ["This is the first document.", "This is the second document."]
    tf_idf = TfidfVectorizer()
    trans = tf_idf.fit_transform(texts)
    feature_list = tf_idf.get_feature_names_out()
    weight = trans.toarray()
    print(feature_list)
    print(weight)


#  训练数据使用占位符，或许时降低占位符对分类的影响？


if __name__ == '__main__':
    # jiebaTest()
    tfidfTest()


# QA System
# Question class
# 文本分类 成龙是谁？ => 预处理 [分词(使用空格间隔开) + TD-IDF向量化] => 分类模型 => 问题类型：演员简介
# 词性标注, 句子 => 分词+按照自定义的词性标，pair再拿出需要的标记, 此步骤的目的是拿到查询的key
# 根据问题和查询的key，在图数据库中进行查询

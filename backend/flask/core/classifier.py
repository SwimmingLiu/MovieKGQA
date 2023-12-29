import json
import os

import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# print(os.getcwd())
# TRAIN_DATASET_PATH = os.path.join("../data", "train.json")    # 单个文件run的目录和从app.py run 的目录不一样
TRAIN_DATASET_PATH = os.path.join("data", "train.json")

jieba.setLogLevel("ERROR")


# 在进行文本分类任务时，使用jieba对文本进行分词可以将复杂的句子拆分成独立的词汇，从而更好地表示句子的含义和特征
# 提高分类准确率   cut 是分词
def normalize(sentence: str):
    return " ".join(jieba.cut(sentence))


class BaseClassifier:
    """
    底层分类器。

    使用 TF-IDF 向量化文本，然后使用朴素贝叶斯预测标签。
    """

    def __init__(self):
        self._vectorizer = TfidfVectorizer()
        self._classifier = MultinomialNB(alpha=0.01)

    def _train(self, x: list, y: list):
        X = self._vectorizer.fit_transform(x).toarray()
        self._classifier.fit(X, y)

    def _predict(self, x: list):
        X = self._vectorizer.transform(x).toarray()
        return self._classifier.predict(X)


class Classifier(BaseClassifier):
    """
    问题分类器。

    根据问题中出现的关键词，将问题归于某一已知类别下。
    """

    def __init__(self):
        BaseClassifier.__init__(self)
        # question: 'nm简介' ...  label: 'introduce_by_movie ...
        questions, labels = Classifier._read_train_dataset()
        self._train(questions, labels)

    def classify(self, sentence: str):
        question = normalize(sentence)
        # question = sentence
        y = self._predict([question])
        return y[0]

    @staticmethod
    def _read_train_dataset():
        with open(TRAIN_DATASET_PATH, "r", encoding="utf-8") as fr:
            train_dataset: dict[str, list[str]] = json.load(fr)

        questions = []
        labels = []
        for label, sentences in train_dataset.items():
            questions.extend([normalize(sentence) for sentence in sentences])
            # questions.extend([sentence for sentence in sentences])
            labels.extend([label for _ in sentences])

        return questions, labels


if __name__ == "__main__":
    classifier = Classifier()

    while True:
        sentence = input("请输入问题：").strip()
        label = classifier.classify(sentence)
        print(f"问题分类：{label}")

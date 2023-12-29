- **flask**
  - ***core***
    - *classifier  问题分类，句子=>jieba分词，再按空格为间隔拼接在一起，转为TF-IDF向量=>喂入分类模型*
    - *database  连接Neo4j*
    - *parser  对句子进行词性标注(这里使用userdict作为自定义词性)，拿到查询的key*
    - *qa  汇合上述三个模块实现知识问答*
  - ***data***
    - *train.json  训练分类模型的数据*
    - *userdict  词性标注的文件*
  - ***test***
    - *词性标注和TF-IDF测试*
- **spider**

  - *generate_userdict.py  生成用户字典，作用：导入jieba进行词性标注，进而提取关键词*
  - *main_x.py  爬虫代码，生成movie.csv和actor.csv文件*
  - *process_data.py  根据爬虫结果，生成需要的文件，可将其导入至Neo4j*
  - *database_x  包含最终的结果文件和导入Neo4j的CQL语句*

​	


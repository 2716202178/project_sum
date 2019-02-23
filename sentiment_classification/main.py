# encoding:utf-8
import pandas as pd
import numpy as np
import re
import nltk
from nltk.tokenize import WordPunctTokenizer
from nltk.corpus import stopwords as pw
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import pos_tag
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV


#  读取文件
def readfile(file_name=""):
    if file_name is not None:
        pd.set_option("max_colwidth", 2000000)
        return pd.read_csv(file_name)


#  分词并去掉停用词
def sentence2words(sentence):
    words = WordPunctTokenizer().tokenize(sentence)
    if pw is None:
        nltk.download("stopwords")  # 下载停用词
    cache_stop_words = pw.words("english")

    words_with_lower = []  # 将分词转换成小写
    for i in words:
        words_with_lower.append(i.lower())
    words_without_stopwords = []

    for elem in words_with_lower:   # 去掉停用词
        if elem not in cache_stop_words:
            words_without_stopwords.append(elem)

    words_with_reduction = word_reduction(words_without_stopwords)
    return words_with_reduction


#  去掉数字标点和非字母字符
def clean_line(line2process=""):
    pat = re.compile('<[^>]+>', re.S)   # 去除</br>等标签
    line2process = pat.sub('', line2process)
    line2process = re.sub('[^A-Za-z]', ' ', line2process)  # 去除非英文字符
    return line2process


# 获取单词的词性
def get_wordnet_pos(tag):
    if wordnet is None:
        nltk.download('wordnet')
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


#  词形还原（如countries-->country）
def word_reduction(wordlist2lem):
    if wordnet is None:
        nltk.download('wordnet')
    tagged_sent = pos_tag(wordlist2lem)  # 获取单词的词性
    # print(tagged_sent)
    reduct_word_list = []
    wnl = WordNetLemmatizer()
    for tag in tagged_sent:
        wordnet_pos = get_wordnet_pos(tag[1]) or wordnet.NOUN
        reduct_word_list.append(wnl.lemmatize(tag[0], pos=wordnet_pos))  # 词形还原
    return reduct_word_list


# 单条review测试
def single_test(df2process):
    print(df2process.loc[2, "review"])
    line = df2process.loc[2, "review"]
    _line_after_clean = clean_line(line)
    print(_line_after_clean)
    words_clean = sentence2words(_line_after_clean)
    print(words_clean)
    print(len(words_clean))


# 分词测试
def clean_test():
    # content["clean_1"] = content.review.apply(lambda x: list2str(sentence2words(clean_line(x))))
    # del content['review']
    # content.to_csv("clean.csv")
    # print(content.clean_1[0:5])
    # nltk.download('averaged_perceptron_tagger')
    pass


# 将clean_1这一列所有的数据存在list数组中
def clean_1_to_list(clean_1_csvfile):
    clean_step1 = pd.read_csv(clean_1_csvfile)
    data2vector_list = clean_step1["clean_1"].tolist()
    return data2vector_list


# 获取label对应的数组
def label_to_list(label_csvfile):
    clean_step1 = pd.read_csv(label_csvfile)
    label2vector_list = clean_step1["label"].tolist()
    return label2vector_list


def rfclassifier(x_train, y_train):
    # 随机森林训练参数设置
    # 树的个数
    numTrees = 500
    # 特征子集采样策略，auto 表示算法自主选取
    featureSubsetStrategy = "auto"
    # 纯度计算
    impurity = "gini"
    # 树的最大层次
    maxDepth = 50

    # 训练随机森林分类器
    rf = RandomForestClassifier(n_estimators=numTrees, max_depth=maxDepth,
                                oob_score=True, random_state=666, n_jobs=-1)
    rf.fit(x_train, y_train)

    # # 确定当前模型的准确度
    # accuracy_score = rf.oob_score_
    # print("Test Accuracy = %f" % accuracy_score)
    return rf


# 网格搜索的方法
def rf_gradsearch_classifier(x_train, y_train):
    param_grid = {'n_estimators': [100, 150, 200, 250], 'max_depth': [15, 20, 25, 30]}

    rf_clf = RandomForestClassifier(oob_score=True, random_state=666, n_jobs=-1)
    grid_search = GridSearchCV(rf_clf, param_grid, n_jobs=-1, )
    grid_search.fit(x_train, y_train)

    print('最好的参数组合：', grid_search.best_params_)
    print('平均得分：', grid_search.best_score_)

    # 保存模型
    rf_clf = grid_search.best_estimator_
    return rf_clf


#  向量化
def word2vec():
    vectorizer = CountVectorizer()
    word2vector = vectorizer.fit_transform(clean_2_list).toarray()
    print(word2vector)
    feature_names_v1 = vectorizer.get_feature_names()
    print(len(feature_names_v1))


if __name__ == "__main__":
    filename = "clean.csv"
    clean_2_list = clean_1_to_list(filename)

    # np.set_printoptions(threshold=np.nan)  # 全部输出
    tfidf2 = TfidfVectorizer()
    X_data = tfidf2.fit_transform(clean_2_list)  # (25000, 64885)
    X_train = X_data[0:20000]  # (20000, 64885)
    X_test = X_data[20000:25000]  # (5000, 64885)

    # 获取标签数组
    label_2_list = label_to_list(filename)
    y_data = np.array(label_2_list)     # (25000,)
    y_train = y_data[0:20000]           # (20000,)
    y_test = y_data[20000:25000]        # (5000,)

    # 训练模型
    rf = rfclassifier(X_train, y_train)
    stat = rf.predict_proba(X_test)   # [0.52046828 0.47953172]分别表示预测为0的概率和预测为1的概率
    print(stat)













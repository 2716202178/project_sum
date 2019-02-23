# -*- coding: utf-8 -*- 
import numpy as np
import pandas as pd
import xlrd
import timeit

from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib

path = r'Data\data.xlsx'

# 将数据导入矩阵
def excel_to_matrix(path):
    data = pd.read_excel(path, header=1)
    datasets = data.values
    # 将数据随机化
    np.random.shuffle(datasets)
    return datasets

# 将数据分成x，y矩阵
def fiter_matrix(datasets):
    x_train = datasets[:, 0:datasets.shape[1] - 1]
    y = datasets[:, datasets.shape[1] - 1:]
    y_train = np.ravel(y)
    assert x_train.shape[0] == y_train.shape[0], \
        "the size of x must be equal to the size of y"
    return x_train, y_train

def rfclassifier(x_train, y_train):
    # 随机森林训练参数设置
    # 树的个数
    numTrees = 100
    # 特征子集采样策略，auto 表示算法自主选取
    featureSubsetStrategy = "auto"
    # 纯度计算
    impurity = "gini"
    # 树的最大层次
    maxDepth = 15

    # 训练随机森林分类器
    rf = RandomForestClassifier(n_estimators=numTrees, max_depth=maxDepth,
                                oob_score=True, random_state=666, n_jobs=-1)
    rf.fit(x_train, y_train)

    # 确定当前模型的准确度
    accuracy_score = rf.oob_score_
    print("Test Accuracy = %f" % accuracy_score)

    # 保存模型      
    joblib.dump(rf, "train_model.m")


if __name__ == '__main__':
    datasets = excel_to_matrix(path)
    x_train, y_train = fiter_matrix(datasets)

    start = timeit.default_timer()
    rfclassifier(x_train, y_train)
    end = timeit.default_timer()
    print(str(end - start))


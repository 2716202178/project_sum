# -*- coding: utf-8 -*- 
import numpy as np
import pandas as pd
import timeit

from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.model_selection import GridSearchCV

path = r'F:\IT\path\python\Model\Data\data.xlsx'

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
    # # 保存模型
    # joblib.dump(rf, "train_model.m")


if __name__ == '__main__':
    datasets = excel_to_matrix(path)
    x_train, y_train = fiter_matrix(datasets)

    start = timeit.default_timer()
    rfclassifier(x_train, y_train)
    end = timeit.default_timer()
    print(str(end - start))


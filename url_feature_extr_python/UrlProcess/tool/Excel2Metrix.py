import numpy as np
import xlrd

def excel_to_matrix(path):
    table = xlrd.open_workbook(path).sheets()[0]  # 获取第一个sheet表
    print(table.col_values(0)[1:])
    row = table.nrows  # 行数
    col = table.ncols  # 列数

    datamatrix = np.zeros((row-1, col))  # 生成一个nrows行ncols列，且元素均为0的初始矩阵
    for x in range(col):
        cols = np.matrix(table.col_values(x)[1:])  # 把list转换为矩阵进行矩阵操作
        datamatrix[:, x] = cols  # 按列把数据存进矩阵中
    # 数据归一化

    return datamatrix

if __name__ == "__main__":
    path = u"D:\\url_feature_extr_python-master\\UrlProcess\\data\\access\\access.xlsx"
    datamatrix = excel_to_matrix(path)
    print(datamatrix)

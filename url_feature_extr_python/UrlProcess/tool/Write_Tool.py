import xlwt


#  将数据写入新文件
def init_write(file_path):
    # 创建sheet
    f = xlwt.Workbook()
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    # 初始化表头
    tb_head = [
        u'path_len',
        u'sub_path_number',
        u'sub_path_max_len',
        u'sub_path_avg_len',
        u'path_type',
        u'para_len',
        u'para_num',
        u'para_avg_len',
        u'para_name_type',
        u'para_name_max_len',
        u'para_value_type',
        u'para_value_max_len',
        u'digit_percent',
        u'alpha_percent',
        u'url_unknown_amount',
        u'nginx_test',
        u'para_value_contain_ip',
        u'sql_risk_level',
        u'xss_risk_level',
        u'sensitive_risk_level',
        u'other_risk_level',
        u'directory_max_length',
    ]
    data_write(file_path,f,sheet1,0,tb_head,'label')
    return (f,sheet1)
def data_write(file_path,f,sheet,index, datas, label):
    # 将数据写入第 index行，第 j 列
    j = 0
    print(datas)
    for data in datas:
        sheet.write(index, j, data)
        j = j + 1
    label_map = {"label":"label","access":0, "directory":1, "other":2, "sensitive":3, "sql":4, "xss":5}
    label = label_map.get(label)
    sheet.write(index, j, label)
    f.save(file_path)  # 保存文件

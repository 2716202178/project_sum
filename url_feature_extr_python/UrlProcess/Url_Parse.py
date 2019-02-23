from math import log
import re
from tool.Properties_Util import Properties
from tool.Read_Tool import ReadFile
from tool.Write_Tool import init_write,data_write


class UrlParse(object):

    def __init__(self, in_parm, in_sql_rule, in_xss_rule, in_sensitive_rule):
        self._in_parm = in_parm
        self._sql_rule = in_sql_rule
        self._xss_rule = in_xss_rule
        self._sensitive_rule = in_sensitive_rule
        conf = Properties(in_parm).getProperties()

        self._url_type_dict = self._get_url_type_conf(conf)
        self._sql_risk_words_dict = self._get_sql_risk_words_conf(conf)
        self._xss_risk_words_dict = self._get_xss_risk_words_conf(conf)
        self._sensitive_risk_words_dict = self._get_sensitive_risk_words_conf(conf)
        self._other_risk_words_dict = self._get_other_risk_words_conf(conf)
        self._risk_level_dict = self._get_risk_level_conf(conf)
        self._unknow_special_characters_dict = self._get_unknow_special_characters_conf(conf)

    def _count_directory_max_length(self, url_data):
        directory_max_length = 0
        directory_length = 0
        for i in range(0, len(url_data)):
            if ord(url_data[i]) == 46 or ord(url_data[i]) == 47 or ord(url_data[i]) == 92:
                directory_length += 1
                if directory_max_length < directory_length:
                    directory_max_length = directory_length
            else:
                directory_length = 0

        return directory_max_length

    def _contain_inaddress(self, url_data):
        pattern = "\\D((25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9] \
                  {2}|[1-9]{1}[0-9]{1}|[1-9]|0)\\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\\.\
                  (25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9]))"
        re_pattern = re.compile(pattern)

        if re_pattern.search(url_data) is not None:
            return True
        return False

    def _html_test(self, url_data):
        if_html = False
        pattern1 = ".*<(\\S*?)[^>]*>.*?</\1>.*|.*</.*?>.*"
        re_pattern1 = re.compile(pattern1)
        if_html = True if re_pattern1.search(url_data) is not None else False
        if if_html is False:
            pattern2 = ".*<[a-zA-Z]+(\\s+[a-zA-Z]+\\s*=\\s*(\"([^\"]*)\".*|.*\'([^\']*)\'))*\\s*/>.*"
            re_pattern2 = re.compile(pattern2)
            if_html = True if re_pattern2.search(url_data) is not None else False
        return if_html

    def _unknow_special_characters_amount(self, url_data):
        count = 0
        special_characters = self._unknow_special_characters_dict.get("unknow_specialcharacters",None)

        if special_characters is not None:
            special_character_array = special_characters.split(",")

            for i in range(len(special_character_array)):
                    count += url_data.count(special_character_array[i])

        else:
            print("Cannot get special characters, check the url.parse.properties file!")

        return count

    def _get_url_type_conf(self, conf):
        url_type_dict = dict()

        url_type_dict["empty"] = conf.get("empty")
        url_type_dict["pure_digitals"] = conf.get("pure_digitals")
        url_type_dict["pure_letters"] = conf.get("pure_letters")
        url_type_dict["pure_normalcharacters"] = conf.get("pure_normalcharacters")
        url_type_dict["digitals_and_letters"] = conf.get("digitals_and_letters")
        url_type_dict["digitals_and_normalcharacters"] = conf.get("digitals_and_normalcharacters")
        url_type_dict["letters_and_normalcharacters"] = conf.get("letters_and_normalcharacters")
        url_type_dict["allcontain"] = conf.get("allcontain")
        url_type_dict["unknow"] = conf.get("unknow")

        return url_type_dict

    def _get_sql_risk_words_conf(self, conf):
        sql_risk_words_dict = dict()

        sql_risk_words_dict["sql_risk_low_words"] = conf.get("sql_risk_low_words")
        sql_risk_words_dict["sql_risk_middle_words"] = conf.get("sql_risk_middle_words")
        sql_risk_words_dict["sql_risk_high_words"] = conf.get("sql_risk_high_words")

        return sql_risk_words_dict


    def _get_xss_risk_words_conf(self, conf):
        xss_risk_words_dict = dict()

        xss_risk_words_dict["xss_risk_low_words"] = conf.get("xss_risk_low_words")
        xss_risk_words_dict["xss_risk_middle_words"] = conf.get("xss_risk_middle_words")
        xss_risk_words_dict["xss_risk_high_words"] = conf.get("xss_risk_high_words")

        return xss_risk_words_dict

    def _get_sensitive_risk_words_conf(self, conf):
        sensitive_risk_words_dict = dict()

        sensitive_risk_words_dict["sensitive_risk_low_words"] = conf.get("sensitive_risk_low_words")
        sensitive_risk_words_dict["sensitive_risk_middle_words"] = conf.get("sensitive_risk_middle_words")
        sensitive_risk_words_dict["sensitive_risk_high_words"] = conf.get("sensitive_risk_high_words")

        return sensitive_risk_words_dict

    def _get_other_risk_words_conf(self, conf):
        other_risk_words_dict = dict()

        other_risk_words_dict["other_risk_low_words"] = conf.get("other_risk_low_words")
        other_risk_words_dict["other_risk_middle_words"] = conf.get("other_risk_middle_words")
        other_risk_words_dict["other_risk_high_words"] = conf.get("other_risk_high_words")

        return other_risk_words_dict

    def _get_risk_level_conf(self, conf):
        risk_level_dict = dict()

        risk_level_dict["risk_low"] = conf.get("risk_low")
        risk_level_dict["risk_middle"] = conf.get("risk_middle")
        risk_level_dict["risk_high"] = conf.get("risk_high")

        return risk_level_dict

    def _get_unknow_special_characters_conf(self, conf):
        unknow_special_characters_dict = dict()
        unknow_special_characters_dict["unknow_specialcharacters"] = conf.get("unknow_specialcharacters")

        return unknow_special_characters_dict

    def _judge_url_type_and_unknown_amount(self, url_data):
        result, unknown_amount = 0, 0
        if url_data == "":
            result = int(self._url_type_dict.get("empty", "0"))
        elif self._unknow_special_characters_amount(url_data) > 0:
            unknown_amount = self._unknow_special_characters_amount(url_data)
            result = int(self._url_type_dict.get("unknow", "8"))
        elif re.match("^[0-9]+$", url_data) is not None:
            result = int(self._url_type_dict.get("pure_digitals", "1"))
        elif re.match("^[A-Za-z]+$", url_data) is not None:
            result = int(self._url_type_dict.get("pure_letters", "2"))
        else:
            flag_digitals, flag_letters, count = 1, 1, 1
            for i in range(len(url_data)):
                if url_data[i].isdigit():
                    flag_digitals = 1
                elif url_data[i].isalpha():
                    flag_letters = 1
                else:
                    count = 0

            if flag_digitals == 0 and flag_letters == 0 and count == 0:
                result = int(self._url_type_dict.get("pure_normalcharacters","3"))
            elif flag_digitals == 1 and flag_letters == 1 and count == 0:
                result = int(self._url_type_dict.get("allcontain","7"))
            elif flag_digitals == 1 and flag_letters == 0 and count == 0:
                result = int(self._url_type_dict.get("digitals_and_normalcharacters","5"))
            elif flag_digitals == 0 and flag_letters == 1 and count == 0:
                result = int(self._url_type_dict.get("letters_and_normalcharacters","6"))
            elif flag_digitals == 1 and flag_letters == 1 and count == 1:
                result = int(self._url_type_dict.get("digitals_and_letters","4"))
            else:
                result = int(self._url_type_dict.get("unknow","8"))

        return [result, unknown_amount]

    def _judge_number_of_type(self, url_data):
        digit_num = 0
        alpha_num = 0
        if url_data is None:
            return [0, 0]
        for i in range(len(url_data)):
            if re.match("^[0-9]+$", url_data[i]):
                digit_num += 1
            elif re.match("^[A-Za-z]+$", url_data[i]):
                alpha_num += 1

        return [digit_num, alpha_num]

    def _special_url_test(self, url_data):
        urldata_length = len(url_data)
        if urldata_length > 4:
            buf = url_data[urldata_length-4:urldata_length]
            if buf == ".php":
                url_split = url_data.split("/")
                if len(url_split) >= 2:
                    if url_split[len(url_split)-2].find(".") != -1:
                        return True
            elif buf == ".aspx":
                url_split = url_data.split(".aspx", 2)
                if len(url_split) > 1:
                    remain_url = url_split[1]
                    if remain_url.find("/") != -1 or remain_url.find(";") != -1:
                        return True
            elif buf == ".asp":
                url_split = url_data.split(".asp", 2)
                if len(url_split) > 1:
                    remain_url = url_split[1]
                    if remain_url.find("/") != -1 or remain_url.find(";") != -1:
                        return True
        return False

    def _contain_ipaddress(self,urldata):
        pattern = "\\D((25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]\
                  {2}|[1-9]{1}[0-9]{1}|[1-9]|0)\\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\\.\
                  (25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9]))"

        return True if re.compile(pattern).search(urldata) else False

    def _judge_contain_sql_risk_words(self, sql, url_data):
        high_level = int(self._risk_level_dict.get("risk_high", "5"))

        #  如果能过匹配规则库中的sql正则就认为是高危等级
        matcher = re.compile(sql).search(url_data.lower())
        if matcher is not None:
            return high_level

        #  含任一高危词便是高危
        high_words_string = self._sql_risk_words_dict.get("sql_risk_high_words", "")

        if high_words_string != "":
            high_word_array = high_words_string.split(",")
            for item in high_word_array:
                if url_data.lower().find(item) != -1:
                    return high_level

        #  含中危和低危词还要根据所含个数求权重和
        middle_count = 0
        middle_level = int(self._risk_level_dict.get("risk_middle", "2"))
        middle_words_string = self._sql_risk_words_dict.get("sql_risk_middle_words", "")
        if middle_words_string != "":
            middle_word_array = middle_words_string.split(",")
            #  若包含重复字符串，则累计
            for i in range(len(middle_word_array)):
                j = url_data.lower().find(middle_word_array[i])
                while j != -1 and j < len(url_data):
                    middle_count += 1
                    j = url_data.lower().find(middle_word_array[i], j+1)

        low_count = 0
        low_level = int(self._risk_level_dict.get("risk_low", "1"))
        low_words_string = self._sql_risk_words_dict.get("sql_risk_low_words", "")
        if low_words_string != "":
            low_word_array = low_words_string.split(",")
            # 若包含重复字符串，则累计
            for i in range(len(low_word_array)):
                j = url_data.lower().find(low_word_array[i])
                while j != -1 and j < len(url_data):
                    low_count += 1
                    j = url_data.lower().find(low_word_array[i], j + 1)

        return middle_count * middle_level + low_count * low_level

    def _judge_contain_xss_risk_words(self, xss, url_data):
        high_level = int(self._risk_level_dict.get("risk_high", "5"))

        # 如果能过匹配规则库中的sql正则就认为是高危等级
        matcher = re.compile(xss).search(url_data.lower())
        if matcher is not None:
            return high_level

        # 含任一高危词便是高危
        high_words_string = self._xss_risk_words_dict.get("xss_risk_high_words", "")

        if high_words_string != "":
            high_word_array = high_words_string.split(",")
            for item in high_word_array:
                if url_data.lower().find(item) != -1:
                    return high_level

        # 含中危和低危词还要根据所含个数求权重和
        middle_count = 0
        middle_level = int(self._risk_level_dict.get("risk_middle", "2"))
        middle_words_string = self._xss_risk_words_dict.get("xss_risk_middle_words", "")
        if middle_words_string != "":
            middle_word_array = middle_words_string.split(",")
            # 若包含重复字符串，则累计
            for i in range(len(middle_word_array)):
                j = url_data.lower().find(middle_word_array[i])
                while j != -1 and j < len(url_data):
                    middle_count += 1
                    j = url_data.lower().find(middle_word_array[i], j + 1)

        low_count = 0
        low_level = int(self._risk_level_dict.get("risk_low", "1"))
        low_words_string = self._xss_risk_words_dict.get("xss_risk_low_words", "")

        if low_words_string != "":
            low_word_array = low_words_string.split(",")
            # 若包含重复字符串，则累计
            for i in range(len(low_word_array)):
                j = url_data.lower().find(low_word_array[i])
                while j != -1 and j < len(url_data):
                    low_count += 1
                    j = url_data.lower().find(low_word_array[i], j + 1)

        return middle_count * middle_level + low_count * low_level

    def _judge_contain_sensitive_risk_words(self, sensitive, url_data):
        high_level = int(self._risk_level_dict.get("risk_high", "5"))

        # 如果能过匹配规则库中的sql正则就认为是高危等级
        matcher = re.compile(sensitive).search(url_data.lower())
        if matcher is not None:
            return high_level

        # 含任一高危词便是高危

        high_words_string = self._sensitive_risk_words_dict.get("sensitive_risk_high_words", "")
        if high_words_string != "":
            high_word_array = high_words_string.split(",")
            for item in high_word_array:
                if url_data.lower().find(item) != -1:
                    return high_level

        # 含中危和低危词还要根据所含个数求权重和
        middle_count = 0
        middle_level = int(self._risk_level_dict.get("risk_middle", "2"))
        middle_words_string = self._sensitive_risk_words_dict.get("sensitive_risk_middle_words", "")
        if middle_words_string != "":
            middle_word_array = middle_words_string.split(",")
            # 若包含重复字符串，则累计
            for i in range(len(middle_word_array)):
                j = url_data.lower().find(middle_word_array[i])
                while j != -1 and j < len(url_data):
                    middle_count += 1
                    j = url_data.lower().find(middle_word_array[i], j + 1)

        low_count = 0
        low_level = int(self._risk_level_dict.get("risk_low", "1"))
        low_words_string = self._sensitive_risk_words_dict.get("sensitive_risk_low_words", "")
        if low_words_string != "":
            low_word_array = low_words_string.split(",")

            # 若包含重复字符串，则累计
            for i in range(len(low_word_array)):
                j = url_data.lower().find(low_word_array[i])
                while j != -1 and j < len(url_data):
                    low_count += 1
                    j = url_data.lower().find(low_word_array[i], j + 1)

        return middle_count * middle_level + low_count * low_level

    def _judge_contain_other_risk_words(self, url_data):
        high_level = int(self._risk_level_dict.get("risk_high", "5"))

        # 含任一高危词便是高危
        high_words_string = self._other_risk_words_dict.get("other_risk_high_words", "")
        if high_words_string != "":
            high_word_array = high_words_string.split(",")
            for item in high_word_array:
                if url_data.lower().find(item) != -1:
                    return high_level

        # 含中危和低危词还要根据所含个数求权重和
        middle_count = 0
        middle_level = int(self._risk_level_dict.get("risk_middle", "2"))
        middle_words_string = self._other_risk_words_dict.get("other_risk_middle_words", "")
        if middle_words_string != "":
            middle_word_array = middle_words_string.split(",")
            # 若包含重复字符串，则累计
            for i in range(len(middle_word_array)):
                j = url_data.lower().find(middle_word_array[i])
                while j != -1 and j < len(url_data):
                    middle_count += 1
                    j = url_data.lower().find(middle_word_array[i], j + 1)

        low_count = 0
        low_level = int(self._risk_level_dict.get("risk_low", "1"))
        low_words_string = self._other_risk_words_dict.get("other_risk_low_words", "")
        if low_words_string != "":
            low_word_array = low_words_string.split(",")
            # 若包含重复字符串，则累计
            for i in range(len(low_word_array)):
                j = url_data.lower().find(low_word_array[i])
                while j != -1 and j < len(url_data):
                    low_count += 1
                    j = url_data.lower().find(low_word_array[i], j + 1)
        return middle_count * middle_level + low_count * low_level

    def _quantificaton(self, data):
        if data != 0:
            last_data = int(log(float(data)) / log(float(2)))
            return last_data
        else:
            return 0

    def url_parse(self, url):
        """对传递的url进行特征提取"""
        vector_string = ()
        #路径部分
        sub_path_array = []
        sub_path_number = 0
        sub_path_union_string = ""
        sub_path_max_len = 0
        sub_path_avg_len = 0
        url_split_array = url.split("?", 1)
        path_len = len(url_split_array[0])
        if path_len > 0:
            sub_path_array = [item for item in filter(lambda x:x != "", url_split_array[0].split("/"))]

            if len(sub_path_array) > 0:
                sub_path_number = len(sub_path_array)
                sub_path_union_string = sub_path_union_string.join(sub_path_array)
                sub_path_max_len = max(len(item) for item in sub_path_array)
                if sub_path_number != 0:
                    sub_path_avg_len = len(sub_path_union_string) / sub_path_number
                    #  去掉文件扩展名（.html等）
                    index = sub_path_array[sub_path_number-1].find(".")
                    if index != -1 and url_split_array[0].endswith("/") is False:
                        sub_path_union_string = sub_path_union_string[0:len(sub_path_union_string)-len(sub_path_array[sub_path_number-1])+index]
                        sub_path_array[sub_path_number-1] = sub_path_array[sub_path_number-1][0:index]

        #参数部分
        para_len = 0
        para_num = 0
        para_avg_len = 0
        para_names = ""
        para_values = ""
        para_name_max_len = 0
        para_value_max_len = 0
        para_name_array_buffer = []
        para_value_array_buffer = []
        if len(url_split_array) > 1 and url_split_array[1] != "":
            para_len = len(url_split_array[1])
            para_array = [item for item in filter(lambda x:x != "", url_split_array[1].split("&"))]
            para_num = len(para_array)
            if para_num != 0:
                para_avg_len = len("".join(para_array)) / para_num

            for each_para in para_array:
                each_para_split_array = each_para.split("=", 1)
                para_names += each_para_split_array[0]
                para_name_array_buffer.append(each_para_split_array[0])
                if len(each_para_split_array) > 1 and each_para_split_array[1] != "":
                    para_values += each_para_split_array[1]
                    para_value_array_buffer.append(each_para_split_array[1])

                    if len(each_para_split_array[0]) > 0 and len(each_para_split_array[1]) > 0:
                        para_name_max_len = max(len(each_para_split_array[0]), para_name_max_len)

                        para_value_max_len = max(len(each_para_split_array[1]), para_value_max_len)

        [path_type,path_unknown_amount] = self._judge_url_type_and_unknown_amount(sub_path_union_string)
        [para_name_type,para_name_unknown_amount] = self._judge_url_type_and_unknown_amount(para_names)

        [para_value_type,para_value_unknown_amount] = self._judge_url_type_and_unknown_amount(para_values)
        [path_digit_num,path_alpha_num] = self._judge_number_of_type(sub_path_array)
        [para_name_digit_num, para_name_alpha_num] = self._judge_number_of_type(para_name_array_buffer)
        [para_value_digit_num, para_value_alpha_num] = self._judge_number_of_type(para_value_array_buffer)

        digit_num = path_digit_num + para_name_digit_num + para_value_digit_num
        alpha_num = path_alpha_num + para_name_alpha_num + para_value_alpha_num
        total_number = sub_path_number + para_num * 2
        digit_percent = 0
        alpha_percent = 0
        if total_number != 0:
            digit_percent = int((digit_num * 10) / total_number)
            alpha_percent = int((alpha_num * 10) / total_number)

        url_unknown_amount = path_unknown_amount + para_name_unknown_amount + para_value_unknown_amount
        nginx_test = 1 if (self._special_url_test(url_split_array[0])) else 0

        para_value_contain_ip = (1 if (len(url_split_array) > 1 and self._contain_ipaddress(url_split_array[1])) else 0)
        sql_risk_level = self._judge_contain_sql_risk_words(self._sql_rule, url)
        xss_risk_level = self._judge_contain_xss_risk_words(self._xss_rule, url)
        sensitive_risk_level = self._judge_contain_sensitive_risk_words(self._sensitive_rule, url)
        other_risk_level = self._judge_contain_other_risk_words(url)
        directory_max_length = self._count_directory_max_length(url)

        #  对所有长度和数量特征进行量化
        path_len = self._quantificaton(path_len)
        sub_path_number = self._quantificaton(sub_path_number)
        sub_path_avg_len = self._quantificaton(sub_path_avg_len)
        sub_path_max_len = self._quantificaton(sub_path_max_len)
        para_len = self._quantificaton(para_len)
        para_num = self._quantificaton(para_num)
        para_avg_len = self._quantificaton(para_avg_len)
        para_name_max_len = self._quantificaton(para_name_max_len)
        para_value_max_len = self._quantificaton(para_value_max_len)

        """删除了之前的
            pathRisklevel,paraNameRiskLevel,paraValueRiskLevel,ifContainKeywords,4个特征,
            新增了
            sqlRiskLevel,xssRisklevel,sensitiveRisklevel,otherRisklevel,directoryMaxLength,5个特征                 
        """
        vector_string = (
                          path_len, sub_path_number, sub_path_max_len, sub_path_avg_len, path_type, para_len, para_num,
                          para_avg_len, para_name_type, para_name_max_len, para_value_type, para_value_max_len,
                          digit_percent, alpha_percent, url_unknown_amount, nginx_test, para_value_contain_ip,
                          sql_risk_level, xss_risk_level, sensitive_risk_level, other_risk_level, directory_max_length
                        )
        return vector_string



if __name__ == "__main__":
    input_file_path = ["data/access/part-00000", "data/directory/part-00000"]
    output_file_path = "data/data.xlsx"
    label = "directory"
    #   读取数据文件
    res = ReadFile(input_file_path).read_content()

    #   读取规则文件
    sql_rule = ReadFile(["regulation/sql-_20180601160333.txt"]).read_content()[0].strip("\n")
    sensitive_rule = ReadFile(["regulation/sensitive_20180601160333.txt"]).read_content()[0].strip("\n")
    xss_rule = ReadFile(["regulation/xss_20180601160333.txt"]).read_content()[0].strip("\n")
    urlParse = UrlParse("regulation/Feature_parse_20180601160333.properties", sql_rule, xss_rule, sensitive_rule)

    #   单条测试数据
    # print(res[15])
    # stat = urlParse.url_parse(res[1])
    # print(stat)
    # data_write("data/access/access.xlsx", 1, stat,True)
    #   批量数据处理结果展示
    index = 1
    [f,sheet1] = init_write(output_file_path)
    # f = open("part-00000-other-python.txt",'a')
    for cell in res[0:1200]:
        try:
            stat = urlParse.url_parse(cell)
            # print(stat, index)
            data_write(output_file_path, f,sheet1,index,stat,label)
            index += 1
            # f.write('\n%s:%s'%(stat,index))
        except Exception as e:
            index += 1
            print(index,str(e))
            continue
    # f.close()

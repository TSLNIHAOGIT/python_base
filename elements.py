import numpy as np
import pandas as pd
data=['''报关10-11-2 生
      物 一般贸易 转发: 运单号999-5106 7811，内销，清关主体：生物识别，货物已到昌北机场，请帮忙安排清关，谢谢~~''', '', '一般贸易', '8542319000', '商品名称:单片集成电路', '包装：纸箱1', '用途:\xa0指纹识别模组\n用数据处理器', '功能:\xa0将指纹信号转换为电信号，具有图像采集功能', '品牌:\xa0无', '型号: F1270-104104A03S-S-V1', '是否加密:\xa0否', '量产，无批号', '已封装\xa0', '\xa0', '8542319000', '商品名称:单片集成电路', '包装：纸箱2', '用途:\xa0指纹识别模组用数据处理器', '功能:\xa0将指纹信号转换为电信号，具有图像采集功能', '品牌:\xa0无', '型号:F1290-098098A02S-S-V1', '是否加密:\xa0否', '量产，无批号', '\xa0\xa0\xa0已封装\xa0', '\xa0', '8542319000', '商品名称:单片集成电路', '包装：纸箱3', '用途:\xa0指纹识别模组用数据处理器', '功能:\xa0将指纹信号转换为电信号，具有图像采集功能', '品牌:\xa0无', '型号:F1150-152047A01S-S-V1', '是否加密:\xa0否', '量产，无批号', '\xa0\xa0\xa0已封装\xa0', '\xa0', '8542319000', '商品名称:单片集成电路', '包装：纸箱4', '用途:\xa0指纹识别模组用数据处理器', '功能:\xa0将指纹信号转换为电信号，具有图像采集功能', '品牌:\xa0无', '型号:F1290-096096A01S-S-V1', '是否加密:\xa0否', '量产，无批号', '\xa0\xa0\xa0已封装\xa0', '\xa0', '8542319000', '商品名称:单片集成电路', '包装：纸箱5', '用途:\xa0指纹识别模组用数据处理器', '功能:\xa0将指纹信号转换为电信号，具有图像采集功能', '品牌:\xa0无', '型号:F1023-120120A01S-S-V1', '是否加密:\xa0否', '量产，无批号', '\xa0\xa0\xa0已封装\xa0', '\xa0', '8542319000', '商品名称:单片集成电路', '包装：纸箱6', '用途:\xa0指纹识别模组用数据处理器', '功能:\xa0将指纹信号转换为电信号，具有图像采集功能', '品牌:\xa0无', '型号:F1021-140140A01S-S-V1', '是否加密:\xa0否', '量产，无批号', '\xa0\xa0\xa0已封装\xa0', '\xa0', '8542319000', '商品名称:单片集成电路', '包装：纸箱7', '用途:\xa0指纹识别模组用数据处理器', '功能:\xa0将指纹信号转换为电信号，具有图像采集功能', '品牌:\xa0无', '型号:F1140-154044A01S-S-V1', '是否加密:\xa0否', '量产，无批号', '\xa0\xa0\xa0已封装\xa0', '\xa0', '8542319000', '商品名称:单片集成电路', '包装：纸箱8', '用途:\xa0指纹识别模组用数据处理器', '功能:\xa0将指纹信号转换为电信号，具有图像采集功能', '品牌:\xa0无', '型号: F1022-100100A03S-S-V1', '是否加密:\xa0否', '量产，无批号', '\xa0\xa0\xa0已封装\xa0', '']
data=np.array(data)

##是针对每一个文件结构化，还是针对一单中所有的文件，如pdf,word,excel等等进行结构化
##是否是表格

###对于要结构化的文本，从第一行开始判断，是否为hs_code,是否包含分隔符，如果都没有前面的内容都放在一起，直到找到hs_code或者分隔符位置

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# 设置value的显示长度为100，默认为50
pd.set_option('max_colwidth', 300)

import re


##针对pdf识别结果

def juduge_is_hscode(data):
    pattern = '[0-9]{6,}\.*[0-9]*'
    data = re.findall(pattern, data)
    if data:
        #         print('data hs',data)
        data_num = ''.join(data)
        # 需要查数据库判断，之后写逻辑
        if len(data_num) >= 10:
            return True
        else:
            return False
    else:
        return False


def elements_struct(data, not_excel=True, file_type=None):
    #     each_hs_product={}
    # 初始化为空
    each_hs_all_elements = {}
    all_content = []
    for each in data:
        #         if not_excel:
        if file_type == 'word':
            if not_excel:
                # text是原始的每一行内容
                text = each
            else:
                text = ''.join(each)
        elif file_type == 'pdf':
            each = each[0:-4]
            # 取出列表中的字符串
            text = ''.join(each)
        #         print('text:\n',text)

        # 每个hs编码相应的产品对应一个字典

        #         #初始化为空
        #         text_list=['','']
        #         each_hs_all_elements[text_list[0]]=[]
        #             print(text)
        ##判断是否是HS编码
        bool_value = juduge_is_hscode(text)
        #             print(text,bool_value)

        ##这里要改成遇到下一个重复的名称时，说明开始重复了，要将前面的结果进行汇总
        pattern0 = '：|:|；'
        m0 = re.search(pattern0, text)
        #         print('m',m0)
        # 不含分隔符，且含有hs编码
        if bool_value and (not m0):
            # 遇到下一个hs编码时要把之前一个hs对应的申报要素都放到列表里
            all_content.append(each_hs_all_elements)

            # 清空重用，开始下一次hs对应的申报要素收集
            #                 each_hs_product={}
            each_hs_all_elements = {}
            each_hs_all_elements['hs_code'] = text
        #                 each_hs_product['hs_code']=text

        else:
            # 找到每个申报要素中的分隔符,分隔，如果有某个申报要素是多行显示以分隔符为标准将其拼接在一起
            pattern1 = '：|:|；'
            m = re.search(pattern1, text)
            if m:
                text_list = text.split('{}'.format(m.group()), maxsplit=1)
                #                     print(text_list)
                if text_list[1] != '':
                    each_hs_all_elements[text_list[0]] = text_list[1]
                #                         each_hs_all_elements.append(text)
                else:
                    ##内容可能在下面
                    each_hs_all_elements[text_list[0]] = text_list[1]
                    print('很特殊')

            else:
                text = "  " + text
                each_hs_all_elements[text_list[0]] += text
    #                     print(text)

    ##退出循环之后把最后那一次也加进来
    all_content.append(each_hs_all_elements)
    return all_content


def elements_struct_new(data, not_excel=True, file_type=None):
    #     each_hs_product={}
    # 初始化为空
    each_hs_all_elements = {}
    all_content = []
    all_key_name = set()
    current_key_name = ''
    for each in data:
        #         if not_excel:
        if file_type == 'word':
            if not_excel:
                # text是原始的每一行内容
                text = each
            else:
                text = ''.join(each)
        elif file_type == 'pdf':
            each = each[0:-4]
            # 取出列表中的字符串
            text = ''.join(each)
        #         print('text: ',text)

        # 每个hs编码相应的产品对应一个字典

        #         #初始化为空
        #         text_list=['','']
        #         each_hs_all_elements[text_list[0]]=[]
        #             print(text)

        #             print(text,bool_value)

        ##这里要改成遇到下一个重复的名称时，说明开始重复了，要将前面的结果进行汇总
        #         pattern0='：|:|；'
        #         m0=re.search(pattern0,text)
        #         print('m',m0)
        # 不含分隔符，且含有hs编码
        #         if bool_value and (not m0):
        #         print('0 current={}  ,all={}  bool={} \n'.format(current_key_name,all_key_name,current_key_name in all_key_name))
        if current_key_name in all_key_name:
            # 遇到下一个hs编码时要把之前一个hs对应的申报要素都放到列表里

            #             print('each_hs_all_elements',each_hs_all_elements)
            all_content.append(each_hs_all_elements)

            # 清空重用，开始下一次hs对应的申报要素收集
            #                 each_hs_product={}
            each_hs_all_elements = {}
            all_key_name = set()

            all_key_name.add(current_key_name)


        #          each_hs_product['hs_code']=text

        else:
            ##判断是否为HS编码
            bool_value = juduge_is_hscode(text)
            #             print('bool_value={} text={}'.format(bool_value,text))
            if bool_value:
                each_hs_all_elements['hs_code'] = text

                # 把上一次的加进来
                all_key_name.add(current_key_name)
                # 这一个才是当前的
                current_key_name = 'hs_code'

            #                print('bool current={}  ,all={}\n'.format(current_key_name,all_key_name))

            # 找到每个申报要素中的分隔符,分隔，如果有某个申报要素是多行显示以分隔符为标准将其拼接在一起
            pattern1 = '：|:|；'
            m = re.search(pattern1, text)
            if m:
                text_list = text.split('{}'.format(m.group()), maxsplit=1)
                #                     print(text_list)
                if text_list[1] != '':
                    each_hs_all_elements[text_list[0]] = text_list[1]

                    all_key_name.add(current_key_name)
                    current_key_name = text_list[0]

                #                         each_hs_all_elements.append(text)
                else:
                    ##内容可能在下面
                    each_hs_all_elements[text_list[0]] = text_list[1]

                    all_key_name.add(current_key_name)
                    current_key_name = text_list[0]
                    print('很特殊')
            #                 print('m current={}  ,all={}\n'.format(current_key_name,all_key_name))

            else:
                text = "  " + text
                each_hs_all_elements[text_list[0]] += text
    #                     print(text)

    ##退出循环之后把最后那一次也加进来
    all_content.append(each_hs_all_elements)
    return all_content


def judge_content_is_right():
    pass


def delete_wrong_rows_cols(df):
    # 如果行或者列缺失值占比超过一定阈值就删除就删除
    # 先判断列，删除后；再判断行（删除全为缺失值的行），
    col_name = df.columns
    df_shape = df.shape
    for each in col_name:
        # 将空字符串替换为None
        df[each] = df[each].apply(lambda x: x if x != '' else None)
        null_rate = pd.isna(df[each]).sum() / df_shape[0]
        #        print(null_rate)
        if null_rate > 0.8:
            df = df.drop(each, axis=1)
    df = df.dropna(axis=0, how='all')
    return df


def final_table_results(df):
    df1 = df[['hs_code', '商品名称']]
    return df


##测试时注意传过来的是word还是pdf
# all_content=elements_struct(data,file_type='word',not_excel=False)
# all_content=elements_struct(data,file_type='pdf',not_excel=False)


all_content = elements_struct_new(data, file_type='word', not_excel=False)

import pandas as pd

print('all_content', all_content)
#
# df = pd.DataFrame(all_content)
# df = delete_wrong_rows_cols(df)
# df
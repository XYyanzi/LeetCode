'''
#-*- coding: utf-8 -*-
@Author: xunyan
@Time: 2020/12/11 7:46 下午
@File: 根据userId生成手机号.py
'''
import pymysql
import requests


class MysqlConnection(object):
    def __init__(self):
        self.connection = pymysql.Connect(host='127.0.0.1', user='root', password='advance.ai2016',
                                          database='atome_id', port=3306, autocommit=True)
        self.cursor = self.connection.cursor(cursor=pymysql.cursors.DictCursor)

    def __enter__(self):
        return self

    def select(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def __exit__(self, type, value, trace):
        self.cursor.close()
        self.connection.close()


def jiemi(mobile_list):
    url = 'http://127.0.0.1:10074/nkp-internal-api/internal/decrypt'
    request_body = {
        "encryptDataList": mobile_list
    }
    response = requests.post(url, json=request_body)
    print(response.text)
    mobile = response.json()['data']['decryptDataList']
    return mobile


def convert_to_mobile():
    # 从文件中逐行读取user_id
    database = MysqlConnection()
    mobile_encrypt_list = []
    mobile = []
    f = open('1.csv', 'r')
    for line in f.readlines():
        user_id = line.strip()
        # 根据userId查询出手机号加密值
        sql = "select mobile_number from user where `id`='{}'".format(user_id)
        print(sql)
        mobile_encrypt = database.select(sql)
        print(mobile_encrypt)
        if mobile_encrypt:
            mobile_encrypt = mobile_encrypt[0]['mobile_number']
            mobile_encrypt_list.append(mobile_encrypt)
        else:
            print('未查询到user')
            continue
    response_list = jiemi(mobile_encrypt_list)
    for i in response_list:
        mobile.append(i['decryptStr'])
    with open('2.csv', 'w') as f:
        for m in mobile:
            f.writelines(m+'\n')


if __name__ == '__main__':
    convert_to_mobile()

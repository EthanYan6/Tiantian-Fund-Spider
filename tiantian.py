#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@Author         : Ethan Yan
@Contact        : yanyuliang6@163.com
@File           : tiantian.py
@Time           : 2020/4/6 16:02
@Desc           : 爬取天天基金的金融数据
@Method of use  : Just run
@Software       : PyCharm
@License        : (C) Copyright 2019-2050, Node Supply Chain Manager Corporation Limited.
"""
import requests
import json
from pymysql import connect
from time import sleep


class PureFinance(object):
    def __init__(self, code):
        self.code = code
        self.conn = connect(host='数据库地址', port=3306, database='数据库', user='用户名', password='密码')

        print("开始初始化数据库表，删除该基金下错误数据...")
        cur = self.conn.cursor()
        sql_str = """delete from fund where fundname=%s;"""
        # 将表的自增序列恢复，比如原先4322条数据，删除了4322后，下次编号任然希望从4322开始；从性能角度出发，此语句不应该执行
        sql_str2 = """ALTER TABLE fund AUTO_INCREMENT = 1;"""
        # 执行SQL语句
        row_count = cur.execute(sql_str, [self.code])
        print("表中受影响行数为 {}".format(row_count))
        cur.execute(sql_str2)
        self.conn.commit()
        # 关闭游标
        cur.close()

    def getNPV(self):
        """
        查询全部历史净值
        :return: 查询结果字典，成功或者失败
        """
        page = 1
        url = "http://api.fund.eastmoney.com/f10/lsjz?callback=jQuery18304038998523093684_1586160530315"
        tempurl = url + "&fundCode={}&pageIndex={}&pageSize=20".format(self.code, page)
        header = {"Referer": "http://fundf10.eastmoney.com/jjjz_{}.html".format(self.code)}

        jsonData = requests.get(tempurl, headers=header).content.decode()
        dictData = json.loads(jsonData[41:-1])
        print("初次执行结果：\n{}".format(dictData))
        totalCount = dictData.get("TotalCount")

        sql = """insert into fund(fundname, funddate, NPV, rate) values(%s, %s, %s, %s);"""
        tmpList = list()

        pageTotal = totalCount // 20
        if totalCount % 20 != 0:
            pageTotal += 1
        print("总页数为 {}".format(pageTotal))

        for singlePage in range(1, pageTotal+1):
            tempurl = url + "&fundCode={}&pageIndex={}&pageSize=20".format(self.code, singlePage)
            print("现在处理第 {} 页数据".format(singlePage))
            jsonData = requests.get(tempurl, headers=header).content.decode()
            dictData = json.loads(jsonData[41:-1])
            listDateData = dictData.get("Data", {"LSJZList": None}).get("LSJZList")
            for item in listDateData:
                # 获取日期
                npvDate = item.get("FSRQ")
                # 获取每日单位净值
                npv = item.get("DWJZ")
                # 获取每日增长率，基金最开始的一段时间为封闭期，增长率为0
                tempRate = item.get("JZZZL")
                rate = "0.00" if tempRate == "" else tempRate
                view = (self.code, str(npvDate), str(npv), str(rate))
                tmpList.append(view)
            sleep(1)

        try:
            cur = self.conn.cursor()
            cur.executemany(sql, tmpList)
            self.conn.commit()
        except Exception as e:
            print(e)
            return {"message": "error", "status": 400}
        finally:
            cur.close()
            self.conn.close()

        return {"message": "ok", "status": 200}


fund = PureFinance('基金代码')
mes = fund.getNPV()
# 打印处理结果
print(mes)

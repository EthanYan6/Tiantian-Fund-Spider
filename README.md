# Tiantian-Fund-Spider
Desc: 爬取天天基金历史净值数据脚本

# 说明文档

## 1.数据展示分析

[点击进入展示页面](https://www.pythonnote.cn/Tiantian-Fund-Spider/)

![图片预览](https://gitee.com/Ethanyan/pic_data/raw/master/15862635917574.jpg)

## 2.天天基金的相关接口

1. 查询某个基金的相关信息

    ```url
    http://fund.eastmoney.com/001938.html?spm=search
    ```

    > 其中的001938为基金的代码
    >

2. 查询基金的历史净值页面

    ```url
    http://fundf10.eastmoney.com/jjjz_001938.html
    ```

    > 其中的001938为基金的代码

3. 查询基金历史净值数据接口

    ```url
    http://api.fund.eastmoney.com/f10/lsjz?callback=jQuery18304038998523093684_1586160530315&fundCode=基金代码&pageIndex=页数&pageSize=每页数据条数
    ```

    > 由于反爬措施，访问需要携带请求头：Referer，它的值如下
    
    ```url
    http://fundf10.eastmoney.com/jjjz_基金代码.html
    ```

## <a id="#数据库表">3.数据库表</a>

```sql
create database financedb;

create table fund(
    id int auto_increment primary key,
    fundname varchar(20),
    funddate date,
    NPV decimal(9,4),
    rate decimal(5,2)
);
```

## 4.使用方法

1. 安装模块：

    ```shell script
    pip install requests
    pip install pymysql
    ```
    
    > `Python` 版本为 3.x

2. 在本地数据库 `mysql` 中创建数据库 `financedb`，并在该数据库中创建数据库表 `fund`。（创建语句可查看第二部分 [数据库表](#数据库表)）

3. 在文件 `tiantian.py` 中修改如下配置项：
  
    ```shell script
    class PureFinance(object):
        def __init__(self, code):
            ...
    --->    self.conn = connect(host='数据库地址', port=3306, database='数据库', user='用户名', password='密码')
            ...
    ```

4. 在文件 `tiantian.py` 如下位置填上需要爬取的基金代码：

    ```shell script
    ...
    fund = PureFinance('基金代码') <--- 修改此处
    mes = fund.getNPV()
    ...
    ```
   
5. 执行完毕后，可在对应的数据库表中查看数据是否保存完成。 


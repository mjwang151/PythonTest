import requests
import pymysql


def options(data):
    url = "https://app.amarsoft.com/hubservicetest/api/gateway"
    headers = {'content-type': "application/json;charset=utf-8", 'Accept': 'application/json'}
    res = requests.post(url=url, json=data, headers=headers)
    print(res.text)


data = {"transcode": "R1103V3", "userid": "11", "orGid": "EDS", "account": "EDS", "source": "EDS",
        "params": {"name": "重庆雨汇食品有限公司11"}}
options(data)

# 打开数据库连接
conn = pymysql.connect(host='192.168.61.78', port=3306, user='chaxun', password='chaxun',database='crservice_ws', charset='utf8')
# 获取游标对象
cursor = conn.cursor()
# 查询 SQL 语句
sql = "select * from eds_monitor_entlist;"
# 执行 SQL 语句 返回值就是 SQL 语句在执行过程中影响的行数
row_count = cursor.execute(sql)
print("SQL 语句执行影响的行数%d" % row_count)
# 取出结果集中一行数据,　例如:(1, '张三')
# print(cursor.fetchone())
# 取出结果集中的所有数据, 例如:((1, '张三'), (2, '李四'), (3, '王五'))
for line in cursor.fetchall():
    print(line)
# 关闭游标
cursor.close()
# 关闭连接
conn.close()

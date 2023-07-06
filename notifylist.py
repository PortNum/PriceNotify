#! /usr/bin/env python

import akshare as ak
import config
import dbutils
import dbutils as db
import os

print(os.getcwd())

'''
type|name|symbol|compare_direction|price|number

--type: 1:future    2:stock     3:cfd
'''


def choose_action():
    global id
    while True:
        action = input("1:添加   2:删除    3:列表    4:结束操作\n请选择操作:")
        if action == "1":
            choose_type()
            continue
        if action == "2":
            while True:
                try:
                    id = int(input("请输入要删除的任务ID："))
                except ValueError as e:
                    print("请输入整数！")
                    continue
                break
            dbutils.delete_task(id)
            dbutils.list_task()
            continue
        if action == "3":
            dbutils.list_task()
            continue
        if action == "4":
            break


def choose_type():
    while True:
        type = input("1:内盘期货   2：A股    3：CFD   4:放弃\n添加类型:")
        if type == "1":
            add_cn_future()
            break
        if type == '2':
            print('待实现')
            break
        if type == '3':
            print('待实现')
            break
        if type == '4':
            print("放弃操作，退出")
            break
        continue


def compare_direction():
    global direction
    while True:
        try:
            direction = int(input("1：高于等于     2：低于等于\n请选择："))
        except ValueError as e:
            print("请输入正确的数字")
        if direction == 1:
            return '高于'
        if direction == 2:
            return '低于'
        if direction != 1 and direction != 2:
            print("请输入正确的数字")
            continue


def get_price():
    global price
    while True:
        try:
            price = float(input("请输入价格："))
        except ValueError as e:
            print("请输入数字")
            continue
        if price < 0:
            print("请输入数字")
            continue
        break
    return price


def add_cn_future():
    global name, symbol
    future_items = ak.futures_symbol_mark()
    length = future_items.shape[0]
    for j in future_items.index:
        if (j + 1) % 10 == 0:
            print(f"%2s:%2s" % (j, future_items.at[j, 'symbol']))
        else:
            print(f"%2s:%2s" % (j, future_items.at[j, 'symbol']), end="  ")
    while True:
        try:
            item = int(input("请选择期货品种："))
        except ValueError as e:
            print("请正确输入数字")
            continue
        if item > length - 1 or item < 0:
            print("请输入正确的数字")
            continue
        name = future_items.at[item, 'symbol']
        contracts = ak.futures_zh_realtime(symbol=name)
        print(contracts)
        print("%-8s%-8s%-8s" % ("序号", "合约", "现价"))
        for c in contracts.index:
            print("%-8s%-8s%-8s" % (c, contracts.at[c, 'symbol'], contracts.at[c, 'trade']))
        while True:
            try:
                symbol_index = int(input("请选择合约序号："))
            except ValueError as e:
                print("请正确输入数字")
                continue
            if symbol_index > contracts.shape[0] - 1 or item < 0:
                print("请输入正确的数字")
                continue
            symbol = contracts.at[symbol_index, 'symbol']
            print("已选择：%s ,合约：%s" % (future_items.at[item, 'symbol'], symbol))
            break
        break
    direction = compare_direction()
    price = get_price()
    num = get_num()
    values = ['cn_future', name, symbol, direction, price, num]
    sqlite_db = dbutils.get_db()
    sqlite_db.insert(config.table_name, config.table_fields, values)
    print("添加成功！")
    dbutils.list_task()


def get_num():
    global num
    while True:
        try:
            num = int(input("请输入通知次数："))
        except ValueError as e:
            print("请输入数字")
            continue
        if num < 0:
            print("请输入正确数字数字")
            continue
        break
    return num


def db_init():
    sqlite_db = db.Db("notify.db")
    sqlite_db.create_table(config.table_name, config.field_list)
    return sqlite_db


if __name__ == '__main__':
    choose_action()

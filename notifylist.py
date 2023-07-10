#!/usr/bin/python

import akshare as ak
import config
import dbutils
import dbutils as db
import os

print(os.getcwd())


def choose_action():
    global id
    while True:
        action = input("1:添加   2:删除    3:列表    4:重置     5：放弃操作\n请选择操作:")
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
            confirm_del = input("即将清空所有的任务并重置，是否继续(y/n)？")
            if confirm_del == "y" or confirm_del == "Y":
                dbutils.delete_task_table()
                print("重置成功！")
                continue
            print("已放弃操作！")
            continue
        if action == "5":
            break


def choose_type():
    while True:
        type = input("1:内盘期货   2：A股    3：CFD   4:放弃\n添加类型:")
        if type == "1":
            add_cn_future()
            break
        if type == '2':
            add_cn_stocks()
            break
        if type == '3':
            add_foreign_commodity_cfd()
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
            print(f"%2s:%2s" % (j, future_items.at[j, 'symbol']), end="\n\n")
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
            print("已选择：%s ,合约：%s" % (name, symbol))
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


def add_foreign_commodity_cfd():
    global cfd_symbol, cfd_name
    cfds = ak.futures_hq_subscribe_exchange_symbol()
    length = cfds.shape[0]
    for cfd in cfds.index:
        if (cfd + 1) % 10 == 0:
            print(f"%2s:%2s" % (cfd, cfds.at[cfd, 'symbol']), end="\n\n")
        else:
            print(f"%2s:%2s" % (cfd, cfds.at[cfd, 'symbol']), end="  ")
    while True:
        try:
            item = int(input("请选择外盘商品CFD品种："))
        except ValueError as e:
            print("请正确输入数字")
            continue
        if item > length - 1 or item < 0:
            print("请输入正确的数字")
            continue
        cfd_name = cfds.at[item, 'symbol']
        cfd_symbol = cfds.at[item, 'code']
        cfd_price = get_current_cfd_price(cfd_symbol)

        print("已选择：%s ,代码：%s, 当前价格：%s" % (cfd_name, cfd_symbol, cfd_price))
        break
    direction = compare_direction()
    price = get_price()
    num = get_num()
    values = ['foreign_commodity_cfd', cfd_name, cfd_symbol, direction, price, num]
    sqlite_db = dbutils.get_db()
    sqlite_db.insert(config.table_name, config.table_fields, values)
    print("添加成功！")
    dbutils.list_task()


def add_cn_stocks():
    while True:
        try:
            stock_symbol = input("请输入6位A股个股代码：")
            if len(stock_symbol) > 6:
                continue
            stock_info = ak.stock_individual_info_em(symbol=stock_symbol)
            stock_name = stock_info.at[5, 'value']
            stock_prices = ak.stock_bid_ask_em(symbol=stock_symbol)
            stock_current_price = stock_prices.at[8, 'value']
            confirm = input("A股 %s %s  现价：%s ,是否添加(y/n)？" % (stock_symbol, stock_name, stock_current_price))
            if confirm != "y" and confirm != "Y":
                print("已放弃添加！")
                break
            direction = compare_direction()
            price = get_price()
            num = get_num()
            values = ['cn_stock', stock_name, stock_symbol, direction, price, num]
            sqlite_db = dbutils.get_db()
            sqlite_db.insert(config.table_name, config.table_fields, values)
            print("添加成功！")
            dbutils.list_task()
            break

        except Exception as e:
            print(e)
            print("查询个股失败")
            continue


def get_current_cfd_price(code: str):
    list = ['CT', code]
    try:
        futures_foreign_commodity_realtime_df = ak.futures_foreign_commodity_realtime(subscribe_list=list)
        current_price = futures_foreign_commodity_realtime_df.at[1, '最新价']
        return current_price
    except Exception as e:
        print(e)
        return "获取失败"


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

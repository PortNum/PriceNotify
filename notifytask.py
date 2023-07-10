#!/usr/bin/python
import datetime
import json
import time
import config
import dbutils
import akshare as ak

import notifyutils
import sys


def get_current_price_cn_future(symbol: str):
    try:
        if is_belong_zjs(symbol):
            futures_zh_spot_df = ak.futures_zh_spot(symbol=symbol, market="FF", adjust='0')
            return futures_zh_spot_df.at[0, 'current_price']
        futures_zh_spot_df = ak.futures_zh_spot(symbol=symbol, market="CF", adjust='0')
        return futures_zh_spot_df.at[0, 'current_price']
    except Exception as e:
        print("获取 %s 当前价格失败" % symbol)
        print(e)
        return None


def get_current_cfd_price(code: str):
    list = ['CT', code]
    try:
        futures_foreign_commodity_realtime_df = ak.futures_foreign_commodity_realtime(subscribe_list=list)
        current_price = futures_foreign_commodity_realtime_df.at[1, '最新价']
        return current_price
    except Exception as e:
        print(e)
        return None


def compare_price(current_price, target_price, compare_direction, symbol, name):
    print(name, symbol, current_price, compare_direction, target_price, end=" ?")
    if compare_direction == "高于":
        if current_price >= target_price:
            print("YES")
            return True
        else:
            print("NO")
            return False

    if compare_direction == "低于":
        if current_price <= target_price:
            print("YES")
            return True
        print("NO")
        return False
    print("NO")
    return False


def is_belong_zjs(symbol: str):
    # 判断是否中金所产品
    zhong_jin_suo = "IF|IH|IC|IM|TF|TS|TL"
    zjs = zhong_jin_suo.split("|")
    for s in zjs:
        if symbol.startswith(s):
            return True
    return False



def is_workday():
    now = datetime.datetime.now()
    workday = now.weekday()
    print("今天是周 %s " % (workday + 1), end=" ")
    if workday == 5 or workday == 6:
        print(",未开盘")
        return False
    return True


def is_cn_future_opening_time():
    now_localtime = time.strftime("%H:%M:%S", time.localtime())
    if "09:00:00" < now_localtime < "11:30:00" or "13:30:00" < now_localtime < "15:00:00" or "21:00:00" < now_localtime < "23:00:00":
        return True
    print("内盘期货未开盘: %s" % now_localtime)
    return False


if __name__ == '__main__':
    while True:
        rows = dbutils.list_task()
        if rows is not None:
            try:
                for row in rows:
                    need_notify_num = row[6]
                    target_price = row[5]
                    compare_direction = row[4]
                    notify_id = row[0]
                    task_type = row[1]
                    symbol = row[3]
                    name = row[2]
                    if task_type == "cn_future" and need_notify_num > 0:
                        if is_workday() and is_cn_future_opening_time():
                            current_price = get_current_price_cn_future(symbol)
                            if compare_price(current_price, target_price=target_price,
                                             compare_direction=compare_direction, symbol=symbol, name=name):
                                content = "到价提醒：%s ,%s ,当前价格 %s %s设置价格：%s" % (
                                    name, symbol, current_price, compare_direction, target_price)
                                resp = notifyutils.send_notify(content)
                                if resp.status_code == 200 and json.loads(resp.content)['StatusCode'] == 0:
                                    dbutils.update_task(notify_id, need_notify_num)
                                    print(content, "发送成功")
                    if task_type == "foreign_commodity_cfd" and need_notify_num >0:
                        current_price = get_current_cfd_price(symbol)
                        if compare_price(current_price, target_price=target_price,
                                         compare_direction=compare_direction,symbol=symbol, name=name):
                            content = "到价提醒：%s ,%s ,当前价格 %s %s设置价格：%s" % (
                                name, symbol, current_price, compare_direction, target_price)
                            resp = notifyutils.send_notify(content)
                            if resp.status_code == 200 and json.loads(resp.content)['StatusCode'] == 0:
                                dbutils.update_task(notify_id, need_notify_num)
                                print(content, "发送成功")

            except Exception as e:
                print(e)
        time.sleep(config.sleep_time)

#!/usr/bin/python
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


def compare_price(current_price, target_price, compare_direction):
    print(current_price, compare_direction, target_price, end=" ?")
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


def list_task():
    try:
        db = dbutils.get_db()
        rows = db.select(config.table_name, config.table_fields_all)
        print("%-8s%-15s%-8s%-10s%-8s%-8s%-8s" % (
            "ID", "类型", "名称", "代码", "高于/低于", "价格", "剩余通知次数"))
        for r in rows:
            print("%-8s%-15s%-8s%-10s%-8s%-8s%-8s" % (r[0], r[1], r[2], r[3], r[4], r[5], r[6]))
        db.close_conn()
        return rows
    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    while True:
        rows = list_task()
        if rows is not None:
            try:
                for row in rows:
                    need_notify_num = row[6]
                    target_price = row[5]
                    compare_direction = row[4]
                    notify_id = row[0]
                    if row[1] == "cn_future" and need_notify_num > 0:
                        current_price = get_current_price_cn_future(row[3])
                        if compare_price(current_price, target_price=target_price, compare_direction=compare_direction):
                            content = "到价提醒：%s ,%s ,当前价格 %s %s设置价格：%s" % (
                                row[2], row[3], current_price, compare_direction, row[5])
                            resp = notifyutils.send_notify(content)
                            if resp.status_code == 200 and json.loads(resp.content)['StatusCode'] == 0:
                                dbutils.update_task(notify_id, need_notify_num)
                                print(content, "发送成功")
            except Exception as e:
                print(e)
        time.sleep(config.sleep_time)

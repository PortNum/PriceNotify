import akshare as ak
import pandas as pd


def t():
    fx_pair_quote_df = ak.fx_pair_quote()
    print(fx_pair_quote_df)
    length = fx_pair_quote_df.shape[0]
    while True:
        try:
            forex_index = int(input("请选择货币对："))
        except ValueError as e:
            print("请正确输入数字")
            continue
        if forex_index > length - 1 or forex_index < 0:
            print("请输入正确的数字")
            continue
        name = fx_pair_quote_df.at[forex_index, '货币对']
        symbol = forex_index
        current_price = fx_pair_quote_df.at[forex_index, '卖报价']
        confirm_choice = input("已选择：%s ,代码：%s, 缺定添加(y/n)？" % (name, symbol))
        if confirm_choice != "y" or confirm_choice != "Y":
            print("放弃操作！")
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







def foreign_commodity_cfd():
    cfds = ak.futures_hq_subscribe_exchange_symbol()
    length = cfds.shape[0]
    for cfd in cfds.index:
        if (cfd + 1) % 5 == 0:
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
        name = cfds.at[item, 'symbol']
        symbol = cfds.at[item, 'code']



def get_current_cfd_price(code: str):
    list = ['CT', code]
    futures_foreign_commodity_realtime_df = ak.futures_foreign_commodity_realtime(subscribe_list=list)
    current_price = futures_foreign_commodity_realtime_df.at[1, '最新价']
    print(current_price)


if __name__ == '__main__':
    # foreign_commodity_cfd()
    t()

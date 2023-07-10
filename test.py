import akshare as ak
import pandas as pd


def t():
    stock_individual_info_em_df = ak.stock_individual_info_em(symbol="002372")
    print(stock_individual_info_em_df)
    stock_bid_ask_em_df = ak.stock_bid_ask_em(symbol="002372")
    # print(stock_bid_ask_em_df)
    print(stock_bid_ask_em_df.at[8, 'value'])
    stock_name = stock_individual_info_em_df.at[5, 'value']
    print(stock_name)






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
        print("已选择：%s ,代码：%s" % (name, symbol))
        break


def get_current_cfd_price(code: str):
    list = ['CT', code]
    futures_foreign_commodity_realtime_df = ak.futures_foreign_commodity_realtime(subscribe_list=list)
    current_price = futures_foreign_commodity_realtime_df.at[1, '最新价']
    print(current_price)


if __name__ == '__main__':
    # foreign_commodity_cfd()
    t()

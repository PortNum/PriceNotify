# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time
import akshare as ak

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print("开始接收实时行情, 每 3 秒刷新一次")
    subscribe_list = ak.futures_foreign_commodity_subscribe_exchange_symbol() ##获取外盘CFD代码
    future_items = ak.futures_symbol_mark()
    for j in future_items.index:
        if j%10 ==0:
            print(future_items.at[j,'symbol'])
        else:
            print(future_items.at[j,'symbol'],end="  ")

    futures_zh_realtime_df = ak.futures_zh_realtime(symbol="棉花")
    print(futures_zh_realtime_df)

    subscribe_list = ['CL', 'XAU', 'XAG']

    futures_zh_spot_df = ak.futures_zh_spot(symbol='SA2309,SR2309', market="CF", adjust='0')
    print(futures_zh_spot_df)

    # while True:
    #     time.sleep(3)
    #     futures_foreign_commodity_realtime_df = ak.futures_foreign_commodity_realtime(subscribe_list=subscribe_list) ##获取外盘CFD报价
    #     print(futures_foreign_commodity_realtime_df)




if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

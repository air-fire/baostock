import baostock as bs
import pandas as pd
from stock.stock import Stock
import os


# 证券类型，其中1：股票，2：指数，3：其它，4：可转债，5：ETF


def update_stock_data():
    bs.login()
    rs = bs.query_stock_basic()
    bs.logout()
    data = []
    while (rs.error_code == '0') & rs.next():
        data.append(rs.get_row_data())
    df = pd.DataFrame(data, columns=rs.fields)
    df.to_csv("data/stock_data.csv", index=False, encoding="utf_8_sig")


def update_individual_stock_data():
    stock_df = pd.read_csv("data/stock_data.csv", dtype={'code': str})
    bs.login()
    for _, row in stock_df.iterrows():
        if str(row['type']) == '1' and str(row['status']) == '1' and row['code'][3:6] not in ['300', '310', '688']:
            stock = Stock()
            stock.set_symbol(row['code'])
            stock.save_to_csv()
    bs.logout()


def strategy_select_stocks():
    stock_df = pd.read_csv("data/stock_data.csv", dtype={'code': str})
    selected_stocks = []
    for _, row in stock_df.iterrows():
        if str(row['type']) == '1' and str(row['status']) == '1' and row['code'][3:6] not in ['300', '310', '688']:
            stock = Stock()
            stock.set_symbol(row['code'])
            result = stock.stock_strategy_min_volume()
            if result:
                selected_stocks.append(result)
    return selected_stocks


def main():
    info = """
    请选择要执行的操作：
    1. 更新股票列表
    2. 更新个股数据
    3. 策略选股
    4. 退出
    """
    print(info)
    choice = input("请输入操作编号 (1/2/3/4): ").strip()

    while choice not in ['1', '2', '3', '4']:
        choice = input("无效输入，请重新输入操作编号 (1/2/3): ").strip()
    if choice == '1':
        if os.path.exists("data/stock_data.csv"):
            os.remove("data/stock_data.csv")
        update_stock_data()
        print('股票列表数据更新完成！')
    elif choice == '2':
        if not os.path.exists("data/stock_data.csv"):
            print("股票列表数据不存在，正在更新股票列表数据...")
            update_stock_data()
        update_individual_stock_data()
        print('个股数据更新完成！')
    elif choice == '3':
        selected_stocks = strategy_select_stocks()
        if not selected_stocks:
            print("没有符合策略的股票。")
        else:
            with open('results/selected_stocks.txt', 'w') as f:
                for stock in selected_stocks:
                    f.write(f"{stock}\n")
    elif choice == '4':
        print("退出程序。")
        return


if __name__ == "__main__":
    main()

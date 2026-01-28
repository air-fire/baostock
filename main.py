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
    print(df)


def update_individual_stock_data():
    stock_df = pd.read_csv("data/stock_data.csv", dtype={'code': str})
    bs.login()
    for _, row in stock_df.iterrows():
        if str(row['type']) == '1' and str(row['status']) == '1' and (row['code'][3:6] not in ['300', '310', '688']):
            stock = Stock()
            stock.set_symbol(row['code'])
            stock.save_to_csv()
    bs.logout()


def main():
    is_update_stock_data = input("是否更新股票列表数据？(y/n): ").strip().lower() == 'y'
    if is_update_stock_data:
        if os.path.exists("data/stock_data.csv"):
            os.remove("data/stock_data.csv")
        update_stock_data()
    else:
        # 更新个股数据
        print("更新个股数据。")
        update_individual_stock_data()


if __name__ == "__main__":
    main()

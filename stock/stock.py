import baostock as bs
import pandas as pd
import os
import datetime


class Stock:
    def __init__(self):
        self.symbol = None

    def set_symbol(self, symbol):
        self.symbol = symbol

    def get_symbol(self):
        return self.symbol

    def get_start_date(self):
        if os.path.exists(f'data/{self.get_symbol()}.csv'):
            df = pd.read_csv(f'data/{self.get_symbol()}.csv')
            if not df.empty:
                start_date = pd.to_datetime(df['date'].iloc[-1]) + datetime.timedelta(
                    days=1)
                # print(pd.to_datetime(df['date'].iloc[-1]))
                if start_date >= pd.to_datetime('today', format='%Y-%m-%d'):
                    return pd.to_datetime('today').date().strftime('%Y-%m-%d')
                else:
                    return start_date.strftime('%Y-%m-%d')
            else:
                return '2026-01-01'
        else:
            return '2026-01-01'

    def get_end_date(self):
        datetime_today = datetime.date.today()
        return datetime_today.strftime('%Y-%m-%d')

    def fetch_data(self):
        if self.get_start_date() >= self.get_end_date():
            return None
        else:
            rs = bs.query_history_k_data_plus(code=self.symbol, start_date=self.get_start_date(), end_date=self.get_end_date(
            ), fields="date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST")
            if rs.error_code != '0':
                raise ValueError(f"Failed to fetch {self.get_symbol()} data.")
            else:
                return rs

    def to_dataframe(self):
        if self.fetch_data() is None:
            return pd.DataFrame()
        else:
            rs = self.fetch_data()
            data_list = []
            while rs.next():
                data_list.append(rs.get_row_data())
            if not data_list:
                return pd.DataFrame(columns=rs.fields)
            return pd.DataFrame(data_list, columns=rs.fields)

    # 判断股票数据文件是否存在且非空
    def is_data_file_valid(self):
        if os.path.exists(f'data/{self.get_symbol()}.csv'):
            df = pd.read_csv(f'data/{self.get_symbol()}.csv')
            return not df.empty
        return False

    def save_to_csv(self):
        df = self.to_dataframe()
        if df.empty:
            print(f"{self.get_symbol()} No new data to save.")
            return
        else:
            if self.is_data_file_valid():
                df.to_csv(f'data/{self.get_symbol()}.csv',
                          index=False, mode='a', header=False)
                print(f"Data appended to data/{self.get_symbol()}.csv")
            else:
                df.to_csv(f'data/{self.get_symbol()}.csv',
                          index=False, mode='a',header=True)
                print(f"Data saved to data/{self.get_symbol()}.csv")

    def stock_strategy_min_volume(self):
        df_all = pd.read_csv(f'data/{self.get_symbol()}.csv')
        df_part = df_all.tail(30)

        if df_part['volume'].iloc[-1] == df_part['volume'].min():
            print(f"Stock {self.get_symbol()} has the minimum volume in the last 30 days.\n")
            return self.get_symbol()


if __name__ == "__main__":

    stock = Stock()
    stock.set_symbol("sh.601919")  # Example stock symbol
    bs.login()
    stock.save_to_csv()
    bs.logout()

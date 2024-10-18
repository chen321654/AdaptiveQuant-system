import json
import requests
import pandas as pd
import datetime
from typing import Union
# from sqlalchemy import create_engine


def get_stock_data_k(
        code: str,
        start_date: Union[str, datetime.date] = '',
        end_date: Union[str, datetime.date] = '',
) -> pd.DataFrame:
    """
    获取股票历史K线数据，处理JSONP格式（来自提供的API端口）。
    """
    if start_date:
        start_date = start_date.replace('-', '') if isinstance(start_date, str) else start_date.strftime('%Y%m%d')
    if end_date:
        end_date = end_date.replace('-', '') if isinstance(end_date, str) else end_date.strftime('%Y%m%d')

    # 默认获取足够多的历史数据
    limit = 100000

    # 构建请求URL
    url = f'https://push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery35108650244582749764_1728997834353&secid=0.{code}&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&klt=101&fqt=1&end={end_date}&lmt={limit}&_=1728997834401'

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"请求失败，状态码：{response.status_code}")

    # 去除JSONP回调函数部分
    jsonp_text = response.text
    json_str = jsonp_text[jsonp_text.index('(') + 1: jsonp_text.rindex(')')]

    # 解析JSON数据
    data = json.loads(json_str)

    if 'data' not in data or not data['data']:
        return None  # 返回None以便在主函数中处理

    # 获取K线数据
    kline_data = data['data']['klines']

    # 获取股票名称
    stock_name = data['data']['name']

    # 将每条数据按逗号分隔并构造DataFrame
    records = [item.split(',') for item in kline_data]
    df = pd.DataFrame(records, columns=[
        '日期', '开盘价', '收盘价', '最高价', '最低价', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率'])

    df['股票名称'] = stock_name
    df['股票代码'] = code
    # 数据类型转换
    df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d')  # 日期精确到日
    df[['开盘价', '收盘价', '最高价', '最低价', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率']] = df[
        ['开盘价', '收盘价', '最高价', '最低价', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率']].astype(
        float)

    df.set_index('日期', inplace=True)

    # 返回指定日期范围内的数据
    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        df = df[(df.index >= start_date) & (df.index <= end_date)]

    # 返回股票名称和数据
    return stock_name, df


def save_to_database(df: pd.DataFrame, stock_name: str, stock_code: str, engine):
    """
    将DataFrame数据保存到数据库。
    """
    # 创建表名：股票名称（股票代码）
    table_name = "tb_stock"
    df.to_sql(name=table_name, con=engine, if_exists='append', index=True)

    print(f"{stock_name} 数据已保存到数据库.")


# if __name__ == '__main__':
#     # 数据库连接字符串（MySQL）
#     DATABASE_URL = 'mysql+pymysql://root:123456@localhost:3306/aq_sys'
#     # 替换 username、password 和 database_name 为您的 MySQL 用户名、密码和数据库名称
#     engine = create_engine(DATABASE_URL)
#
#     # 设置开始和结束日期
#     start_date = '2023-10-16'
#     end_date = '2024-10-15'
#     #df = get_stock_data_k('300001', start_date=start_date, end_date=end_date)
#    # print('股票历史K线数据:\n', df)
#
#     for code in range(300001, 300010):
#         stock_code = str(code)
#         try:
#             stock_name, df = get_stock_data_k(stock_code, start_date=start_date, end_date=end_date)
#             if df is not None and not df.empty:
#                 save_to_database(df, stock_name, stock_code, engine)
#             else:
#                 print(f"{stock_code} 没有数据或数据为空。")
#         except Exception as e:
#             print(f"处理股票代码 {stock_code} 时出错: {e}")

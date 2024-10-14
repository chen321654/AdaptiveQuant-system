import json
import requests
import datetime
import pandas as pd
from typing import List, Union


def get_price_day_tx(
        code: str, start_date: Union[str, datetime.date] = '', end_date: Union[str, datetime.date] = '',
        frequency: str = '1d'
) -> pd.DataFrame:
    """
    获取腾讯接口的日线、周线、月线数据。

    Args:
        code (str): 股票代码。
        start_date (str or datetime.date): 起始日期，格式为'YYYY-MM-DD'。
        end_date (str or datetime.date): 结束日期，格式为'YYYY-MM-DD'。
        frequency (str): 数据频率，默认为'1d'（日线），可选'1w'（周线）、'1M'（月线）。

    Returns:
        pd.DataFrame: 包含时间、开盘价、收盘价、最高价、最低价和成交量的数据表。
    """
    unit = 'week' if frequency == '1w' else 'month' if frequency == '1M' else 'day'

    if start_date:
        start_date = start_date.strftime('%Y-%m-%d') if isinstance(start_date, datetime.date) else \
        start_date.split(' ')[0]
    if end_date:
        end_date = end_date.strftime('%Y-%m-%d') if isinstance(end_date, datetime.date) else end_date.split(' ')[0]

    # 计算天数差
    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        count = (end_date - start_date).days + 1
    else:
        count = 10  # 默认获取10天数据

    # 生成API请求URL
    url = f'http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={code},{unit},,{end_date},{count},qfq'
    response = requests.get(url)
    data = json.loads(response.content)

    # 解析数据
    ms = 'qfq' + unit
    stock_data = data['data'][code]
    buf = stock_data.get(ms, stock_data.get(unit))  # 如果没有qfq数据，使用非复权数据
    df = pd.DataFrame(buf, columns=['time', 'open', 'close', 'high', 'low', 'volume'], dtype='float')
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)

    # 返回指定日期范围内的数据
    if start_date and end_date:
        df = df[(df.index >= start_date) & (df.index <= end_date)]

    return df


def get_price_sina(
        code: str, start_date: Union[str, datetime.date] = '', end_date: Union[str, datetime.date] = '',
        count: int = 10, frequency: str = '60m'
) -> pd.DataFrame:
    """
    获取新浪接口的全周期数据，包括分钟线、日线、周线、月线。

    Args:
        code (str): 股票代码。
        start_date (str or datetime.date): 起始日期，格式为'YYYY-MM-DD'。
        end_date (str or datetime.date): 结束日期，格式为'YYYY-MM-DD'。
        count (int): 获取的记录条数，默认为10。
        frequency (str): 数据频率，支持'1m', '5m', '15m', '30m', '60m', '1d', '1w', '1M'。

    Returns:
        pd.DataFrame: 包含时间、开盘价、收盘价、最高价、最低价和成交量的数据表。
    """
    frequency = frequency.replace('1d', '240m').replace('1w', '1200m').replace('1M', '7200m')
    ts = int(frequency[:-1])

    url = f'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={code}&scale={ts}&ma=5&datalen={count}'
    response = requests.get(url)
    data = json.loads(response.content)

    df = pd.DataFrame(data, columns=['day', 'open', 'high', 'low', 'close', 'volume'])
    df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
    df['day'] = pd.to_datetime(df['day'])
    df.set_index('day', inplace=True)

    # 返回指定日期范围内的数据
    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        df = df[(df.index >= start_date) & (df.index <= end_date)]

    return df


def get_price(
        code: str, start_date: Union[str, datetime.date] = '', end_date: Union[str, datetime.date] = '',
        frequency: str = '1d', fields: List[str] = []
) -> pd.DataFrame:
    """
    获取指定股票的历史数据，自动选择腾讯或新浪接口。

    Args:
        code (str): 股票代码，格式如'SZ160637'。
        start_date (str or datetime.date): 起始日期，格式为'YYYY-MM-DD'。
        end_date (str or datetime.date): 结束日期，格式为'YYYY-MM-DD'。
        frequency (str): 数据频率，支持'1d', '1w', '1M', '1m', '5m', '15m', '30m', '60m'。
        fields (List[str]): 需要返回的字段，默认为空表示返回所有字段。

    Returns:
        pd.DataFrame: 包含历史行情数据的DataFrame。
    """
    # 证券代码兼容处理
    xcode = code.replace('.XSHG', '').replace('.XSHE', '')
    xcode = 'sh' + xcode if 'XSHG' in code else 'sz' + xcode if 'XSHE' in code else code

    # 计算天数差
    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        count = (end_date - start_date).days + 1
    else:
        count = 10  # 默认获取10天数据

    # 根据频率选择不同的数据源
    if frequency in ['1d', '1w', '1M']:  # 日线、周线、月线
        try:
            return get_price_sina(xcode, start_date=start_date, end_date=end_date, count=count, frequency=frequency)
        except Exception:
            return get_price_day_tx(xcode, start_date=start_date, end_date=end_date, frequency=frequency)

    elif frequency in ['1m', '5m', '15m', '30m', '60m']:  # 分钟线
        try:
            return get_price_sina(xcode, start_date=start_date, end_date=end_date, count=count, frequency=frequency)
        except Exception:
            # return get_price_min_tx(xcode, end_date=end_date, count=count, frequency=frequency)
            pass

    return pd.DataFrame()  # 如果频率不匹配，返回空的DataFrame


if __name__ == '__main__':
    # 示例调用方法
    df = get_price('SZ000002', '2020-01-01', '2024-1-1', frequency='1d')
    df.to_excel('data.xlsx', index=False)
    print('历史行情数据:\n', df)

import datetime
import json
from decimal import Decimal

import pandas as pd

from django.http import JsonResponse, HttpResponse
from django.views import View

from apps.DataShow.models import Stock
from utils.views import LoginRequiredJSONMixin
from utils.getStockData import get_stock_data_k
from utils.Api import invokeApi


class DataGetView(View):
    def get(self, request):
        # 设置开始和结束日期
        start_date = datetime.date.today()
        end_date = datetime.date.today()
        for code in range(300001, 301000):
            stock_code = str(code)
            try:
                stock_name, df = get_stock_data_k(stock_code, start_date=start_date, end_date=end_date)
                df = df.reset_index()
                records = df.to_records(index=False)
                records = list(records)
                for record in records:
                    item = Stock(
                        股票名称=record['股票名称'],
                        股票代码=record['股票代码'],
                        日期=pd.to_datetime(record['日期']),
                        开盘价=Decimal(record['开盘价']),
                        收盘价=Decimal(record['收盘价']),
                        最高价=Decimal(record['最高价']),
                        最低价=Decimal(record['最低价']),
                        成交量=int(record['成交量']),
                        成交额=Decimal(record['成交额']),
                        振幅=Decimal(record['振幅']),
                        涨跌幅=Decimal(record['涨跌幅']),
                        涨跌额=Decimal(record['涨跌额']),
                        换手率=Decimal(record['换手率'])
                    )
                    item.save()
            except Exception as e:
                print(f"处理股票代码 {stock_code} 时出错: {e}")

        return JsonResponse({"code": 200})


class DataShowView(View):
    def get(self, request):
        data = json.loads(request.body)
        stock_data = invokeApi(data)
        # 从 requests.Response 提取内容、状态码和 headers
        content = stock_data.content  # 获取响应内容
        status_code = stock_data.status_code  # 获取响应状态码
        headers = stock_data.headers  # 获取响应头

        # 构建 Django 的 HttpResponse 对象
        response = HttpResponse(content=content, status=status_code)

        # 设置 headers，过滤掉 hop-by-hop 头部
        hop_by_hop_headers = ['Connection', 'Keep-Alive', 'Proxy-Authenticate',
                              'Proxy-Authorization', 'TE', 'Trailers',
                              'Transfer-Encoding', 'Upgrade']

        for key, value in headers.items():
            if key not in hop_by_hop_headers:
                response[key] = value

        return response

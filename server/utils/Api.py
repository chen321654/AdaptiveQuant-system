import json
import time
import urllib.parse
import requests
import uuid


def invokeApi(data):
    # 生成唯一的 trace 值
    unique_id = str(uuid.uuid4())
    timestamp = str(int(time.time() * 1000))  # 毫秒级时间戳
    trace = f"{unique_id}-{timestamp}"

    # 设置请求头
    headers = {
        'Content-Type': 'application/json'
    }

    # 构造 queryData 的 JSON 数据
    query_data = {
        "trace": trace,
        **data
    }

    # 将 queryData 转换为 JSON 字符串
    query_json = json.dumps(query_data)

    # 使用 urllib.parse.quote 对 JSON 字符串进行 URL 编码
    encoded_query = urllib.parse.quote(query_json)

    # 构造完整的 URL
    base_url = ("https://quote.tradeswitcher.com/quote-stock-b-api/kline?token=daf8a18427b0f12a74e8043bb533dd27-c-app"
                "&query=")
    full_url = base_url + encoded_query

    # 发起 GET 请求
    resp = requests.get(url=full_url, headers=headers)

    # 返回请求响应
    return resp


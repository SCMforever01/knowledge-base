import base64

def encode_base64(original_string):
    """
    对给定字符串进行 Base64 编码。

    :param original_string: 要编码的原始字符串
    :return: Base64 编码后的字符串
    """
    encoded_bytes = base64.b64encode(original_string.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

def decode_base64(encoded_string):
    """
    对给定的 Base64 编码字符串进行解码。

    :param encoded_string: 要解码的 Base64 编码字符串
    :return: 解码后的原始字符串
    """
    decoded_bytes = base64.b64decode(encoded_string)
    return decoded_bytes.decode('utf-8')


# 编码示例
original = "sWvCucu4BIsWVNU35E32FF_18RaqHNgL"
encoded = encode_base64(original)
print(f"原始字符串: {original}")
print(f"Base64 编码: {encoded}")

# 解码示例
decoded = decode_base64(encoded)
print(f"解码后的字符串: {decoded}")

import json
import hashlib
import base64
import requests

def call(url, param_map, app_id, app_key):
    # 将参数字典转换为 JSON 字符串
    body = json.dumps(param_map)

    # 生成签名（MD5加密）
    sign = hashlib.md5((app_id + body + app_key).encode('utf-8')).hexdigest().upper()

    # 构造 header 和 body
    json_data = {
        "header": {
            "appid": app_id,
            "sign": sign
        },
        "body": body
    }

    # 对 JSON 数据进行 base64 编码
    data = base64.b64encode(json.dumps(json_data).encode('utf-8')).decode('utf-8')

    # 发送 POST 请求
    response = requests.post(url, data={'data': data})

    return response


url = "https://api.id.mioffice.cn/api/account/findUidByUserName"
param_map = {
    "userName": "shichunming"
}
app_id = "knowledge-base"
app_key = "b840fa0d283c421cb82d2c8990bbf20b"

# response = call(url, param_map, app_id, app_key)
# print(response.text)

uid = "269596f9f098449f8d05be78ae76225e"
param_map1 = {
    "uid": uid
}
url1 = "https://api.id.mioffice.cn/api/department/queryFullDeptByUid"
# response = call(url1, param_map1, app_id, app_key)
# print(response.text)

import requests


class HttpRequest:
    def __init__(self, base_url):
        """
        初始化请求类，可以设置一个基础 URL
        """
        self.base_url = base_url

    def send_request(self, endpoint, method="GET", headers=None, params=None, data=None, json=None, timeout=10):
        """
        通用请求方法，根据请求方法发送不同的请求
        :param endpoint: API的接口地址（不包含基础URL）
        :param method: HTTP方法，默认为 GET
        :param headers: 请求头，默认无
        :param params: URL参数，适用于GET请求，默认为无
        :param data: 表单数据，适用于POST请求
        :param json: JSON格式的请求体数据
        :param timeout: 超时时间，默认10秒
        :return: 返回响应对象或错误信息
        """
        url = self.base_url + endpoint
        method = method.upper()

        try:
            if method == "GET":
                response = requests.get(url, headers=headers, params=params, timeout=timeout)
            elif method == "POST":
                response = requests.post(url, headers=headers, params=params, data=data, json=json, timeout=timeout)
            elif method == "PUT":
                response = requests.put(url, headers=headers, params=params, data=data, json=json, timeout=timeout)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, params=params, timeout=timeout)
            else:
                return f"不支持的请求方法: {method}"

            # 检查响应状态码
            response.raise_for_status()  # 若状态码非 200，抛出HTTPError
            return response  # 成功时返回响应对象

        except requests.exceptions.HTTPError as http_err:
            return f"HTTP 错误: {http_err}"
        except requests.exceptions.RequestException as req_err:
            return f"请求异常: {req_err}"


localhost_base_url = "http://localhost:9000/api/knowledge-base"
staging_base_url = "http://knowledge-base-staging.c5-cloudml.xiaomi.srv/knowledge-base"
client = HttpRequest(staging_base_url)

data = {
    "ns_name": "ktest189341b1a29b242001846804272222703616",
    "name": "ceshi",
    "department": "1"
}

headers = {
    "Content-Type": "application/json",
    "X-User-Name": "shichunming"
}

# response = client.send_request("/manage/trans", headers=headers, method="POST", json=data)
#
# if isinstance(response, requests.Response):
#     if response.headers.get("Content-Type") == "application/json":
#         print(response.json())  # 服务器返回JSON格式时
#     else:
#         print(response.text)  # 非JSON响应
# else:
#     print(response)  # 错误信息


# response = client.send_request("", method="GET", headers={"X-User-Name": "shichunming"})
# if isinstance(response, requests.Response):
#     print(response.json())
# else:
#     print(response)  # 错误信息

response = client.send_request("/getUser", method="GET",params={"name": "shichunming"}, headers={"X-User-Name": "shichunming"})
if isinstance(response, requests.Response):
    print(response.json())
else:
    print(response)  # 错误信息

# 学习制作网易云音乐客户端。
# 此文件实现登陆查询等一系列功能。

"""
4.10日。
"""
import requests
import hashlib


def shotlist(lst):
	"""列表去重。"""
	temp1 = sorted(list(set(lst)))
	return temp1


class WebApi:
	"""一些功能。"""
	# def __init__(self):
	default_timeout = 10
	headers = {
		'Accept': '*/*',
		'Accept-Encoding': 'gzip,deflate,sdch',
		'Accept-Language': 'zh-CN,zh;q=0.8',
		'Proxy-Connection': 'keep-alive',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Host': 'music.163.com',
		'Referer': 'http://music.163.com/',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
	}


	def httpRequest(self, action, method="GET", add=None, data=None, headers=headers, cookies='', timeout=default_timeout, urlencode='utf-8'): 
		"""
					默认以get方式请求，
					GET方式附加内容用add参数，POST方式提交内容用data参数。
					编码用urlencode参数，默认utf-8。
					GET方式以文本形式返回请求的内容。
					POST方式返回cookies和文本形式的内容。(0,1)
					默认cookies为空。
		"""
		if method.upper() == 'GET':
			if add:
				html = requests.get(action, params=add, headers=headers, cookies=cookies, timeout=timeout)
			else:
				html = requests.get(action, headers=headers, cookies=cookies, timeout=timeout)
			html.encoding = urlencode
			return html.text
		elif method.upper() == 'POST':
			if data:
				html = requests.post(action, data=data, headers=headers, cookies=cookies, timeout=timeout)
			else:
				html = requests.post(action, headers=headers, cookies=cookies, timeout=timeout)
			html.encoding = urlencode
			return html.cookies, html.text

	def login(self, username, password):
		"""
					以网易账号登陆，其他的登陆待写。返回cookies。
		"""
		data = {
			'username': username,
			'password': hashlib.md5(password.encode('utf-8')).hexdigest(),
			'remeberLogin': 'true'
		}
		cki = self.httpRequest('http://music.163.com/api/login', method="POST", data=data)	
		return cki[0]


if __name__ == '__main__':
	main = WebApi()
	cookies = main.login('b754048538@163.com', 'yuan97')
	req = requests.post('http://music.163.com/', headers=main.headers, cookies=cookies)
	print(req.text)
#coding=utf-8

import os
import sys
import shlex
import requests
from bs4 import BeautifulSoup

# 前置
# 安装 you-get
# pip3 install BeautifulSoup4
# pip3 install requests


# 简单的脚本, 没有处理剧集分页的情况, 需要手动点击分页后的那一集然后贴地址到这里. 
# 以 神探狄仁杰第二部 为例, 这部电视剧有 40 集, 先点击第 1 集,
# 获取第一页前 30 集的地址, 然后点 31 集, 复制 31 集的地址到这里,
# 获取后 10 集的地址.
url = 'https://v.youku.com/v_show/id_XNjQwNTc5NDY0OA==.html?spm=a2hkm.8166622.PhoneSokuProgram_1.dchapters_1&s=cfcf39dd33c2455396b3'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


html = requests.get(url, headers=headers).text
soup = BeautifulSoup(html, features="html.parser")
links = soup.find_all("a", class_="sn")

if len(links) == 0:
	sys.exit("获取剧集列表失败")

# 是否不保存链接直接下载.
download = True

if download:
	for link in links[1:]:
		addr = 'https:' + link.get('href')
		print("Downloading " + addr)

		# 是否使用 Cookies. 替换你自己的路径.
		using_cookies = False
		cookies = '/Users/wangminjie/Downloads/cookies.txt ' if using_cookies else ''
		
		output_path = '-o ' + shlex.quote(soup.title.string) + ' ' if len(soup.title.string) > 0 else ''

		cmd = '$(which you-get) ' + output_path + cookies + addr
		# cmd = '~/GitHub/you-get/you-get ' + output_path + cookies + addr
		os.system(cmd)
else:
	filename = (soup.title.string if len(soup.title.string) > 0 else 'youku_url_list') + '.txt'
	with open(filename, 'a') as out:
		for link in links:
			addr = 'https:' + link.get('href')
			print(addr)
			out.write(addr + '\n')

	print("保存完毕")
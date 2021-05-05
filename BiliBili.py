import requests

url = 'https://api.live.bilibili.com/msg/send'

header = {
    'cookie': '_uuid=C6690AA3-56E1-D859-1A3B-EBD02593DF7815721infoc; bsource=search_baidu; buvid3=07AD3BAA-EC75-46D2-AD8E-93E57482E87C34786infoc; sid=9u19v9hd; fingerprint=e4a6e51b1cb9941d46d3e350330aecea; buvid_fp=07AD3BAA-EC75-46D2-AD8E-93E57482E87C34786infoc; buvid_fp_plain=84E6B7FB-C0A9-4E57-91FA-9AD775BCE35B143109infoc; DedeUserID=413435897; DedeUserID__ckMd5=b1468a8c2ec40637; SESSDATA=1c4b992d,1635646151,ea15a*51; bili_jct=ce050424c816fa1d025960042e66554b; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(J|kY))mumR0J\'uYk||mRuYk; _dfcaptcha=e52746ca1bafeb7245f5849ce1581c0c; LIVE_BUVID=AUTO9116200942839585; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1620094316; Hm_lpvt_8a6e55dbd2870f0f5bc9194cddf32a02=1620094316; PVID=2'
    ,
    'User-Agent': 'Chrome/90.0.4430.93'
}
data = {
    'bubble': '0',
    'msg': '主播讲的真好',
    'color': '16777215',
    'mode': '1',
    'fontsize': '25',
    'rnd': '1620094283',
    'roomid': '4507559',
    'csrf': 'ce050424c816fa1d025960042e66554b',
    'csrf_token': 'ce050424c816fa1d025960042e66554b'
}
res = requests.post(url, data=data, headers=header).text
cookies = requests.session().cookies.get_dict()
print(cookies)
print(res)

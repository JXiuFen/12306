import requests
import urllib.request
import json
import re
import time
from PIL import Image
session=requests.Session()
headers={
"Cookie": "_passport_session=4d8df9e2547446928be72944a5ae28b47124; _passport_ct=bdb38ed444904267a57f9d72663cf8a5t7064; _jc_save_wfdc_flag=dc; _jc_save_toDate=2019-04-17; _jc_save_toStation=%u9633%u897F%2CWMQ; _jc_save_fromDate=2019-04-18; _jc_save_fromStation=%u6C5F%u95E8%u4E1C%2CJWQ; BIGipServerotn=4007067914.50210.0000; RAIL_EXPIRATION=1556008518681; RAIL_DEVICEID=JGfnZOmnBKXOpaaVGA16L_moRtYYxbqq5HSw7Adx3s41cO2rpUC9s5IzsrSuqZ3fC4DQkpVLifCWZGrIx1pejmJd1QZfjdpBVQk6wVPMjbAlFmZb3e0w9yfARUu1kcJzp_01ctKhNTfRzQYczgL_a7n7UujD7qzz; BIGipServerpassport=786956554.50215.0000; route=9036359bb8a8a461c164a04f8f50b252; BIGipServerpool_passport=317522442.50215.0000",
	"Host": "kyfw.12306.cn",
"Origin": "https://kyfw.12306.cn",
"Referer": "https://kyfw.12306.cn/otn/resources/login.html",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.64 Safari/537.36",
"X-Requested-With": "XMLHttpRequest"
}

#获取图片位置坐标
class Ver(object):
	@classmethod
	def ver_number(cls,num):
		num_list=[]
		for i in num.split("."):
			if i=='1':
				num_list.append('35,70')
			if i=='2':
				num_list.append('110,70')
			if i == '3':
				num_list.append('180,70')
			if i == '4':
				num_list.append('250,70')
			if i == '5':
				num_list.append('35,150')
			if i == '6':
				num_list.append('110,150')
			if i == '7':
				num_list.append('180,150')
			if i == '8':
				num_list.append('250,150')
		# print(",".join(num_list))
		return ",".join(num_list)

#验证验证码的正确
class Inspection_code(object):
	@classmethod
	def ins_code(cls,code):
		#验证码校验的URL
		url_3="https://kyfw.12306.cn/passport/captcha/captcha-check?callback=jQuery19105078130602797195_1555379868782&answer={}&rand=sjrand&login_site=E&_=1555379868788".format(Ver.ver_number(code))  #code是验证码的坐标，这是我自己写的函数获取坐标的
		result_code=session.get(url=url_3,headers=headers)
		result_code.encoding='utf-8'
		#获取返回的信息，可能返回验证码校验成功，或失败
		result_message=re.findall('"result_message":".*?","result_code":"(.*?)"',result_code.text)[0]
		return result_message

#登录
class Login(object):
	@classmethod
	def logn(cls,code):
		url_1 = "https://kyfw.12306.cn/passport/web/login"  # 登录url
		data_login = {
			"username": "xxxxxxx",#账号
			"password": "xxxxxxx",#密码
			"appid": "otn",
			"answer": Ver.ver_number(code)#验证码的坐标
		}
		result_logn = session.post(url=url_1, headers=headers, data=data_login)
		result_logn.encoding = 'utf-8'
		# print(result_logn.text)
		#获取cookies值，用于验证是否已经登录成功的
		cookies = requests.utils.dict_from_cookiejar(result_logn.cookies)
		result_message=re.findall('"result_message":"(.*?)","result_code"',result_logn.text)[0]
		print(result_message+"!")
		return  cookies

#保存验证图片
def save_code_img():
	# 验证码图片生成的URL
	url_2 = "https://kyfw.12306.cn/passport/captcha/captcha-image64?login_site=E&module=login&rand=sjrand&1555379925163&callback=jQuery19105078130602797195_1555379868782&_=1555379868783"
	result_jmp=session.get(url=url_2,headers=headers).text
	# 获取验证码图片URL
	jmp_url=re.findall('"image":"(.*?)","result_message"',result_jmp)[0]
	#保存验证码图片
	urllib.request.urlretrieve("data:image/jpg;base64,"+jmp_url,'code.jpg')

#个人用户界面
def main():
	save_code_img()
	print("=======================")
	print("模拟登陆12306")
	time.sleep(2)
	# 打开验证码图片
	im = Image.open('code.jpg')
	im.show()
	time.sleep(1)
	code=input("请输入验证码的位置(格式:1.2):")

	if Inspection_code.ins_code(code)=='4':
		print("验证成功！")
		cookies=Login.logn(code)
	else:
		print("验证失败，重新输入")
		code = input("请输入验证码的位置(格式:1.2):")
		if Inspection_code.ins_code(code) == '4':
			print("验证成功！")
			cookies=Login.logn(code)
		else:
			print("验证再次失败，重新输入")
			code = input("请输入验证码的位置(格式:1.2):")
			if Inspection_code.ins_code(code) == '4':
				print("验证成功！")
				cookies=Login.logn(code)
			else:
				exit("验证失败!")

	headers={
		"Host": "kyfw.12306.cn",
	"Origin": "https://kyfw.12306.cn",
	"Referer": "https://kyfw.12306.cn/otn/resources/login.html",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.64 Safari/537.36",
	"X-Requested-With": "XMLHttpRequest"
	}
	#验证登录是否成功的URL
	uamtk_url = "https://kyfw.12306.cn/passport/web/auth/uamtk-static"
	data_uamtk = {'appid': 'otn', }
	html_uamtk = session.post(uamtk_url, headers=headers, cookies=cookies, data=data_uamtk)
	html_uamtk.encoding = 'utf-8'
	result_code=json.loads(html_uamtk.text)
	if result_code['result_code']==0:
		print("状态：{}    用户：{}".format(result_code["result_message"],result_code["name"]))
	else:
		print(result_code["result_message"]+'!')

if __name__ == '__main__':
    main()
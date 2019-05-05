import requests
import socks
import time
import zlib
import re
import socket
#My module start
import webengine
import language
import category_
#My moudle end 
from urllib.parse import unquote
from bs4 import BeautifulSoup
from pytz import timezone
from datetime import datetime

#Time format 
fmt = "%Y-%m-%d %H:%M:%S %Z%z"

#Url REGEX
ANY_URL_REGEX = "^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"

session=requests.session()
session.proxies = {'http':  'socks5h://localhost:9050',
	               'https': 'socks5h://localhost:9050'}
def category_return(text,languages_code):
	if(languages_code =='en' or languages_code =='un'):
		category,keywords=category_.analysis(text).enC()
	elif(languages_code=='de'):
		category,keywords=category_.analysis(text).deC()
	elif(languages_code=='ko'):
		category,keywords=category_.analysis(text).koC()
	elif(languages_code=='ja'):
		category,keywords=category_.analysis(text).jaC()
	elif(languages_code=='es'):
		category,keywords=category_.analysis(text).esC()
	elif(languages_code=='it'):
		category,keywords=category_.analysis(text).itC()
	elif(languages_code=='ru'):
		category,keywords=category_.analysis(text).ruC()
	elif(languages_code.find('zh')>=0):
		category,keywords=category_.analysis(text).zh_cnC()
	else:
		category,keywords=category_.analysis(text).enC()

	if(category!='unknown'):
		keywrods_str=list(set(keywords))
		keywords_str=''
		for i in keywords:
			keywords_str+=i+','
		keywords_str=keywords_str[:-1]

	return(category,keywords)
	
	
def analysis(url):
	status='None'
	server='None'
	code='None'.encode('utf-8')
	title='None'.encode('utf-8')
	nowtime = datetime.now(timezone('Asia/Seoul')).strftime(fmt)[:-9]
	try:
			res=session.get(url,timeout=10,headers={'Connection':'close'})
			status=res.status_code
			requests_txt=res.text

			Soup=BeautifulSoup(requests_txt,"html.parser")
			
			# source get
			if (Soup.find('html') is not None):
				code=str(Soup.find('html')).encode('utf-8')
			else:
				code=(res.text).encode('utf-8')

			# title tag  
			if (Soup.find('title') is not None):
				title=Soup.find('title').get_text().encode('utf-8')
			elif (Soup.find('TITLE') is not None):
				title=Soup.find('TITLE').get_text().encode('utf-8')

			# Check 'server' in header 
			if('server' in list(res.headers.keys())):
				server=res.headers['server']
			elif('Server' in list(res.headers.keys())):
				server=res.headers['Server']
			
			# language analysis 
			textcode,languages=language.analysis(requests_txt)
			
			# category analysis
			category,keywords=(category_return(title.decode('utf-8'),languages[0]))
			
			# if not found category in title text , more anyalas page text code
			if(category=='unknown'):
				category,keywords=(category_return(textcode,languages[0]))

			language1=languages[0]
			language2=languages[1]
			language3=languages[2]
			code=zlib.compress(code)
			url_box=[]
			for a_tag in (Soup.find_all('a',href=True)):
				url_box.append(a_tag['href'])
			for form_tag in (Soup.find_all('form',action=True)):
				url_box.append(form_tag['action'])
			for iframe_tag in Soup.find_all('iframe',src=True):
				url_box.append(iframe_tag['src'])
			for img_tag in Soup.find_all('img',src=True):
				url_box.append(img_tag['src'])
			if(len(url_box)>=2):
				url_box=list(set(url_box))
			onion_box=[]

			keywords=','.join(list(set(keywords)))
			for url_one in url_box:
					if(re.findall(ANY_URL_REGEX,url_one)!=[]):
						if(url_one.find('.onion')>=0):
							onion_box.append(url_one[:url_one.find('.onion')+6])
			onion_box=list(set(onion_box))
			status=res.status_code
			return (category,keywords,url,nowtime,status,server,code,title,language1,language2,language3,onion_box)

	except requests.exceptions.ConnectionError as e:
			# Sockect is max Error
			return ('unknown','unknown',url,nowtime,'unknown','unknown','unknown','unknown','unknown','unknown','unknown','unknown')
	except requests.exceptions.ReadTimeout as e:
			# Connect fail (time out)
			return ('unknown','unknown',url,nowtime,'unknown','unknown','unknown','unknown','unknown','unknown','unknown','unknown')
		
	except Exception as e:
			# Error
			return ('unknown','unknown',url,nowtime,'unknown','unknown','unknown','unknown','unknown','unknown','unknown','unknown')
	


def report (url,engine, recursion_count):
	category,keywords,url,nowtime,status,server,code,title,language1,language2,language3,url_box=analysis(url)
	password='server connect password'
	if(status!='unknown'):
		data={'category':category,'keyword':keywords,'engine':engine,'url':url,'time':nowtime,'state':status,'server':server,'code':str(code),'title':title,'language1':language1,'language2':language2,'language3':language3,'password':password}
		res=requests.post('http://intadd.kr/darkup/saveinfo.php',data=data)
		print (res)
		print (url)
		if(recursion_count<=2 and type(url_box)==list):
			if(url in url_box):
				url_box.remove(url)

			#recursion_start
			for urls in url_box:
					report (urls,url, recursion_count+1)
			
def ResultToServer(onion_info):
	recursion_count=1
	for onion_url in onion_info.keys():
				onion_engine=onion_info[onion_url]
				report(onion_url,onion_engine,recursion_count)

def main  ():
	print ('[*] Start [*]')
	keyword=category_.search_keyword_list()
	for Word in keyword:
				search_class=webengine.onion_parser(Word,session)
				dicts={}
				torSearchvalue={'torSearch':search_class.torSearch()}
				print ('tordone')
				candlevalue={'candle':search_class.candle()}
				print ('candle done')
				dicts.update(webengine.Deduplication(torSearchvalue,candlevalue,'init'))
				dicts.update(webengine.Deduplication(dicts,{'ahmia':search_class.ahmia()},'combine'))
				dicts.update(webengine.Deduplication(dicts,{'visitor':search_class.visitor()},'combine'))
				ResultToServer(dicts)
		
main()

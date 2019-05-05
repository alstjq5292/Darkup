from bs4 import BeautifulSoup
import requests
import time
from urllib.parse import unquote


class onion_parser(object):

	def __init__(self,keyword,session):
		self.key_word=keyword
		self.session=session
	

	def torSearch(self):
		
		query='cmd=Search!&q='+self.key_word
		base_url='http://xmh57jrzrnw6insl.onion/4a1f6b371c/search.cgi?'
		url=base_url+query
		proxies = {'http':  'socks5h://localhost:9050',
		                    'https': 'socks5h://localhost:9050'}

		while(1):
			try:
							origin=self.session.get(url,proxies=proxies,headers={'Connection':'close'})
							origin.close()
							break
			except Exception as e:
							time.sleep(5)
		
		Soup=BeautifulSoup(origin.text,'html.parser')

		if(origin.text.find('Sorry, your search for')>=0):
			return ([])
		for small in Soup.find_all("small"):
			if(small.get_text().find("Results")>=0):
				search_len=int((small.get_text()[small.get_text().find('of ')+3:len(small.get_text())-1]))
				break

		all_url=[]

		if(search_len /100 >0):
			for i in range(0,int(search_len/100)):

				search_query=base_url+query+'&ps=100&q=card&s=RPD&np='+str(i)
				try:
					res=self.session.get(search_query,proxies=proxies,headers={'Connection':'close'})
					res.close()
					if(res.text.find('Sorry, your search for')>=0):
						break
					Soup=BeautifulSoup(res.text,'html.parser')
				except Exception as e:
					continue

				for j in (Soup.find_all('a',href=True)):
					if(j['href'][:7]=='http://'):
						all_url.append(j['href'][:j['href'].find('onion')+5])
						all_url=list(set(all_url))			

		all_url=list(set(all_url))
		return (all_url)

	def ahmia(self):
		url='http://msydqstlz2kzerdg.onion/search/?q='+self.key_word
		#session.keep_alive = False
		proxies = {'http':  'socks5h://localhost:9050',
		                            'https': 'socks5h://localhost:9050'}
		all_url=[]
		while(1):
			try:
				origin=self.session.get(url,proxies=proxies,headers={'Connection':'close'})
				origin.close()
				break
			except Exception as e:
				time.sleep(5)

		if(origin.text.find("Sorry, but Ahmia couldn't find ")>=0):
			return (all_url)
			
		Soup=BeautifulSoup(origin.text,'html.parser')

		for i in Soup.find_all('a',href=True):
			if(i['href'].find('.onion')>0 and i['href'].find('http://')>0):
				all_url.append (i['href'][i['href'].find('http://'):i['href'].find('.onion')+6])
		
		return (list(set(all_url)))

	def candle(self):
		proxies = {'http':  'socks5h://localhost:9050',
		                            'https': 'socks5h://localhost:9050'}
		url='http://gjobqjj7wyczbqie.onion/?q='+self.key_word
		res=self.session.get(url,proxies=proxies,headers={'Connection':'close'})
		soup=BeautifulSoup(res.text,'html.parser')
		all_url=[]
		for h2 in soup.find_all('h2'):
			if(h2.find('a')['href'].find('.onion')>0 and h2.find('a')['href'].find('http://')>=0):
				all_url.append(h2.find('a')['href'])

		return (list(set(all_url)))		
	def visitor(self):
		
		query='?q='+self.key_word
		base_url='http://visitorfi5kl7q7i.onion/search/'
		url=base_url+query

		while(1):
			try:
						origin=self.session.get(url)
						break
			except Exception as e:
						time.sleep(5)
		urlbox=[]	

		for i in range(1,10):
			search_url=url+'&page='+str(i)
			res=self.session.get(search_url)
			soup=BeautifulSoup(res.text,'html.parser')
			if(soup.get_text().find('http://visitorfi5kl7q7i.onion')==0):
					break
			soup=soup.find('ul',{'class':'steps'})
			for i in soup.find_all('li'):
				url_one=((i.find('a')['href']))

				url_one=url_one[:url_one.find('.onion')+6]
				urlbox.append(url_one)

		urlbox=list(set(urlbox))
		return (urlbox)



	'''
	def haystack(self):
		base_url='http://haystakvxad7wbk5.onion/?q=keyword&offset='.replace('keyword',self.key_word)
		url='http://haystakvxad7wbk5.onion/?q=keyword&offset=40'.replace('keyword',self.key_word)

		while(1):
			try:
				origin=self.session.get(url)
				print (origin)
				break
			except Exception as e:
				print (e)
				time.sleep(2)

		Soup=BeautifulSoup(origin.text,'html.parser')

		

		result_len=int((Soup.find('p').get_text())[Soup.find('p').get_text().find("Found ")+6:Soup.find('p').get_text().find(' result')])
		
		all_url=[]

		for i in range(0,int(result_len/20),20):
			query=base_url+str(i)
			try:
				res=self.session.get(query)
			except:
				continue
			Soup=BeautifulSoup(res.text,'html.parser')
			for j in Soup.find_all('a',href=True):
				if(j['href'][:19].find('redir.php?url=http')>=0):
					tmp=unquote(unquote(j['href']))
					url=tmp[tmp.find('http:'):tmp.find('onion')+5]
					all_url.append(url)
				all_url=list(set(all_url))
		all_url=list(set(all_url))
		return (all_url)


	'''
def Deduplication(*args):
        tmpA=list(args)[0]
        tmpB=list(args)[1]
        if(list(args)[2]=='init'):
                tmpAstring=list(tmpA.keys())[0]
                tmpBstring=list(tmpB.keys())[0]
                alls={}
                for i in tmpA[tmpAstring]:
                        if(tmpB[tmpBstring].count(i)>0):
                                        tmpB[tmpBstring].remove(i)
                                        alls.update({i:tmpAstring+' '+tmpBstring})
                        else:
                                        alls.update({i:tmpAstring})

                for j in tmpB[tmpBstring]:
                        alls.update({j:tmpBstring})

                return (alls)

        elif(list(args)[2]=='combine'):
                dicts=list(args)[0]
                tmpA=list(args)[1]
                tmpC=list(dicts.keys())

                tmpAstring=list(tmpA.keys())[0]

                for i in tmpA[tmpAstring]:

                                if(tmpC.count(i)>0):
                                        dicts.update({i:dicts[i]+' | '+tmpAstring})
                                else:
                                        dicts.update({i:tmpAstring})
                return (dicts)

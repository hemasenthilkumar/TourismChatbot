import nltk
import json
import pandas
import re
import random
from fuzzywuzzy import fuzz
import operator
import urllib
import urllib3
from urllib.parse import urlencode
import urllib.request as r
import googlemaps
from bs4 import BeautifulSoup
import re
import sys
import requests
s=""
def r1():
    return review(s)
def review(name):
    try:
        df=pandas.read_excel("G:/revs.xls")
        df.to_json(path_or_buf='F:/rev.json',orient='table')
        with open('F:/rev.json') as jd:
                    d=json.load(jd)
        for i in range(len(d['data'])):
                if(name== d['data'][i]['name']):
                        return d['data'][i]['reviews']
    except IndexError:
        return "No reviews"
def dist(o="vellore",t="chennai",m="driving"):
    try:
        if ((o != '') and (t != '') and (m != '')):
            api_key = 'AIzaSyDdd0tYnOw7-bLVpZvyTqn6F4JY_VZPh0k'
            base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
            origins = [o]
            destinations = [t]
            payload = {
                'origins': '|'.join(origins),
                'destinations': '|'.join(destinations),
                'mode': m,
                'api_key': api_key,
            }
            try:
                r = requests.get(base_url, params=payload)
                if r.status_code != 200:
                    return('HTTP status code {} received, program terminated.'.format(r.status_code))
                else:
                    x = json.loads(r.text)

                    for (isrc, src) in enumerate(x['origin_addresses']):

                        for (idst, dst) in enumerate(x['destination_addresses']):

                            row = x['rows'][isrc]

                            cell = row['elements'][idst]

                            if cell['status'] == 'OK':

                                return(('{} to {}: {}, {}.').format(src, dst,
                                                                   cell['distance']['text'],
                                                                   cell['duration']['text']))
                            else:

                                return(('{} to {}: status = {}').format(src, dst,
                                                                       cell['status']))
                    with open('gdmpydemo.json', 'w')as f:
                           f.write(r.text)
            except ConnectionError:
                return("Please check your internet net connection!")
            except urllib3.exceptions.NewConnectionError:
                return("Please check your internet net connection!")
            except urllib3.exceptions.MaxRetryError:
                return("Please check your internet net connection!")
            except requests.exceptions.ConnectionError:
                return("Please check your internet net connection!")
            except socket.gaierror:
                return("Please check your internet net connection!")
                
                
        else:
            return("Please make sure you include from<place>to<place> in your query!")


    except ValueError:
        return ('Error')
    except ConnectionError:
        return("Please check your internet net connection!")
    if sys.flags.interactive:
        from pprint import pprint

def key2(q):
	keyword=''
	add=['where can i find', 'where is', 'which place is', 'where can i find','address',"where to find","where i can find"]
	dis=["how far is","how long","how many km","how many kilometeres","time takes",'distance',"how far it is"]
	direc=["ways","directions","how to find","route","paths","how can i reach","how can i go to"]
	op=["darshan timings","opening hours","open timings","open hours","open"]
	ph=["phone number","number","contact","phone","call","contact details"]
	fe=["darshan fee","entry fee","money","pay","cost"]
	for i in add:
		if i in q:
			keyword="address"
	for i in dis:
		if i in q:
			keyword="distance"
	for i in direc:
		if i in q:
			keyword="directions"
	for i in op:
		if i in q:
			keyword="open"
	for i in ph:
		if i in q:
			keyword="phone"
	for i in fe:
		if i in q:
			keyword="entry fee"
	return keyword

def dowhat(q,d):
   try:
       l=[]
       k=key2(q)
       m=chinker(q)
       i=ques(m,d)
       if('suggest' in q):
           for r in range(5):
               j=random.randint(0,50)
               l.append(d['data'][j]['name'])
           return (",").join(l)
       if ('entry' in k) and ('fee' in k):
           return d['data'][i]['entry_fee']
       elif ('open' in k)or ('time' in k):
           return d['data'][i]['open_hours']
       elif 'address' in k:
           return d['data'][i]['address']
       elif 'phone' in k:
           return d['data'][i]['phone_number']
       else:
           return("Couldn't find answer for your query")

   except TypeError:
       return ("I cannot understand your question.")
   except Warning:
       return ("I cannot understand your question..")
   except KeyError:
       return("I couldn't find answer for your question")
def direc(q):
    try:
        l=placefinder(q)
        start=l[0]
        finish=l[1]
        url = 'http://maps.googleapis.com/maps/api/directions/json?%s' % urlencode((('origin', start),('destination', finish)))
        ur = r.urlopen(url).read().decode('UTF-8')
        result = json.loads(ur)
        l=[]
        if(result['status']=="NOT_FOUND"):
            print("not found")
        else:
            for i in range (0, len (result['routes'][0]['legs'][0]['steps'])):
                j = result['routes'][0]['legs'][0]['steps'][i]['html_instructions']
                soup=BeautifulSoup(j,"html.parser")
                text=soup.get_text()
                l.append(text)
        return(" ").join(l)
    except urllib.error.HTTPError:
        return("Enter your locations correctly!")
    except urllib.error.URLError:
	    return("Please make sure your internet connection is on!")
    except IndexError:
        return("Route not found")
    except ConnectionError:
        return("Please check your internet net connection!")

def placefinder(q):
    try:
        l=l=re.findall('from(.*?)to(.*?)$',q)[0]
        l=[x.strip() for x in l]
        return l
    except IndexError:
        l=[]
        return l

def ques(q,d):
    l=[]
    for i in range(60):
            l.append(fuzz.token_sort_ratio(q,d['data'][i]['name']))
    return l.index(max(l))

def chinker(cus):
 s1=nltk.pos_tag(nltk.word_tokenize(cus))
 grammer="""NP:
	{<.*>+}
	}<VBD|IN|MD|WRB|VB|DT>+{
	"""
 cp=nltk.RegexpParser(grammer)
 r=cp.parse(s1)
 d=[]
 for subtree in r.subtrees(filter=lambda t: t.label()=='NP'):
     d.append(" ".join([a for (a,b) in subtree.leaves()]))
 return (" ").join(d)

def user(c):
    try:
        global s
        cus=c.lower()
        count=0
        if(cus=='quit'):
            return("Bye")
        if not cus:
            return("I cannot understand your query")
        elif('temple' in cus)or('temples' in cus) or ('kovil' in cus):
            count=1
            df=pandas.read_excel("F:/temple_.xls")
            df.to_json(path_or_buf='F:/temple1.json',orient='table')
            with open('F:/temple1.json') as jd:
                d=json.load(jd)
            p=ques(cus,d)
            r=(dowhat(cus,d))
            s=d['data'][p]['name']
            if(r!="None"):
               return("I have found this:"+"  "+s+"  "+r)
        elif('lodge' in cus)or('stay' in cus):
            count=1
            df=pandas.read_excel("F:/lodge.xls")
            df.to_json(path_or_buf='F:/lod.json',orient='table')
            with open('F:/lod.json') as jd:
                d=json.load(jd)
            cus=cus.replace('lodge','')
            cus=cus.replace('stay','')
            r=(dowhat(cus,d))
            p=ques(cus,d)
            s=d['data'][p]['name']
            if(r!="None"):
              return("I have found this:"+"  "+s+"  "+r)
        elif('church' in cus):
            count=1
            df=pandas.read_excel("F:/Church.xls")
            df.to_json(path_or_buf='F:/church.json',orient='table')
            with open('F:/church.json') as jd:
                d=json.load(jd)
            r=(dowhat(cus,d))
            p=ques(cus,d)
            s=d['data'][p]['name']
            if(r!="None"):
                return("I have found this:"+"  "+s+"  "+r)
        elif('food' in cus)or('restaurant' in cus) or ('hotel' in cus) or('canteen' in cus):
            count=1
            df=pandas.read_excel("F:/Food.xls")
            df.to_json(path_or_buf='F:/food.json',orient='table')
            with open('F:/food.json') as jd:
                d=json.load(jd)
            cus=cus.replace('restaurent','')
            cus=cus.replace('hotel','')
            cus=cus.replace('canteen','')
            r=(dowhat(cus,d))
            p=ques(cus,d)
            s=d['data'][p]['name']
            if(r!="None"):
                 return("I have found this:"+"  "+s+"  "+r)
        elif(count==0):
                 k=key2(cus)
                 if('directions' in k):
                     return direc(cus)
                 if('distance' in k):
                     pl=placefinder(cus)
                     if(pl!=[]):
                         o=pl[0]
                         t=pl[1]
                         return dist(o,t)
                     else:
                         return("Please make sure you include from<place>to<place> in your query!")
                
        else:
            return("I cannot understand your query.Make sure to specify temple,stay or hotel in query!")
    except TypeError:
        return("Not found")

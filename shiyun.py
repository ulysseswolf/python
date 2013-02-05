import os
import sys
import MySQLdb
import urllib2
from BeautifulSoup import BeautifulSoup
import codecs
import datetime
import simplejson

reload(sys)
sys.setdefaultencoding('utf8')

today = datetime.date.today()
logname = '/py/shiyun-%s.log' % today
logfile = codecs.open(logname,'a',encoding='utf-8')

INSERT = u'INSERT IGNORE INTO SHIYUN_RAW (PK,MODEL,TITLE,DIRECTOR,ACTOR) VALUES (%s,%s,%s,%s,%s)'

def openDB():
        return MySQLdb.connect(host='10.100.1.42',port=3306,user='root',passwd='',db='test',charset='utf8')


def Log(str):
        logfile.write(str + '\n')

def parse():
	url = 'http://cord.tvxio.com/api/vendor/lenovo/items/?format=xml'
        #get shiyun response xml data
        response = urllib2.urlopen(url=url)
        xml = response.read()

        #parse xml data,get attributes
        soup = BeautifulSoup(xml)
        nodelist = soup.findAll('list-item')
        for content in nodelist:
                pk = content.pk.string
                model = content.content_model.string
                #if model=='trailer':
                        #continue
                title = content.title.string
		shiyunDetail(pk,title,model)
                #cursor.execute(INSERT,(pk,model,title))


        #conn.commit()
        #cursor.close()
        #conn.close()
        Log('mission complete')
        logfile.close()

def shiyunDetail(pk,title,model):
	conn = openDB()
	cursor = conn.cursor()
        try:
		url = 'http://cord.tvxio.com/api/item/%s' % pk
		print 'parsing url : %s' % url
                #Log('shiyun url:%s' % url)
                response = urllib2.urlopen(url=url)
                data = simplejson.load(response)
        except urllib2.HTTPError, e:
                print e.code
                return None
        except Exception, e:
                print e
                return None
                
        #use simplejson to parse response json data
        title = data['title']
        items = data['attributes']
	if items == None:
		Log('title:%s None' % title)
		return None
        #r_directors = items['director']
	r_directors = items.get('director')
        #directors = []
	directors = ''
        if r_directors != None:
                for director in r_directors:
                        #directors.append(director[1])
			directors += director[1] + '/'
                        
        #actors = []
	actors = ''
        #r_actors = items['actor']
	r_actors = items.get('actor')
        if r_actors != None:
                for actor in r_actors:
                        #actors.append(actor[1])
			actors += actor[1] + '/'

	if len(directors) > 1:
		directors = directors[0:len(directors)-1]
	if len(actors) > 1:
		actors = actors[0:len(actors)-1]
        Log('pk:%s, model:%s, title:%s, ditector:%s, actor:%s' % (pk,model,title,directors,actors))
       	#movie = {'title':title,'directors':directors,'actors':actors}
        #return shiyun movie detail
        #return movie
	cursor.execute(INSERT,(pk,model,title,directors,actors))
	conn.commit()

if __name__ == '__main__':
	parse()

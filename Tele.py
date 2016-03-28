import requests
import bs4
import sys
import os

from reportlab.platypus import SimpleDocTemplate, Paragraph,Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_JUSTIFY
 
import io
#import threading

os.mkdir('TelegraphToday')
def scrap_link(url,f):
	#url='http://www.telegraphindia.com/1160328/jsp/frontpage/'+link
	print ""
	styles = getSampleStyleSheet()
	styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
	response=requests.get(url)
	html=response.text
	soup=bs4.BeautifulSoup(html,'lxml')
	#print soup.prettify()

	head=soup.select('#hd')[0]
	f.append(Paragraph('<font size=16>'+head.getText().encode('utf-8')+'</font>',styles['Italic'])) 
	f.append(Spacer(1,20))

	#print head.getText()
	#f.write('                          '+head.getText().encode('utf-8')+'\n\n')
	print ""
	td=soup.select('.story')[0]
	for p in td.select('p'):
		#print p.getText()
		f.append(Paragraph('<font size=12>'+p.getText().encode('utf-8')+'</font>',styles['Normal']))
	#f.write('\n')	
	f.append(Spacer(1,20))



def scrap(url_cur,base_url,name)	:	


	#url='http://www.telegraphindia.com'+part

	buf = io.BytesIO()
 
	# Setup the document with paper size and margins
	doc = SimpleDocTemplate(
    buf,
    rightMargin=inch/2,
    leftMargin=inch/2,
    topMargin=inch/2,
    bottomMargin=inch/2,
    pagesize=letter,
	)
 
	# Styling paragraphs
	styles = getSampleStyleSheet()

	paragraphs=[]


	print ""
	response=requests.get(url_cur)
	html=response.text
	soup=bs4.BeautifulSoup(html,'lxml')
	#f=open('TelegraphToday/'+name+'.txt','a')
	#print soup.prettify()
	print 'downloading '+name+'...'
	td=soup.select('.story a')
	for p in td:
		href = p.get('href')	
		if not href.startswith('/'):
			print ""
			print 'fetching '+href+'...'
			print base_url+href
			scrap_link(base_url+href,paragraphs)
	#f.close()	
	doc.build(paragraphs)
	with open('TelegraphToday/'+name+'.pdf', 'w') as fd:
    		fd.write(buf.getvalue())	

def download():
	urls=['http://www.telegraphindia.com/1160328/jsp/frontpage/index.jsp',
		  'http://www.telegraphindia.com/1160328/jsp/nation/index.jsp',
		  'http://www.telegraphindia.com/1160328/jsp/calcutta/index.jsp',
		  'http://www.telegraphindia.com/1160328/jsp/bengal/index.jsp',
		  'http://www.telegraphindia.com/1160328/jsp/foreign/index.jsp',
		  'http://www.telegraphindia.com/1160328/jsp/business/index.jsp',
		  'http://www.telegraphindia.com/1160328/jsp/sports/index.jsp'	]
	base_urls=['http://www.telegraphindia.com/1160328/jsp/frontpage/',
		  	   'http://www.telegraphindia.com/1160328/jsp/nation/',
		  	   'http://www.telegraphindia.com/1160328/jsp/calcutta/',
		       'http://www.telegraphindia.com/1160328/jsp/bengal/',
		       'http://www.telegraphindia.com/1160328/jsp/foreign/',
		       'http://www.telegraphindia.com/1160328/jsp/business/',
		       'http://www.telegraphindia.com/1160328/jsp/sports/']
	names=['front_page','nation','calcutta','bengal','foreign','business','sports']

	#scrap('http://www.telegraphindia.com/1160328/jsp/frontpage/index.jsp','http://www.telegraphindia.com/1160328/jsp/frontpage/','front_page')
	
	for i in range(0,len(urls)):
			scrap(urls[i],base_urls[i],names[i])
	print 'finished downloading pages'		
	print 'saved files to TelegraphToday'
			

download()			
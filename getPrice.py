from WindPy import w
import datetime
import sqlite3
import numpy

conn=sqlite3.connect("stockr.db3")
cur=conn.cursor()
#get data for one year
numdays=150
#clear the table and keep only data a year from now
cur.execute("delete from dp")

#start connection with Wind
w.start()

# if connected to Wind
if w.isconnected():
	#fetch data
	# personal version allows 600000-600120
	stockStartIndex=600000
	for j in range(0,100):
		stockIndex=stockStartIndex+j
		print ("j="+str(j))
		stock=str(stockIndex)+".sh"
		oneday=datetime.timedelta(days=1)
		totaldays=datetime.timedelta(days=numdays)
		dateEnd=datetime.date.today()
		dateStr=dateEnd-totaldays



		strdateStr=str(dateStr).replace("-","").split(" ")[0]
		strdateEnd=str(dateEnd).replace("-","").split(" ")[0]
		d=w.wsd(stock,"sec_englishname,open,high,low,close,volume",strdateStr,strdateEnd,"Priceadj=f;tradingcalendar=nib")
		print (d.Data)


		stockname=stock

		#data of each requested entry between the requested dates 
		#will be returned into its own array
		# in this case i asked for 6 kinds of entries
		arrSec_Name=d.Data[0]
		arrOpen=d.Data[1]
		arrHigh=d.Data[2]
		arrLow=d.Data[3]
		arrClose=d.Data[4]
		arrVolume=d.Data[5]
		
		#write enties to database
		#table "DailyPrice" scheme is:
		#id int, price_date datetime, open decimal,hight decinmal,low decimal,close decimal
		datei=dateStr 
		for i in range(0,len(arrOpen)):
			po=arrOpen[i]
			if po==None or numpy.isnan(po): po=0
			ph=arrHigh[i]
			if ph==None or numpy.isnan(ph): ph=0
			pl=arrLow[i]
			if pl==None or numpy.isnan(pl): pl=0
			pc=arrClose[i]
			if pc==None or numpy.isnan(pc): pc=0
			pv=arrVolume[i]
			if pv==None or numpy.isnan(pv): pv=0

			strO=str(po)
			strH=str(ph)
			strL=str(pl)
			strC=str(pc)
			strV=str(pv)
			message="insert into dp values(%s,\"%s\",%s,%s,%s,%s,%s)"%(stock.split(".")[0],str(datei),strO,strH,strL,strC,strV)
			#print ("meswsage="+message)
			cur.execute(message)
			datei=datei+oneday
		#for i
	#for j

#if connect

conn.commit()

#close conenction
w.stop()
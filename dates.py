import datetime

def getdates(numdays):
	oneday=datetime.timedelta(days=1)
	today=datetime.date.today()
	datei=today

	for i in range(0,numdays):
		print(str(datei).replace("-",""))
		datei=datei-oneday
	

getdates(100)

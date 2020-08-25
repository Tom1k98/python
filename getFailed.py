#!/usr/bin/env python3
import mysql.connector
from mymail import *
import argparse

usersList = []


def parseArgs():
	global args
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', '--num', default=10, type=int, help='pouzij, pokud chces jiny pocet zaznamu, nez 10 poslednich')
	parser.add_argument('-m', '--mail', type=str, default='tomas.storc@afd.cz', help='pouzij, pokud chces info poslat na jiny mail nez tomas.storc@afd.cz')
	args = parser.parse_args()

def connectDB():
	global rowsNum
	global failedRows
	dbobj = mysql.connector.connect(
        host='localhost', 
        user='root', 
        passwd='toor333koma',
        database='AFDsupport')
	mycursor = dbobj.cursor()
	mycursor.execute(f'select * from ost_syslog where title like \'%Excessive%\' order by log_id desc limit {args.num};')
	rowsNum = 0
	failedRows = 0
	for res in mycursor:
        #print(res[3])
		username = res[3].split(' ')[1:][6]
		attempts = res[3].split(' ')[1:][-1]
		if username not in "IP:":
			usersList.append(f'{username}, pocet pokusu: {attempts}')
			rowsNum = rowsNum + 1
		else:
			failedRows = failedRows + 1

def sendinfo(to):
	strList = str.join('\n', usersList)
	message = f'Poslednich {rowsNum+failedRows} prekrocenych pokusu o prihlaseni:\n...........\n{strList}\n.......\nu {failedRows} se nepovedlo zjistit prihlasovaci jmeno, ve vypisu jsou vynechana'
	subject = 'Pokusy o prihlaseni do ticket systemu'
	mysendmail(to, subject, message)

def testInfo():
	print(f'number of succesful rows: {rowsNum}\nnumber of failed rows: {failedRows}')

if __name__ == '__main__':
	parseArgs()
	connectDB()
	sendinfo(args.mail)
	#testInfo()

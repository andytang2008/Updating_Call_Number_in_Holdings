#######################################################
#  Update the holding call numbers in batch by using Ex Libris item API
#   Andy Tang 04/2023
#######################################################
import requests
import xml.etree.ElementTree as ET
from tkinter import *
#it will open a file open box
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

top = tk.Tk()
top.geometry("500x200")


global location
global itemPolicy
global apiKey
apiKey='Put your library cataloging records updating API key here'

def locateFile():
	#messagebox.showinfo( "Hello Python", "Hello World")
	top.file_path = filedialog.askopenfilename()
	print(top.file_path)

	top.destroy()

	

B = tk.Button(top, text ="Locate the MMS ID file!", command = locateFile)
E = tk.Button(top, text="Quit", command=top.destroy)  #.pack() is commented at the end of this line.
B.place(x = 35,y = 60)
E.place(x = 260,y = 60)

top.mainloop()

mms_ID_File=top.file_path

print(mms_ID_File);


global callNumberLostList
callNumberLostList=[]


def api_updateHolding(mms_id,holdingId,xmlstr):
	headers = {
		'accept': 'application/xml',
		'Content-Type': 'application/xml',
	}
	
	data = xmlstr
	mms_ID=mms_id
	response = requests.put('https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs/'+mms_ID+'/holdings/'+holdingId+'?apikey='+apiKey, headers=headers,data=data)
	print("*******************update holding**********************")
	print(response.content)

def api_getHolding(mms_id,holdingId,classNumber, cutterNumber):  #get the exact holding record.
	headers = {
		'accept': 'application/xml',
		'Content-Type': 'application/xml',
	}
	mms_ID=mms_id
	response = requests.get('https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs/'+mms_ID+'/holdings/'+holdingId+'?apikey='+apiKey, headers=headers)
	print('###################################')
	print(response.content)
	print('###################################')
	print ("class Number:"+classNumber)
	print ("cutter Number:" + cutterNumber)
	
	xmlResponse=response.content

	#root = ET.fromstring(xmlResponse)
	tree = ET.ElementTree(ET.fromstring(xmlResponse))
	root = tree.getroot()
	classN=root.find(".//*[@code='h']").text
	print ('classN: '+classN)
	cutterN=root.find(".//*[@code='i']").text
	print ('cutterN : '+cutterN)
	
	#root.find(".//*[@code='h']").text='xxxxx'
	#root.find(".//*[@code='i']").text='yyyyy'
	root.find(".//*[@code='h']").text=classNumber
	root.find(".//*[@code='i']").text=cutterNumber
	print ('classN: '+classN)
	xmlstr = ET.tostring(root, method='xml')
	xmlstr_decoded=xmlstr
	print (xmlstr_decoded)
	tree.write('output.xml')
	api_updateHolding(mms_ID,holdingId,xmlstr_decoded)
	

		
def api_getHoldings(mmsID, classNumber, cutterNumber):  #get holding lists
	headers = {
		'accept': 'application/xml',
		'Content-Type': 'application/xml',
	}
	
	mms_ID=mmsID
	response = requests.get('https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs/'+mms_ID+'/holdings?apikey='+apiKey, headers=headers)
	print("^^^^^^^^^^^^^^^^^^^^^^^")
	print(response.content)
	
	myroot = ET.fromstring(response.text)
	#print(myroot)
	print(myroot.tag)
	i=0
	for x in myroot.findall('holding'):  #if there is no holding at all, all code in for cycle will not run.
		i=i+1
		holdingId = x.find("holding_id").text
		print(i)
		print('xxxxholdingId:   '+holdingId)
		api_getHolding(mms_ID,holdingId,classNumber, cutterNumber)
		
	return '',''

f = open(mms_ID_File, "r")
lines = f.read().splitlines() # lines is an array, each element in array contains the format like 991008836536904082|31166002949495
#barcode='31166002949495'


for x in lines:
	if len(x)>1:  # avoid the empty element such as CR in lines.
		mmsID,classNumber,cutterNumber = x.split('|') # x is the each element in lines array
		print ("mmsID:"+mmsID)
		print ("class Number:"+classNumber)
		print ("cutter Number:" + cutterNumber)

		holdingId=api_getHoldings(mmsID, classNumber, cutterNumber)


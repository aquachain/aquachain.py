#!/usr/bin/env python3.6
from aquachain.aquatool import AquaTool
from datetime import datetime
aqua = AquaTool(ipcpath='~/.aquachain/aquachain.ipc')

head = aqua.gethead_header()


parent = head
#d = 0
while head['parentHash'] != "0x0000000000000000000000000000000000000000000000000000000000000000":
#	d = d + 1
#	if d % 1000 == 0:
#		print("\nchecking", int(head['number'], 16))
#		print("")
#		d = 0
	
	for tx in head['transactions']:
		receipt = aqua.gettransactionreceipt(tx)
		if receipt['contractAddress'] != None:
			print("\nblock number", int(head['number'], 16))
			print("tx time", datetime.utcfromtimestamp(int(head['timestamp'], 16)))
			print("tx hash", tx) 
			#print("tx receipt", receipt)
			print("gas used", int(receipt['gasUsed'], 16))
			print("contract address", receipt['contractAddress'])
			print("creator", receipt['from'])
	head = aqua.getheaderbyhash(head['parentHash'])


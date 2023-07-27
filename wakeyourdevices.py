#!/usr/bin/env python

import subprocess
import re
import scapy.all as scapy

list_of_mac = []

class Mass_Wake_On_Lan:
	def Run(self, list_of_mac):
		try:
			for mac in list_of_mac:
				command = "wakeonlan " + mac
				subprocess.call(command, shell=True)
		except ValueError:
			pass
	def Search(self, ip):
		mac_list = self.Scan(ip)
		if len(mac_list) == 0:
			print("[*] Cannot find out the mac of this device")
		else:
			for mac in mac_list:
				print(mac['mac'] + "\t" + mac['ip'])
			add = input("wol[Add this mac's in list? y/n]> ")
			if add == "y":
				global list_of_mac
				for mac in mac_list:
					if mac['mac'] not in list_of_mac:
						list_of_mac.append(mac['mac'])
						print("[+] The MAC has been added")
					else:
						print("[*] " + mac['mac']  + " is already on the list") 

	def Create(self):
		global list_of_mac
		print("[!!!][back] If enough") 
		while True:
			mac = input("wol[Write a MAC]> ")
			if mac == "back":
				break
			elif mac in list_of_mac:
				print("[*] This MAC exists in the list")
			else:
				if len(mac) == 17:
					list_of_mac.append(mac)
					print("[+] " + mac + " has been added in list")
				else:
					print("[*] Wrong MAC")
	def Help(self):
		print("[1] Start Attack\n[2] Create a list of MAC\n[3] Search the MAC\n[q] Exit\n[h] Help\n[s] Show the list\n[c] Clear this list\n[d] Remove the mac from list")

	def Show_list(self, list_of_mac):
		print("\n")
		count = 1
		for mac in list_of_mac:
			print("[" + str(count) + "] " + str(mac) + "\n")
			count += 1

	def Remove_mac_from_list(self, number_of_mac_in_list, list_of_mac):
		list_of_mac.remove(list_of_mac[int(number_of_mac_in_list) - 1])
		print("[+] The mac has been deleted from the list")


	def Scan(self, ip):
		arp_request = scapy.ARP(pdst=ip)
		broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
		arp_request_broadcast = broadcast/arp_request
		answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0] #srp - send and receive packets
									       #[0] - the first element in list
		clients_list = []
		for element in answered_list:
			client_dict = {"ip": element[0].pdst, "mac": element[1].hwsrc}
			clients_list.append(client_dict)
		return clients_list
	def Banner(self):
		print('''
░██╗░░░░░░░██╗░█████╗░██╗░░██╗███████╗██╗░░░██╗░█████╗░██╗░░░██╗██████╗░██████╗░███████╗██╗░░░██╗██╗░█████╗░███████╗░██████╗
░██║░░██╗░░██║██╔══██╗██║░██╔╝██╔════╝╚██╗░██╔╝██╔══██╗██║░░░██║██╔══██╗██╔══██╗██╔════╝██║░░░██║██║██╔══██╗██╔════╝██╔════╝
░╚██╗████╗██╔╝███████║█████═╝░█████╗░░░╚████╔╝░██║░░██║██║░░░██║██████╔╝██║░░██║█████╗░░╚██╗░██╔╝██║██║░░╚═╝█████╗░░╚█████╗░
░░████╔═████║░██╔══██║██╔═██╗░██╔══╝░░░░╚██╔╝░░██║░░██║██║░░░██║██╔══██╗██║░░██║██╔══╝░░░╚████╔╝░██║██║░░██╗██╔══╝░░░╚═══██╗
░░╚██╔╝░╚██╔╝░██║░░██║██║░╚██╗███████╗░░░██║░░░╚█████╔╝╚██████╔╝██║░░██║██████╔╝███████╗░░╚██╔╝░░██║╚█████╔╝███████╗██████╔╝
░░░╚═╝░░░╚═╝░░╚═╝░░╚═╝╚═╝░░╚═╝╚══════╝░░░╚═╝░░░░╚════╝░░╚═════╝░╚═╝░░╚═╝╚═════╝░╚══════╝░░░╚═╝░░░╚═╝░╚════╝░╚══════╝╚═════╝░
\n\t\t\t\t\t\tMade by Legion from DEDSEC''')

wol = Mass_Wake_On_Lan()
wol.Banner()
wol.Help()

while True:
	choice = input("wol> ")
	if choice == str(1):
		wol.Run(list_of_mac)
	elif choice == str(2):
		wol.Create()
	elif choice == str(3):
		try:
			ip = input("wol[Write ip/ip range]> " )
			wol.Search(ip)
		except Exception:
			print("[*] This IP doesn't exist")
	elif choice == "q":
		break
	elif choice == "h":
		wol.Banner()
		wol.Help()
	elif choice == "s":
		wol.Show_list(list_of_mac)
	elif choice == "c":
		list_of_mac = []
		print("[+] The list has been cleared")
	elif choice == "d":
		try:
			wol.Show_list(list_of_mac)
			print("\n\n")
			number = input("wol[Number of mac]> ")
			if int(number) > len(list_of_mac):
				print("[*] This number of mac doesn't exists")
			else:
				wol.Remove_mac_from_list(number, list_of_mac)
		except ValueError:
			print("[*] Wrong number")
	else:
		print("[*] Wrong choice")

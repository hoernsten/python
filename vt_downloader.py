#!/usr/bin/python

''' Tested for use with Python 3.5.3 on Windows 10 and Python 3.4.0 on Ubuntu 16.04.
Requires access to the VirusTotal Intelligence service.
Remember to add your personal API key to the 'key' variable. '''

import re
import sys
import signal
import urllib.request
from os.path import expanduser

# Handle Ctrl+C more gracefully
def ctrlc(sig, frame):
	print()
	sys.exit(0)
signal.signal(signal.SIGINT, ctrlc)

# Your personal API key
key = ''

# Validate the key variable
while not re.match("(?i)[a-z0-9]{64}", key):
	print('Error: The \'key\' variable is empty or incorrect.')
	input('Press enter to exit...')
	sys.exit()

def main():

	# Ask for the file hash
	hsh = input('File hash (MD5|SHA256): ')

	# Validate the hash input
	while not re.match("(?i)([a-z0-9]{64})|([a-z0-9]{32})", hsh):
		print('Error: Invalid hash.')
		return main()

	# Ask for the file name
	ext = input('File name incl. extension (optional): ')

	# If no file name is provided, the name will be equal to the hash
	if ext == "":
		ext = hsh

	# Define the download URL and destination (cross-platform)
	url = 'https://www.virustotal.com/intelligence/download/?hash=%s&apikey=%s' % (hsh, key)
	dst = expanduser("~") + '/Desktop/' + ext

	# Attempt to download the file
	try:
		print('Downloading file to ' + dst + '...')
		urllib.request.urlretrieve(url, dst)
		print('Success!')
	except urllib.error.HTTPError:
		print('Error: File not found.')
	except urllib.error.URLError:
		print('Error: Connection timeout.')

	return main()

main()

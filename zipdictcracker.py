import zipfile
import sys
import threading
from threading import Thread
import argparse

found = False

def extractFile(zFile, password, lock, passFile):
	with lock:
		try:
			print('Checking With Password: {}'.format(password.decode('utf-8')))
			zFile.extractall(pwd=password)
			print('===========================================')
			print('\n[+] Password Found = {}\n'.format(password.decode('utf-8')))
			print('===========================================')
			global found
			found = True
		except:
			pass
			
def main():
	parser = argparse.ArgumentParser('Dictionary Based Zip File Password Cracker')
	parser.add_argument('file', type=str, help='The Zip File Name. You can also provide the full path of the ZipFile')
	parser.add_argument('dictionary', type=str, help='The Dictionary File Name. You can also provide the full path of the Dictionary File')
	args = parser.parse_args()
	
	global found

	try:
		print('===========================================')
		print('\nLoding Files\n')
		print('===========================================')
		zFile = zipfile.ZipFile(args.file)
		passFile = open(args.dictionary, 'rb')
	except Exception as e:
		print(e)
		sys.exit(1)
	
	print('\nFiles Loaded\n')
	print('===========================================')
	print('\nCracking Password Using Dictionary Attack\n')
	print('===========================================\n')
	lock = threading.Lock()
	for line in passFile:
		password = line.strip()
		# print('{}\r'.format(password))
		if found != True:
			t = Thread(target=extractFile, args=(zFile, password, lock, passFile))
			t.start()
	
	while (threading.active_count() > 1):
		if threading.active_count() == 1 and found != True:
			print(found)
			print('===========================================')
			print('\nPassword Not Found In Dictionary\n')
			print('===========================================')
			sys.exit()
		elif threading.active_count() == 1 and found == True:
			passFile.close()
			print('\n===========================================\n')
			print('Exiting From Application\n')
			print('===========================================\n')
			
if __name__ == '__main__':
	main()

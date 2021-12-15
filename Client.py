import socket
import time
import re
import pickle
import os

s = socket.socket()
port = 5052
ip = '' 
s.connect((ip, port))
print('Connected')
username=input('Please Username : ')

def recv_file(message):

	suffix=message['suffix']

	size=int(message['size'])

	recived_f = 'file_'+str(time.time()).split('.')[0]+'.'+str(suffix)
	
	with open(recived_f, 'wb') as f:
		print('file opened')
		data = s.recv(size)
		f.write(data)
	f.close()

while True:
	
	message=s.recv(4096)
	message=pickle.loads(message)

	RF_TF= message['RF_TF']

	if RF_TF == True:
		recv_file(message)
	
	elif RF_TF == False:
		print(bytes(message['msg']).decode())
		
	type_message = input('For send file F and for send message M :')
	
	if type_message == 'F':
		file_name=input('Path File :')

		file_suffix = re.findall(r'(\w*$:?)',file_name)

		with open(file_name, 'rb') as f:
			file_size=os.path.getsize(file_name)
			l=f.read(file_size)
			info_file={'suffix':file_suffix[0],'size':file_size,'RF_TF':True}
			data=pickle.dumps(info_file)
			s.sendall(data)
			time.sleep(3)
			s.send(l)
		f.close()
			
	elif type_message == 'M':
		message=input('Message :')
		info_msg={'msg':str(username +  ' >>> ' + message).encode('utf-8'),'RF_TF':False}
		data=pickle.dumps(info_msg)
		s.send(data)


import socket
import time
import re
import pickle
import os

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(('',5052))
server.listen(1)

username=input('Please Enter Uername : ')

print('Waiting for client ....')
c, addr = server.accept()
print('Connected')

def recv_file(msg_recv):

	suffix=msg_recv['suffix']

	size=int(msg_recv['size'])

	recived_f = 'file_'+str(time.time()).split('.')[0]+'.'+str(suffix)
	
	with open(recived_f, 'wb') as f:
		print('file opened')
		data = c.recv(size)
		f.write(data)
	f.close()
	
while True:
	kind_message=input('For send file F and for send message M :')

	if kind_message == 'F':
		file_name=input('Path File :')

		file_suffix = re.findall(r'(\w*$:?)',file_name)

		with open(file_name, 'rb') as f:
			file_size=os.path.getsize(file_name)
			l=f.read(file_size)
			info_file={'suffix':file_suffix[0],'size':file_size,'RF_TF':True}
			data=pickle.dumps(info_file)
			c.sendall(data)
			time.sleep(3)
			c.send(l)
		f.close()
			
	elif kind_message == 'M':
		message=input('Message :')
		info_msg={'msg':str(username +  ' >>> ' + message).encode('utf-8'),'RF_TF':False}
		data=pickle.dumps(info_msg)
		c.send(data)

	msg_recv=c.recv(4096)
	msg_recv=pickle.loads(msg_recv)

	RF_TF= msg_recv['RF_TF']

	if RF_TF == True:
		recv_file(msg_recv)
	
	elif RF_TF == False:
		print(bytes(msg_recv['msg']).decode())

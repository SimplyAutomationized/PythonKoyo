import socket
def is_odd(num):
		return num & 0x1
class Koyo():
	def __init__(self,ip,debug=False):
		self.ip = ip
		self.debug=debug
		self.port = 28784
		self.address = (self.ip,self.port)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
		#self.sock.bind((self.ip,28784))
	def WriteC(self,variable,value):
		v=5
		if(value):
			v=4
		msg='484150512adf240b001a000700014'+str(v)+'01f'
		msg+=str(format(variable,'x')).zfill(3)
		if not value:
			value=180+variable
		elif(value and not is_odd(variable)):
			value=180+variable+1
		else:
			value=180+variable-1
		hexvalue=format(value,'x')
		if self.debug:
			print msg+'17'+hexvalue
		self.sock.sendto(bytearray.fromhex(msg),(self.ip,self.port))
		data0 = self.sock.recvfrom(1024)
		data1 = self.sock.recvfrom(1024)
	def ReadC(self,variable):              #484150fd9ffb3408001900011e06814131
		self.sock.sendto(bytearray.fromhex('484150fd9ffb3408001900011e06814131'),(self.ip,self.port))
		reply1 = self.sock.recvfrom(1024)
		reply2 = self.sock.recvfrom(1024)
		data = reply2[0]
		value =  ('{0:b}'.format(bytearray(data)[13]).zfill(8)[::-1])+\
		('{0:b}'.format(bytearray(data)[14]).zfill(8)[::-1])+\
		('{0:b}'.format(bytearray(data)[15]).zfill(8)[::-1])+\
		('{0:b}'.format(bytearray(data)[16]).zfill(8)[::-1])
		if self.debug:
			print value
		return value[variable]=='1'
	def ChangeIP(self,mac,newIP):
		msg='4841506b04fa510f0015'+mac+'0c001000'+\
		'{:02X}{:02X}{:02X}{:02X}'.format(*map(int, newIP.split('.')))
		self.ip=newIP
		#print msg
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		self.sock.sendto(bytearray.fromhex(msg),('<broadcast>',self.port))
		self.sock.recvfrom(1024),self.sock.recvfrom(1024)
	def FindKoyo(self):
		msg='484150f805a550010005'
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		self.sock.settimeout(3)
		self.sock.sendto(bytearray.fromhex(msg),('<broadcast>',self.port))
		recv=''
		while True:
			try:
				newmesg=self.sock.recvfrom(1024)	
			except socket.timeout: 
				break
			ips=map(ord,str(newmesg[0]))
			ip=str(ips[len(ips)-5])+'.'+str(ips[len(ips)-4])+'.'+str(ips[len(ips)-3])+'.'+str(ips[len(ips)-2])
			mac = str(hex(ips[len(ips)-13])[2:].zfill(2))+\
				str(hex(ips[len(ips)-12])[2:].zfill(2))+\
				str(hex(ips[len(ips)-11])[2:].zfill(2))+\
				str(hex(ips[len(ips)-10])[2:].zfill(2))+\
				str(hex(ips[len(ips)-9])[2:].zfill(2))+\
				str(hex(ips[len(ips)-8])[2:].zfill(2))
			print ip,mac
			newmesg=recv
		print 'done'
	
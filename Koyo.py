import socket,time
import binascii

def is_odd(num):
		return num & 0x1
def int_to_bcd(x):
    if x < 0:
        raise ValueError("Cannot be a negative integer")

    bcdstring = ''
    while x > 0:
        nibble = x % 16
        bcdstring = str(nibble) + bcdstring
        x >>= 4
    return int(bcdstring)

class Koyo():
	def __init__(self,ip,debug=False):
		self.ip = ip
		self.debug=debug
		self.port = 28784
		self.address = (self.ip,self.port)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
		self.sock.settimeout(3)
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
		try:
			self.sock.sendto(bytearray.fromhex(msg),(self.ip,self.port))
			data0 = self.sock.recvfrom(1024)
			data1 = self.sock.recvfrom(1024)
		except socket.timeout:
			time.sleep(1)
			pass
	def WriteOutput(self,variable,value):
		v=5
		if(value):
			v=4
		msg='484150512adf240b001a000700014'+str(v)+'01e8'
		msg+=str(format(variable,'x')).zfill(2)
		if not value:
			value=172+variable
		elif(value and not is_odd(variable)):
			value=172+variable+1
		else:
			value=172+variable-1
		hexvalue=format(value,'x')
		if self.debug:
			print msg+'17'+hexvalue
		try:
			self.sock.sendto(bytearray.fromhex(msg),(self.ip,self.port))
			data0 = self.sock.recvfrom(1024)
			data1 = self.sock.recvfrom(1024)
		except socket.timeout:
			time.sleep(1)
			pass
	def ReadOutputs(self):
		msg='484150fa03953508001900011e02414131'
		try:
			self.sock.sendto(bytearray.fromhex(msg),(self.ip,self.port))
			reply1 = self.sock.recvfrom(1024)
			data = self.sock.recvfrom(1024)[0]
			value = ('{0:b}'.format(bytearray(data)[13]).zfill(8)[::-1])+\
			('{0:b}'.format(bytearray(data)[14]).zfill(8)[::-1])
		except socket.timeout:
			print 'Socket TimeOut'
			return -1
		if self.debug:
			print bytearray(data)
			print value
		return value
	def ReadOutput(self,variable):
		outputs=self.ReadOutputs()
		return outputs[variable]=='1'
	def ReadC(self,variable):              #484150fd9ffb3408001900011e06814131
		value = self.ReadC_All()
		return value[variable]=='1'
	def ReadC_All(self):
		try:
			self.sock.sendto(bytearray.fromhex('484150fd9ffb3408001900011e06814131'),(self.ip,self.port))
			reply1 = self.sock.recvfrom(1024)
			reply2 = self.sock.recvfrom(1024)
			data = reply2[0]
			value =  ('{0:b}'.format(bytearray(data)[13]).zfill(8)[::-1])+\
			('{0:b}'.format(bytearray(data)[14]).zfill(8)[::-1])+\
			('{0:b}'.format(bytearray(data)[15]).zfill(8)[::-1])+\
			('{0:b}'.format(bytearray(data)[16]).zfill(8)[::-1])
			return value
		except socket.timeout:
			print "socket timeout"
			pass
			return -1
	def ReadInput(self,input):
		msg='4841502900382808001900011e02014131'
		if(input>16):
			msg='4841505e01687108001900011e02024131'
			input=0
		try:
			self.sock.sendto(bytearray.fromhex(msg),(self.ip,self.port))
			reply1 = self.sock.recvfrom(1024)
			data = self.sock.recvfrom(1024)[0]
		except socket.timeout:
			print 'Socket TimeOut'
			return -1
		if self.debug:
			print bytearray(data)
		value =  ('{0:b}'.format(bytearray(data)[13]).zfill(8)[::-1])+\
		('{0:b}'.format(bytearray(data)[14]).zfill(8)[::-1])
		return value[input]=='1'
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
	def ReadV(self,v): #read v memory words into an int 0-65535
		v=33620017+int(str(variable),8)
		meh = hex(v).replace('0x','')
		if(len(meh) & 0x1):
			meh=meh.zfill(len(meh)+1)
		msg='484150a80a64bf08001900011e'+meh
		try:
			self.sock.sendto(bytearray.fromhex(msg),(self.ip,self.port))
			self.sock.recvfrom(1024)
			data = self.sock.recvfrom(1024)[0]
			if(self.debug):
				print binascii.hexlify(data)
			value= hex(bytearray(data)[14]).replace('0x','').zfill(2)+hex(bytearray(data)[13]).replace('0x','').zfill(2)
			if(int(value,16)!=0 and self.debug):
				print int(str(variable),8),variable,value,int(value,16)
			return int(value,16)
		except socket.timeout:
			print 'timeout err'
			return -1
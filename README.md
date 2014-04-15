PythonKoyo
==========

Ongoing class to communicate with the Koyo ecom protocol.

Read and write to the C memory  C0-C16 in the Koyo H0-ECOM or H0-ECOM100.


Sample Code:

import Koyo.Koyo
plc = Koyo.Koyo('192.168.0.22')
plc.FindKoyo() #find koyo plc on your network
plc.ChangeIP(mac_address,newip)
plc.WriteC( C,bool) #C memory you want to write, true or false
plc.ReadC(C)



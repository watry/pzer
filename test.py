
from controller import *

import time

p = {
	'capture':{
		'uuid': "FA3877BD-7D9C-47D4-88D3-E98D3AC488A2",
		'output':['crt']
		}
}


c = Device(p)

c.protocolstack.add("e1", None, "ethernet", 	)
c.protocolstack.add("ip1",0x0800,"ip", 		[ "e1"])
c.protocolstack.add("b1", None,"bare", 		[ "e1", "ip1"])
c.protocolstack.add("b2", None,"bare", 		[ "e1"])

c.start()
time.sleep(3)
c.terminate()

print(c.parameter)
#print(c.get('uuid'))
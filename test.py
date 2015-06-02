
from controller import *

import time

p = {
	'capture':{
		'uuid': "FA3877BD-7D9C-47D4-88D3-E98D3AC488A2",
		'output':['crt']
		}
}


c = Device(p)

c.protocolstack.add("p1", None, "phy", 	)
c.protocolstack.add("e1", None, "ethernet", 	[ "p1"])
ptpport = c.protocolstack.add("ptp_port",0x88f7,"ptp_port", 		[ "p1", "e1"])
#c.protocolstack.add("ip1",0x0800,"ip", 		[ "p1", "e1"])
#c.protocolstack.add("b1", None,"bare", 		[ "p1", "e1", "ip1"])
#c.protocolstack.add("b2", None,"bare", 		[ "p1", "e1"])

ptpclock = c.protocolstack.add("ptp1", 1, "ptp",    )

ptpclock.register(ptpport)

c.start()
time.sleep(3)
c.terminate()

print(c.parameter)
#print(c.get('uuid'))
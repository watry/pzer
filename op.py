
from controller import *

import time

p = {
	'capture':{
		'uuid': "FA3877BD-7D9C-47D4-88D3-E98D3AC488A2",
		'output':['crt']
		}
}


c = Device(p)
c.addProtocol(
	base = [],
	name = 'eth1',
	typ = 'eth',
	cfg = {}
	)
c.addProtocol(
	base = ['eth1'],
	name = 'bare1',
	typ = 'bare',
	cfg = {}
	)
c.start()
time.sleep(3)
c.terminate()

print(c.parameter)
#print(c.get('uuid'))
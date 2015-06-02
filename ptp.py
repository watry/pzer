


class PtpPort(object):
    def __init__(self):
        super(PtpPort, self).__init__()
        self.clock = None

    def register(self, ptpclock):
        self.clock = ptpclock

    def receive(self, time, content):
        s = "%s -- %s" % (str(time), str(content))
        self.clock.show(s)


class Ptp(object):
    def __init__(self):
        super(Ptp, self).__init__()
        self.ports = []

    def register(self, ptpport):
        self.ports.append(ptpport)
        ptpport.register(self)

    def show(self, s):
        #print("%s--" % s)
        self.ports[0].send(s)
        

"""P42

import queue


class PtpPort(object):
    def __init__(self):
        pass

class PtpLocalPort(PtpPort):
    pass


class PtpClock(object):
    def __init__(self):

    def decode(self, content):
        return 1

    def onMessage(self, port, content):
        ss = find_session(port, content)
        if ss:
            ss.recv(content)
        elif is_announce:
            createSession( this_pkt )

    def recv(self, content):
        pass

    def send(self, type):
        pass


clock_data
defaultDS
currentDS
parentDS
timePropertiesDS

port_data

protocol_engine
    send
    recv
    maintain_data
    statemachine
    calc_time_by_slave

event interface
general interface

The set of event messages consists of: 
a)  Sync (see 13.6) 
b)  Delay_Req (see 13.6) 
c)  Pdelay_Req (see 13.9) 
d)  Pdelay_Resp (see 13.10) 

The set of general messages consists of: 
⎯  Announce (see 13.5) 
⎯  Follow_Up (see 13.7) 
⎯  Delay_Resp (see 13.8) 
⎯  Pdelay_Resp_Follow_Up (see 13.11) 
⎯  Management (see Clause 15) 
⎯  Signaling (see 13.12) 



All PTP-related communications occur via PTP messages. PTP messages have the following attributes:  
⎯  Message class 
⎯  Message sourcePortIdentity 
⎯  Message type 
⎯  Message sequenceId 
⎯  Flags defining options 


"""

'''
def Recv(content, timestamp=[]):
    # check valid
    remote_port = find_remote(content)
    if remote_port==None
        if typ==Announce:
            create_rmt_port(Announce)
    elif: remote_port.accept(content):
        if announce:
            update_self #--> parent clock
        elif sync:
            record('sync', port, sndtime, rcvtime)
'''

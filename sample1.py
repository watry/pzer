




import threading
from winpcapy import *

class cap():
    def __init__(self, parameter):
        self.para = {
            'port':b'',
            'filter':b'',
            'logsize':-1,
            'output':{},
            }
        self.adhandle = None
        self.act = threading.Event()
        self.read_p = threading.Event()
        self.read_p.set()
        self.running = True
        self.config(parameter)
        threading.Thread(target=self.run).start()

    def getpara(self, para):
        t = self.para
        self.read_p.wait()
        self.read_p.clear()
        try:
            for x in para:
                t = t[x]
            self.read_p.set()
            return t
        except:
            self.read_p.set()
            return None
 
    def setpara(self, para, value):
        t = self.para
        self.read_p.wait()
        self.read_p.clear()
        try:
            for x in para[:-1]:
                t = t[x]
            t[para[-1]] = value
            self.read_p.set()
            return True
        except:
            self.read_p.set()
            return False
        
    def config(self, parameter):
        errbuf = create_string_buffer(PCAP_ERRBUF_SIZE)

        try:
            self.setpara(['port'], parameter['port'])
            self.adhandle = pcap_open_live(
                self.getpara(['port']),  # device name
                65536,  # buffer_Byte
                1,      # pronomous mode
                1,      # timeout in ms
                errbuf,
                )
        except:
            pass
        
        try:
            self.setpara(['filter'], parameter['filter'])
            fcode = bpf_program()
            pcap_compile(
                self.adhandle,
                byref(fcode),
                self.getpara(['filter']),
                1,      # pcap_compile
                0       # ip netmask
                )
        except:
            pass
        
        try:
            for x in parameter['output']:
                try:
                    assert(parameter['output'][x] == self.getpara(['output',x]))
                except:
                    self.setpara(['output',x], parameter['output'][x])
        except:
            pass
    
    def run(self):
        header_data = POINTER(pcap_pkthdr)()
        packet_data = POINTER(c_ubyte)()

        while self.running:
            self.act.wait()
            res = pcap_next_ex(
                self.adhandle,
                byref(header_data),
                byref(packet_data),
                )
            if res==1:
                self.output(header_data,packet_data)
        pcap_close(self.adhandle)
        
    def start(self):
        self.act.set()

    def pause(self):
        self.act.clear()
        
    def stop(self):
        self.running = False

    def output(self, header_data, packet_data):
        content = []
        for x in packet_data[:header_data.contents.len]:
            content.append(x)

        pktdata = {
            'port':self.getpara(['port']),
            'time':[header_data.contents.ts.tv_sec, header_data.contents.ts.tv_usec],
            'content':content
            }
        if "crt" in self.getpara(['output']):
            for x in self.getpara(['output',"crt"]):
                x.display(pktdata)
        if "controller" in self.getpara(['output']):
            for x in self.getpara(['output',"controller"]):
                x.receive(pktdata)

import queue

class crt(threading.Thread):
    def __init__(self):
        super(crt, self).__init__()
        self.queue = queue.Queue()
        self.running = True

    def run(self):
        while self.running:
            s = self.queue.get()
            print(s)
            self.queue.task_done()

    def display(self, pktdata):
        exp = "%d:%06d   %s" % (pktdata['time'][0],\
                                pktdata['time'][1],\
                                str(pktdata['content'][:16]))
        self.queue.put(exp)

#--------------

class controller_ingress(threading.Thread):
    def __init__(self, queue, parent, isRunning):
        super(controller_ingress, self).__init__()
        self.queue = queue
        self.parent = parent
        self.isRunning = isRunning

    def run(self):
        while True:
            self.isRunning.wait()
            pkt_data = self.queue.get()
            self.parent.react(str(pkt_data['time']))
            self.queue.task_done()
            


class controller(threading.Thread):
    def __init__(self):
        super(controller, self).__init__()
        self.rx_queue = queue.Queue()
        self.rx_isRunning = threading.Event()
        self.ingress = controller_ingress(self.rx_queue, self, self.rx_isRunning)
        self.ingress.start()

    
    def run(self):
        self.rx_isRunning.set()

    def receive(self, pktdata):
        self.rx_queue.put(pktdata)

    def output(self, value):
        print(value)

    def react(self, sig):
        self.output(sig)
        
#--------------
c = crt()
c.start()

d=controller()
d.start()

cap_parameter = {
    'port':b'\\Device\\NPF_{FA3877BD-7D9C-47D4-88D3-E98D3AC488A2}',
    'filter':b'tcp',
    'logsize':-1,
    'output':{
        #"crt":[c],
        #"file":"z:\\test.txt"
        "controller":[d],
        },
}
new_capture = cap(cap_parameter)
new_capture.start()




#new_capture.pause()
#new_capture.stop()





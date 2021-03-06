from winpcapy import *
from ctypes import *

import threading
import queue

import protocols

name = "aaa"


class DataModel(object):
    def __init__(self, para={}):
        self.parameter = para

    def get(self, index):
        return self.parameter[index]

    def has(self, index):
        return index in self.parameter

    def set(self, index, value, allowCreate=False):
        if allowCreate or self.has(index):
            self.parameter[index] = value
            return True
        else:
            assert()
            return False

    def mset(self, dic, allowCreate=False):
        for x in dic:
            self.set(x, dic[x], allowCreate)


class Capture(DataModel):
    def __init__(self, parameters, Buffer):
        super(Capture, self).__init__()
        init_parameters = {
            "uuid":"",
            "filter":"",
            "output":[]
            }
        self.mset(init_parameters,allowCreate=True)
        self.mset(parameters,allowCreate=False)

        self.RecvBuffer = Buffer

        self._processer_alive      = threading.Event()
        self.running    = threading.Event()

        self.CapThread = threading.Thread(target=self.cap)


    def start(self):
        self.running.set()
        self._processer_alive.set()
        self.CapThread.start()
        #self.DistThread.start()

    def terminate(self):
        self._processer_alive.clear()
        self.running.set()  # break wait_loop
        self.CapThread.join()
        #self.DistThread.join()

        self.CapThread = threading.Thread(target=self.cap)
        #self.DistThread = threading.Thread(target=self.dist)

    def pause(self):
        self.running.clear()

    def continu(self):
        self.running.set()

    def cap(self):
        errbuf = create_string_buffer(PCAP_ERRBUF_SIZE)
        header_data = POINTER(pcap_pkthdr)()
        packet_data = POINTER(c_ubyte)()

        adhandle = pcap_open_live(
                ('\\Device\\NPF_{%s}' % self.get('uuid')).encode('utf8'),
                                                          # device name
                65536,  # buffer_Byte
                1,      # pronomous mode
                1,      # timeout in ms
                errbuf,
                )

        fcode = bpf_program()
        pcap_compile(
            adhandle,
            byref(fcode),
            self.get('filter').encode('utf8'),
            1,      # pcap_compile
            0       # ip netmask
            )
        pcap_freecode(fcode)

        while self._processer_alive.isSet():
            self.running.wait()
            if(pcap_next_ex(
                adhandle,
                byref(header_data),
                byref(packet_data),
                )==1 
                and header_data!=None):

                content = []
                for x in packet_data[:header_data.contents.len]:
                    content.append(x)

                pktdata = {
                    'port':self,
                    'time':[header_data.contents.ts.tv_sec, header_data.contents.ts.tv_usec],
                    'content':content,
                    'offset':0,
                    }

                self.RecvBuffer.put_nowait(pktdata)
                #except QueueFull:
                #    pass

        pcap_close(adhandle)


class Device(DataModel):
    def __init__(self,para):
        init_parameters = {
            "capture":{},
            "output":['crt']
            }
        super(Device, self).__init__(init_parameters)
        self.mset(para,allowCreate=False)
        

        self.RecvBuffer = queue.Queue()
        self.cap  = Capture(para['capture'], self.RecvBuffer)

        self._processer_alive      = threading.Event()
        self.procThread = threading.Thread(target=self._processer)

        self.protocolstack = protocols.Phy()



    def _processer(self):
        while self._processer_alive.isSet():
            if not self.RecvBuffer.empty():
                t = self.RecvBuffer.get(False)  
                self.protocolstack.archive(t)


    def start(self):
        self._processer_alive.set()
        self.procThread.start()
        self.cap.start()

    def terminate(self):
        self._processer_alive.clear()
        self.cap.terminate()
        self.procThread = threading.Thread(target=self._processer)





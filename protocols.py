


class Protocol(object):
    def __init__(self):
        self.__init__protocol__()
    def __init__protocol__(self):
        self.roster = {}
        self.facility = {
            'phy': Phy,
            'ptp': Ptp,
            }
        self.key={}
        self.rkey={}
        self.offset = 0
        self.parent = None

    def add(self, name, key_exp, protocol_type, routine=[]):
        loc = self
        for x in routine:
            key = loc.key[x]
            loc = loc._getSubProtocol(key)
        loc._assignKey(name, key_exp)
        return loc._addSubProtocol(name, protocol_type)


    def onRecv(self, pkt):
        return 

    def archive(self, pkt):
        key = self.getKey(pkt)

        self.onRecv(pkt)

        # shift offset for sub protocols
        pkt['offset'] = pkt['offset'] + self.offset

        # if no protocol added, do nothing
        sub_protocol = self._getSubProtocol(key)
        if sub_protocol:
            sub_protocol.archive(pkt)


    def _assignKey(self, name, key):
        assert(name not in self.key)
        assert(key not in self.rkey)
        self.key[name] = key
        self.rkey[key] = name

    def _addSubProtocol(self, name, protocol_type):
        key = self.key[name]
        try:
            self.roster[key] = self.facility[protocol_type]()
            self.roster[key].parent = self
            return self.roster[key]
        except KeyError:
            print("%s has no %s" % (str(self), key))
            assert()
            return None

    def getKey(self, pkt):
        return None # Please clarify it, e.g. 0x0800 for IP in Eth, 04 for TCP in IP

    def _getSubProtocol(self, key):
        default_protocol = self.roster.get(None)
        return self.roster.get(key, default_protocol)

    def send(self, content):
        if self.parent == None:
            assert() #"inherient!"
        self.parent.send(self.encap(content))

    def encap(self, s):
        return s




class Bare(Protocol):
    def __init__(self):
        super(Bare, self).__init__()

    def onRecv(self, pkt):
        print(pkt['time'])

class Phy(Protocol):
    def __init__(self):
        super(Phy, self).__init__()
        self.facility = {
            'ethernet': Ethernet,
            }

    def send(self, content):
        print(content)



class Ethernet(Protocol):
    def __init__(self):
        super(Ethernet, self).__init__()
        self.facility = {
            'bare':     Bare,
            'ip':       Ip,
            'ptp_port': Ptp_port,
            }
        self.offset = 14

    def getKey(self, pkt):
        i_start = pkt['offset']+12
        i_length = 2
        result = 0
        for i in range(i_length):
            result *= 256
            result += pkt['content'][i_start+i]
        return result

    def encap(self, content):
        return "mac + " + content


class Ip(Protocol):
    def __init__(self):
        super(Ip, self).__init__()
        self.facility = {
            'bare':     Bare,
            }
        self.offset = 24


import ptp
class Ptp(ptp.Ptp, Protocol):
    def __init__(self):
        super(Ptp, self).__init__()
        self.__init__protocol__()

    def onRecv(self, pkt):
        assert()

class Ptp_port(ptp.PtpPort, Protocol):
    def __init__(self):
        super(Ptp_port, self).__init__()
        self.__init__protocol__()

    def onRecv(self, pkt):
        t = pkt["time"]
        i = pkt["offset"]
        self.receive(t, pkt["content"][i:])

    def encap(self, content):
        return "test_ptp"+content


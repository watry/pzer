


class Protocol(object):
    def __init__(self):
        self.roster = {}
        self.facility = {
            'phy': Phy,
            }
        self.key={}
        self.rkey={}
        self.offset = 0

    def add(self, name, key_exp, protocol_type, routine=[]):
        loc = self
        for x in routine:
            key = loc.key[x]
            loc = loc._getSubProtocol(key)
        loc._assignKey(name, key_exp)
        loc._addSubProtocol(name, protocol_type)


    def onRecv(self, pkt):
        return 

    def archive(self, pkt):
        pkt['offset'] = pkt['offset'] + self.offset

        self.onRecv(pkt)

        key = self.getKey(pkt)
        sub_protocol = self._getSubProtocol(key)
        if sub_protocol:
            sub_protocol.archive(pkt)

    def _assignKey(self, name, key):
        self.key[name] = key
        self.rkey[key] = name

    def _addSubProtocol(self, name, protocol_type):
        key = self.key[name]
        self.roster[key] = self.facility[protocol_type]()

    def getKey(self, pkt):
        return None # Please clarify it, e.g. 0x0800 for IP in Eth, 04 for TCP in IP

    def _getSubProtocol(self, key):
        default_protocol = self.roster.get(None)
        return self.roster.get(key, default_protocol)




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



class Ethernet(Protocol):
    def __init__(self):
        super(Ethernet, self).__init__()
        self.facility = {
            'bare':     Bare,
            'ip':       Ip,
            }
        self.offset = 14

    def getKey(self, pkt):
        i_start = pkt['offset']+12
        i_length = 2
        result = 0
        for i in range(i_length):
            result += pkt['content'][i_start+i]
            result *= 256
        return result

class Ip(Protocol):
    def __init__(self):
        super(Ip, self).__init__()
        self.facility = {
            'bare':     Bare,
            }
        self.offset = 24



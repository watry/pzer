
import copy

class Packet():
    def __init__(self):
        pass

class protocol(object):
    def __init__(self, cfg):
        pass
    def accept(self, tar):
    	return False
    def issue(self,tar):
        print(tar)
    def digest(self, tar):
        return []


class bare(protocol):
    def accept(self, tar):
        return True
    def issue(self, tar):
        print('----------')

class ethernet(protocol):
    def __init__(self,cfg):
        pass
    def accept(self, tar):
        return True
    def digest(self, tar):
        c = copy.deepcopy(tar)
        c['content'] = c['content'][14:]
        Id = c['content'][12]*256 + \
            c['content'][13]
        return [[c, Id],]

class mpls(protocol):
    def __init__(self):
        pass

class oam(protocol):
    def __init__(self):
        pass


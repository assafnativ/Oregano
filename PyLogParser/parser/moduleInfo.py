

class ModuleInfo(object):
    def __init__(self, name, addr, length, data):
        self.name = name
        self.addr = addr
        self.length = length
        self.data = data
        self.end = addr + length
    def isInRange(self, address):
        if self.addr <= address and self.end > address:
            return True
        return False
    def getData(self, address, length):
        offset = address - self.addr
        return self.data[offset:offset+length]

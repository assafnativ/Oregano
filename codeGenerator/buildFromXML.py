
from xml.etree.ElementTree import ElementTree, parse, Element, SubElement

class Opcode(object):
    def __init__(self, val, entry):
        self.val = val
        attrib = entry.attrib
        self.attrib = attrib
        self.op_size = int(attrib.get('op_size', 0))
        self.ring = attrib.get('ring', 3)
        if (self.ring == 'f'):
            self.ring = 0
        else:
            self.ring = int(self.ring)
        self.modrm = attrib.r == 'yes'
        self.lockable = attrib.lock == 'yes'
    def __repr__(self):
        return "0x%2x:op_size0x%x:Ring%d" % (self.val, self.op_size, self.ring)

class parser(object):
    MODE_FILTER = {
            'x64' : ['e', 'p', 'r'],
            'x86' : ['r', 'p'] }

    def __init__(self, xmlFile, mode='x64'):
        self.mode = mode
        self.mode_filter = parser.MODE_FILTER[self.mode]
        for root in parse(xmlFile).getroot():
            tag = root.tag
            if tag == 'one-byte':
                self.table = self.parseTable(root)
            elif tag == 'two-byte':
                self.table[0x0f] = self.parseTable(root)
            else:
                pass

    def _isDocAttrib(self, attrib):
        result = ""
        for key in attrib.keys():
            if key.startswith('doc'):
                result += '%s:%s' % (key, attrib.pop(key))
        return result

    def getMatchingEntry(self, pre_opcd):
        result = None
        for entry in pre_opcd:
            attrib = entry.attrib.copy()
            isDocAttrib = self._isDocAttrib(attrib)
            isRef = attrib.pop('ref', None)
            mode = attrib.pop('mode', None)
            attr = attrib.pop('attr', None)
            details = (\
                    attrib.pop('lock', None),
                    attrib.pop('direction', None),
                    attrib.pop('r', None),
                    int(attrib.pop('op_size', 0)),
                    attrib.pop('ring', None),
                    attrib.pop('is_undoc', None),
                    attrib.pop('is_doc', None),
                    attrib.pop('particular', None),
                    attrib.pop('doc', None),
                    attrib.pop('doc_ref', None),
                    int(attrib.pop('sign-ext', 0)),
                    attrib.pop('ring_ref', None),
                    attrib.pop('tttn', None),
                    attrib.pop('alias', None),
                    attrib.pop('mem_format', None),
                    attrib.pop('fpop', None),
                    attrib.pop('fpush', None),
                    attrib.pop('mod', None),
                    attrib.pop('part_alias', None),
                    attrib.pop('doc_part_alias_ref', None))
            if attr in ['invd', 'undef']:
                # Invalid opcode
                pass
            elif isRef:
                # A reference to another part
                print("Opcode ref %s" % isRef)
            elif isDocAttrib:
                # Document reference
                print("Doc ref: %s" % isDocAttrib)
            elif (None == result) and (not mode) or (mode in self.mode_filter):
                result = entry
            elif None != result and (mode in self.mode_filter):
                print("Entry %r overwrites %r" % (result, entry))
                result = entry
            elif not attrib:
                pass
            else:
                print("Default: %r" % (attrib))
                result = entry
            if len(attrib) != 0:
                raise Exception("Unused attributes %r" % (attrib))
        return result

    def parseTable(self, root):
        table = [0] * 0x100
        for pre_opcd in root:
            val = int(pre_opcd.attrib['value'], 16)
            entry = self.getMatchingEntry(pre_opcd)
            if None != entry:
                table[val] = Opcode(val, entry)
            else:
                print("Opcode 0x%2x has no effect" % val)
        return table


if __name__ == '__main__':
    p = parser('x86reference.xml')


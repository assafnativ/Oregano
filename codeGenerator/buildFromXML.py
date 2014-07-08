def makeArray(d, val=None):
    if len(d) > 1:
        return [makeArray(d[1:]) for i in range(d[0])]
    result = []
    for i in d[0]:
       result.append(copy.deepcopy(val))
    return result

class Effect(object):
    def __init__(self):
        self.src = []
        self.dst = []

class SideEffects(object):
    # Make it Singleton
    _instance = None
    def __new__(self, *args, **kw):
        if not cls._instance:
            self._table = makeArray([0x4, 0x100])
            self._table64 = makeArray([0x4, 0x10, 0x100])
            self._fullTable = None
            self._fullTable64 = None
            self._instance = super(OpcodesSideeffect, self).__new__(self, *args, **kw)
        return self._instance

    def getEffect(self, opcode):
        opcodeCopy = opcode
        if isinstance(opcode, str):
            opcode = [ord(x) for x in opcode]
        t = self._table
        while opcode != []:
            b = opcode[0]
            if None == t[b]:
                t[b] = makeArray([0x100])
            t = t[b]
            opcode = opcode[1:]
            if isinstance(t, Effect) and opcode == []:
                raise Exception("Invalid change of opcode into table %s" % repr(opcodeCopy))
        return t

    def appendEffect(self, opcode, src=[], dst=[]):
        effect = self.getEffect(opcode)
        setEffect(
        
from xml.etree.ElementTree import ElementTree

PREFIX_ADDRESS_SIZE = 0x67
PREFIX_OPERAND_SIZE = 0x66
PREFIX_ES   = 0x26
PREFIX_CS   = 0x2e
PREFIX_SS   = 0x36
PREFIX_DS   = 0x3e
PREFIX_FS   = 0x64
PREFIX_GS   = 0x65
PREFIX_LOCK     = 0xf0
PREFIX_REPNZ    = 0xf2
PREFIX_REPZ     = 0xf3

PREFIXES = [PREFIX_ADDRESS_SIZE, PREFIX_OPERAND_SIZE, PREFIX_ES, PREFIX_CS, PREFIX_SS, PREFIX_DS, PREFIX_FS, PREFIX_GS, PREFIX_LOCK, PREFIX_REPNZ, PREFIX_REPZ]
PREFIXES += range(0x41,0x48)
PREFIXES += range(0x49, 0x4F)
PREFIXES += [0x9b]

ACCESS_8BIT  = 1
ACCESS_16BIT = 2
ACCESS_32BIT = 4

SIB_REGISTERS_BY_INDEX = [
        'EAX',
        'ECX',
        'EDX',
        'EBX',
        'ESP',
        'EBP',
        'ESI',
        'EDI' ]

DISPLACEMENT_BY_MODBITS = [
        '',
        'DISPLACEMENT8',
        'DISPLACEMENT32',
        '' ]
DISPLACEMENT_BY_MODBITS_SIB = [
        'DISPLACEMENT32',
        'DISPLACEMENT8_EBP',
        'DISPLACEMENT32_EBP',
        ]

def SIBCode(accessType, sibByte, modBits, effect=''):
    result = effect
    base    = (sibByte & 0x07)
    index   = (sibByte & 0x38) >> 3
    scale   = (sibByte & 0xc0) >> 6
    scale = 2 ** scale
    if 0x4 == index and 0x5 == base:
        if 3 == modBits:
            return ''
        result += DISPLACEMENT_BY_MODBITS_SIB[modBits]
    elif 0x4 == index:
        result += '_'.join([DISPLACEMENT_BY_MODBITS[modBits], SIB_REGISTERS_BY_INDEX[base]])
    elif 0x5 == base:
        if 3 == modBits:
            return ''
        result += '_'.join([
                DISPLACEMENT_BY_MODBITS_SIB[modBits],
                SIB_REGISTERS_BY_INDEX[index],
                '%d' % scale,
                'SIB'])
    else:
        result += '_'.join([
                DISPLACEMENT_BY_MODBITS[modBits],
                SIB_REGISTERS_BY_INDEX[base],
                SIB_REGISTERS_BY_INDEX[index],
                '%d' % scale,
                'SIB'])
    result = result.replace('__', '_')
    if result[-1] == '_':
        result = result[:-1]
    return result

def ModRMOpcode32(accessType, value, effect=''):
    result = effect
    if ACCESS_32BIT == accessType:
        result += 'DWORDPTR_'
    elif ACCESS_8BIT == accessType:
        result += 'BYTEPTR_'
    elif ACCESS_16BIT == accessType:
        result += 'WORDPTR_'
    else:
        raise Exception('Unsupported ModRM')
    mod = (value & 0xc0) >> 6
    reg = (value & 0x38) >> 3
    rm  = (value & 0x07)
    if 0x0 == mod:
        if   0x0 == rm:
            result += 'EAX'
        elif 0x1 == rm:
            result += 'ECX'
        elif 0x2 == rm:
            result += 'EDX'
        elif 0x3 == rm:
            result += 'EBX'
        elif 0x4 == rm:
            effect = result
            result = []
            for i in xrange(0x100):
                result.append(SIBCode(accessType, i, mod, effect))
        elif 0x5 == rm:
            result += 'DISPLACEMENT32'
        elif 0x6 == rm:
            result += 'ESI'
        elif 0x7 == rm:
            result += 'EDI'
    if 0x1 == mod:
        if   0x0 == rm:
            result += '_'.join(['DISPLACEMENT8', 'EAX'])
        elif 0x1 == rm:
            result += '_'.join(['DISPLACEMENT8', 'ECX'])
        elif 0x2 == rm:
            result += '_'.join(['DISPLACEMENT8', 'EDX'])
        elif 0x3 == rm:
            result += '_'.join(['DISPLACEMENT8', 'EBX'])
        elif 0x4 == rm:
            effect = result
            result = []
            for i in xrange(0x100):
                result.append('_'.join([SIBCode(accessType, i, mod, effect)]))
        elif 0x5 == rm:
            result += '_'.join(['DISPLACEMENT8', 'EBP'])
        elif 0x6 == rm:
            result += '_'.join(['DISPLACEMENT8', 'ESI'])
        elif 0x7 == rm:
            result += '_'.join(['DISPLACEMENT8', 'EDI'])
    if 0x2 == mod:
        if   0x0 == rm:
            result += '_'.join(['DISPLACEMENT32', 'EAX'])
        elif 0x1 == rm:
            result += '_'.join(['DISPLACEMENT32', 'ECX'])
        elif 0x2 == rm:
            result += '_'.join(['DISPLACEMENT32', 'EDX'])
        elif 0x3 == rm:
            result += '_'.join(['DISPLACEMENT32', 'EBX'])
        elif 0x4 == rm:
            effect = result
            result = []
            for i in xrange(0x100):
                result.append('_'.join([SIBCode(accessType, i, mod, effect)]))
        elif 0x5 == rm:
            result += '_'.join(['DISPLACEMENT32', 'EBP'])
        elif 0x6 == rm:
            result += '_'.join(['DISPLACEMENT32', 'ESI'])
        elif 0x7 == rm:
            result += '_'.join(['DISPLACEMENT32', 'EDI'])
    if 0x3 == mod:
        # No memory access here
        result = effect
    return result

def ModRMOpcode16(accessType, value, effect=''):
    result = effect
    if ACCESS_32BIT == accessType:
        result += 'DWORDPTR_'
    elif ACCESS_8BIT == accessType:
        result += 'BYTEPTR_'
    elif ACCESS_16BIT == accessType:
        result += 'WORDPTR_'
    else:
        raise Exception('Unsupported ModRM')
    rm  = (value & 0x07)
    reg = (value & 0x38) >> 3
    mod = (value & 0xc0) >> 6
    if 0x0 == mod:
        if   0x0 == rm:
            result += 'BX_SI'
        elif 0x1 == rm:
            result += 'BX_DI'
        elif 0x2 == rm:
            result += 'BP_SI'
        elif 0x3 == rm:
            result += 'BP_DI'
        elif 0x4 == rm:
            result += 'SI'
        elif 0x5 == rm:
            result += 'DI'
        elif 0x6 == rm:
            result += 'DISPLACEMENT16'
        elif 0x7 == rm:
            result += 'BX'
    if 0x1 == mod:
        if   0x0 == rm:
            result += '_'.join(['DISPLACEMENT8', 'BX', 'SI'])
        elif 0x1 == rm:
            result += '_'.join(['DISPLACEMENT8', 'BX', 'DI'])
        elif 0x2 == rm:
            result += '_'.join(['DISPLACEMENT8', 'BP', 'SI'])
        elif 0x3 == rm:
            result += '_'.join(['DISPLACEMENT8', 'BP', 'DI'])
        elif 0x4 == rm:
            result += '_'.join(['DISPLACEMENT8', 'SI'])
        elif 0x5 == rm:
            result += '_'.join(['DISPLACEMENT8', 'DI'])
        elif 0x6 == rm:
            result += '_'.join(['DISPLACEMENT8', 'BP'])
        elif 0x7 == rm:
            result += '_'.join(['DISPLACEMENT8', 'BX'])
    if 0x2 == mod:
        if   0x0 == rm:
            result += '_'.join(['DISPLACEMENT16', 'BX', 'SI'])
        elif 0x1 == rm:
            result += '_'.join(['DISPLACEMENT16', 'BX', 'DI'])
        elif 0x2 == rm:
            result += '_'.join(['DISPLACEMENT16', 'BP', 'SI'])
        elif 0x3 == rm:
            result += '_'.join(['DISPLACEMENT16', 'BP', 'DI'])
        elif 0x4 == rm:
            result += '_'.join(['DISPLACEMENT16', 'SI'])
        elif 0x5 == rm:
            result += '_'.join(['DISPLACEMENT16', 'DI'])
        elif 0x6 == rm:
            result += '_'.join(['DISPLACEMENT16', 'BP'])
        elif 0x7 == rm:
            result += '_'.join(['DISPLACEMENT16', 'BX'])
    if 0x3 == mod:
        # No memory access here
        result = effect
    return result

def generateModRMTable(opcode, accessType, is16Bits):
    result = []
    if not is16Bits:
        for i in xrange(0x100):
            result.append(ModRMOpcode32(accessType, i, ''))
    else:
        for i in xrange(0x100):
            result.append(ModRMOpcode16(accessType, i, ''))

    return result

def generateTable(opcode):
    pass

PROCESSORS = {
        '00' : 0x00, # 8086
        '01' : 0x01, # 80186
        '02' : 0x02, # 80286
        '03' : 0x03, # 80386
        '04' : 0x04, # 80486
        'P1' : 0x05, # Pentium
        'PX' : 0x06, # Pentium with MMX
        'PP' : 0x07, # Pentium Pro
        'P2' : 0x08, # PentiumII
        'P3' : 0x09, # PentiumIII
        'P4' : 0x0A, # Pentium4
        'C1' : 0x0B, # Core
        'C2' : 0x0C, # Core2
        'C7' : 0x0D, # Corei7
        'IT' : 0xff } # Itanium

def getAllText(node, result=''):
    if None != node.text:
        result += node.text
    for subnode in node.getchildren():
        result = getAllText(subnode, result)
    return result

tree = ElementTree()
tree.parse('x86reference.xml')
x86reference = tree.iter().next()
mainNodes = x86reference.getchildren()
oneByte = filter(lambda x:'one-byte' in x.tag, mainNodes)[0]
oneByte = oneByte.getchildren()
twoByte = filter(lambda x:'two-byte' in x.tag, mainNodes)[0]
twoByte = twoByte.getchildren()
opcodesEffects = [None] * 0x100
opcodesEffects[0x0f] = [None] * 0x100
opcodesEffects[PREFIX_ADDRESS_SIZE] = [None] * 0x100
opcodesEffects[PREFIX_ADDRESS_SIZE][0x0f] = [None] * 0x100
opcodesEffects[PREFIX_OPERAND_SIZE] = [None] * 0x100
opcodesEffects[PREFIX_OPERAND_SIZE][0x0f] = [None] * 0x100
opcodesEffects[PREFIX_OPERAND_SIZE][PREFIX_ADDRESS_SIZE] = [None] * 0x100
opcodesEffects[PREFIX_OPERAND_SIZE][PREFIX_ADDRESS_SIZE][0x0f] = [None] * 0x100
opcodesEffects[PREFIX_ADDRESS_SIZE][PREFIX_OPERAND_SIZE] = [None] * 0x100
opcodesEffects[PREFIX_ADDRESS_SIZE][PREFIX_OPERAND_SIZE][0x0f] = [None] * 0x100

EAX_TYPES = ['AL', 'AH', 'AX', 'EAX', 'REAX', 'rAX', 'rEAX', 'eAX']
ONE_BYTE_OPERANDS = ['AL', 'AH', 'BL', 'BH', 'CL', 'CH', 'DL', 'DH', 'Eb', 'Gb', 'Rb', 'Rw']
TWO_BYTE_OPERANDS = ['AX', 'BX', 'CX', 'DX', 'IP', 'DI', 'SI', 'FLAGS', 'SP', 'BP', 'Sw', 'Rw', 'Ew', 'Gw']
FOUR_BYTE_OPERANDS = ['EAX', 'EBX', 'ECX', 'EDX', 'EIP', 'EFLAGS', 'ESP', 'EBP', 'EDI', 'ESI', 'Ed', 'Rd', 'Gd']
def getEffectFromNode(node, oldEffect=None):
    effect = getAllText(node)
    return effect

INVALID_TAGS = [
        'invalid',
        'null',
        'undefined',
        'UD',
        'NOP',
        'HINT_NOP',
        'PREFETCHNTA',
        'PREFETCHT0',
        'PREFETCHT1',
        'PREFETCHT2',
        'BOUND',
        'LEA' ]
MODRM_ACCESS = ['Cd', 'Dd', 'Ev', 'E', 'EST', 'Gv', 'G', 'Er', 'R', 'Evqp', 'Gvqp', 'Sw', 'Ed', 'Rd', 'Gd', 'Ew', 'Gw', 'Rw', 'Eb', 'Gb', 'Rb']
def parseOpcode(codeByte, tableIndex, isTwoByte=False):
    global opcodesEffects

    isSupported = True
    src = set()
    byte = int(codeByte.attrib['value'], 16)
    if 'pri_opcd' != codeByte.tag:
        raise Exception('Unknown node at %d' % tableIndex)
    if 'ring' in codeByte.attrib:
        # Don't log privilaged opcodes, we do not support kernel at first
        isSupported = False
        #print '5 Unsupported ring for 0x%02x' % byte
    if False==isTwoByte and byte in PREFIXES:
        #print '0x%02x is a prefix' % byte
        return
    if True==isTwoByte and 0x3a == byte:
        return

    info = codeByte.getchildren()
    for entry in info:
        if 'proc_start' == entry.tag:
            # Group of opcodes, all got the same memory effect
            #print 'Set of opcodes 0x%02x' % byte
            continue
        if 'attr' in entry.attrib:
            if entry.attrib['attr'] in INVALID_TAGS:
                isSupported = False
                #print '6 Unsupported tag for opcode 0x%02x' % byte
                break
        if 'entry' != entry.tag:
            raise Exception('Opcode with no entry 0x%02x (Index %d)' % (byte, tableIndex))
        if 'mode' in entry.attrib and entry.attrib['mode'] in ['p', '0', 'f']:
            #print 'Mode opcode 0x%02x (%s)' % (byte, entry.attrib)
            isSupported = False
            break
        if 'ring' in entry.attrib and entry.attrib != '3':
            isSupported = False
            break
        proc_start = None
        for i in entry.getchildren():
            if 'proc_start' == i.tag:
                proc_start = int(i.text) #PROCESSORS[i.text]
                if 0xb < proc_start:
                    isSupported = False
                    #print '1 Unsupported opcode 0x%02x' % byte
                    break
            elif 'proc_end' == i.tag:
                proc_end = int(i.text) #PROCESSORS[i.text]
                if 0x5 > proc_end:
                    isSupported = False
                    #print '2 Unsupported opcode 0x%02x' % byte
                    break
            elif 'syntax' == i.tag:
                syntax = i.getchildren()
                for syntaxInfo in syntax:
                    if 'mnem' == syntaxInfo.tag:
                        mnem = syntaxInfo.text
                        if mnem in INVALID_TAGS:
                            src = set()
                            isSupported = False
                            #print '3 Unsupported opcode 0x%02x' % byte
                            break
                    elif 'dst' == syntaxInfo.tag:
                        src.add( getEffectFromNode(syntaxInfo) )
                    elif 'src' == syntaxInfo.tag:
                        src.add( getEffectFromNode(syntaxInfo) )
                    else:
                        raise Exception('Unknown opcode info 0x%02x' % byte)
    #if 0x3a == byte:
    #    print 'Byte 0x3a', src, isSupported

    if isSupported and 0 != len(src):
        if not src.isdisjoint(MODRM_ACCESS):
            if not src.isdisjoint(ONE_BYTE_OPERANDS):
                if False == isTwoByte:
                    opcodesEffects[byte] = \
                        generateModRMTable([byte], ACCESS_8BIT, is16Bits=False)
                    opcodesEffects[PREFIX_ADDRESS_SIZE][byte] = \
                        generateModRMTable([byte], ACCESS_8BIT, is16Bits=True)
                    opcodesEffects[PREFIX_OPERAND_SIZE][byte] = \
                        generateModRMTable([byte], ACCESS_8BIT, is16Bits=False)
                    opcodesEffects[PREFIX_OPERAND_SIZE][PREFIX_ADDRESS_SIZE][byte] = \
                        generateModRMTable([byte], ACCESS_8BIT, is16Bits=True)
                    opcodesEffects[PREFIX_ADDRESS_SIZE][PREFIX_OPERAND_SIZE][byte] = \
                        generateModRMTable([byte], ACCESS_8BIT, is16Bits=True)
                else:
                    opcodesEffects[0x0f][byte] = \
                        generateModRMTable([byte], ACCESS_8BIT, is16Bits=False)
                    opcodesEffects[PREFIX_ADDRESS_SIZE][0x0f][byte] = \
                        generateModRMTable([byte], ACCESS_8BIT, is16Bits=True)
                    opcodesEffects[PREFIX_OPERAND_SIZE][0x0f][byte] = \
                        generateModRMTable([byte], ACCESS_8BIT, is16Bits=False)
                    opcodesEffects[PREFIX_ADDRESS_SIZE][PREFIX_OPERAND_SIZE][0x0f][byte] = \
                        generateModRMTable([byte], ACCESS_8BIT, is16Bits=True)
                    opcodesEffects[PREFIX_OPERAND_SIZE][PREFIX_ADDRESS_SIZE][0x0f][byte] = \
                        generateModRMTable([byte], ACCESS_8BIT, is16Bits=True)
            elif not src.isdisjoint(TWO_BYTE_OPERANDS):
                if False == isTwoByte:
                    opcodesEffects[byte] = \
                        generateModRMTable([byte], ACCESS_16BIT, is16Bits=False)
                    opcodesEffects[PREFIX_ADDRESS_SIZE][byte] = \
                        generateModRMTable([byte], ACCESS_16BIT, is16Bits=True)
                    opcodesEffects[PREFIX_OPERAND_SIZE][byte] = \
                        generateModRMTable([byte], ACCESS_16BIT, is16Bits=False)
                    opcodesEffects[PREFIX_OPERAND_SIZE][PREFIX_ADDRESS_SIZE][byte] = \
                        generateModRMTable([byte], ACCESS_16BIT, is16Bits=True)
                    opcodesEffects[PREFIX_ADDRESS_SIZE][PREFIX_OPERAND_SIZE][byte] = \
                        generateModRMTable([byte], ACCESS_16BIT, is16Bits=True)
                else:
                    opcodesEffects[0x0f][byte] = \
                        generateModRMTable([byte], ACCESS_16BIT, is16Bits=False)
                    opcodesEffects[PREFIX_ADDRESS_SIZE][0x0f][byte] = \
                        generateModRMTable([byte], ACCESS_16BIT, is16Bits=True)
                    opcodesEffects[PREFIX_OPERAND_SIZE][0x0f][byte] = \
                        generateModRMTable([byte], ACCESS_16BIT, is16Bits=False)
                    opcodesEffects[PREFIX_ADDRESS_SIZE][PREFIX_OPERAND_SIZE][0x0f][byte] = \
                        generateModRMTable([byte], ACCESS_16BIT, is16Bits=True)
                    opcodesEffects[PREFIX_OPERAND_SIZE][PREFIX_ADDRESS_SIZE][0x0f][byte] = \
                        generateModRMTable([byte], ACCESS_16BIT, is16Bits=True)
            else:
                if False == isTwoByte:
                    opcodesEffects[byte] = \
                        generateModRMTable([byte], ACCESS_32BIT, is16Bits=False)
                    opcodesEffects[PREFIX_ADDRESS_SIZE][byte] = \
                        generateModRMTable([byte], ACCESS_32BIT, is16Bits=True)
                    opcodesEffects[PREFIX_OPERAND_SIZE][byte] = \
                        generateModRMTable([byte], ACCESS_32BIT, is16Bits=False)
                    opcodesEffects[PREFIX_OPERAND_SIZE][PREFIX_ADDRESS_SIZE][byte] = \
                        generateModRMTable([byte], ACCESS_32BIT, is16Bits=True)
                    opcodesEffects[PREFIX_ADDRESS_SIZE][PREFIX_OPERAND_SIZE][byte] = \
                        generateModRMTable([byte], ACCESS_32BIT, is16Bits=True)
                else:
                    opcodesEffects[0x0f][byte] = \
                        generateModRMTable([byte], ACCESS_32BIT, is16Bits=False)
                    opcodesEffects[PREFIX_ADDRESS_SIZE][0x0f][byte] = \
                        generateModRMTable([byte], ACCESS_32BIT, is16Bits=True)
                    opcodesEffects[PREFIX_OPERAND_SIZE][0x0f][byte] = \
                        generateModRMTable([byte], ACCESS_32BIT, is16Bits=False)
                    opcodesEffects[PREFIX_ADDRESS_SIZE][PREFIX_OPERAND_SIZE][0x0f][byte] = \
                        generateModRMTable([byte], ACCESS_32BIT, is16Bits=True)
                    opcodesEffects[PREFIX_OPERAND_SIZE][PREFIX_ADDRESS_SIZE][0x0f][byte] = \
                        generateModRMTable([byte], ACCESS_32BIT, is16Bits=True)

for tableIndex, firstByte in enumerate(oneByte):
    parseOpcode(firstByte, tableIndex)

for tableIndex, firstByte in enumerate(twoByte):
    parseOpcode(firstByte, tableIndex, isTwoByte=True)

opcodesEffects[0x06] = 'STACK_PUSH32'
opcodesEffects[0x0E] = 'STACK_PUSH32'
opcodesEffects[0x16] = 'STACK_PUSH32'
opcodesEffects[0x1E] = 'STACK_PUSH32'
opcodesEffects[0x50] = 'STACK_PUSH32'
opcodesEffects[0x51] = 'STACK_PUSH32'
opcodesEffects[0x52] = 'STACK_PUSH32'
opcodesEffects[0x53] = 'STACK_PUSH32'
opcodesEffects[0x54] = 'STACK_PUSH32'
opcodesEffects[0x55] = 'STACK_PUSH32'
opcodesEffects[0x56] = 'STACK_PUSH32'
opcodesEffects[0x57] = 'STACK_PUSH32'
opcodesEffects[0x60] = 'STACK_PUSHALL'
opcodesEffects[0x68] = 'STACK_PUSH32'
opcodesEffects[0x6a] = 'STACK_PUSH8'
opcodesEffects[0x9a] = 'STACK_PUSH32'
opcodesEffects[0x9c] = 'STACK_PUSH32'

opcodesEffects[PREFIX_ADDRESS_SIZE][0x06] = 'STACK_PUSH32'
opcodesEffects[PREFIX_ADDRESS_SIZE][0x0E] = 'STACK_PUSH32'
opcodesEffects[PREFIX_ADDRESS_SIZE][0x16] = 'STACK_PUSH32'
opcodesEffects[PREFIX_ADDRESS_SIZE][0x1E] = 'STACK_PUSH32'
opcodesEffects[PREFIX_ADDRESS_SIZE][0x50] = 'STACK_PUSH32'
opcodesEffects[PREFIX_ADDRESS_SIZE][0x51] = 'STACK_PUSH32'
opcodesEffects[PREFIX_ADDRESS_SIZE][0x52] = 'STACK_PUSH32'
opcodesEffects[PREFIX_ADDRESS_SIZE][0x53] = 'STACK_PUSH32'
opcodesEffects[PREFIX_ADDRESS_SIZE][0x54] = 'STACK_PUSH32'
opcodesEffects[PREFIX_ADDRESS_SIZE][0x55] = 'STACK_PUSH32'
opcodesEffects[PREFIX_ADDRESS_SIZE][0x56] = 'STACK_PUSH32'
opcodesEffects[PREFIX_ADDRESS_SIZE][0x57] = 'STACK_PUSH32'
opcodesEffects[PREFIX_ADDRESS_SIZE][0x60] = 'STACK_PUSHALL'
opcodesEffects[PREFIX_ADDRESS_SIZE][0x68] = 'STACK_PUSH32'
opcodesEffects[PREFIX_ADDRESS_SIZE][0x6a] = 'STACK_PUSH8'
opcodesEffects[PREFIX_ADDRESS_SIZE][0x9a] = 'STACK_PUSH32'
opcodesEffects[PREFIX_ADDRESS_SIZE][0x9c] = 'STACK_PUSH32'

opcodesEffects[PREFIX_OPERAND_SIZE][0x06] = 'STACK_PUSH16'
opcodesEffects[PREFIX_OPERAND_SIZE][0x0E] = 'STACK_PUSH16'
opcodesEffects[PREFIX_OPERAND_SIZE][0x16] = 'STACK_PUSH16'
opcodesEffects[PREFIX_OPERAND_SIZE][0x1E] = 'STACK_PUSH16'
opcodesEffects[PREFIX_OPERAND_SIZE][0x50] = 'STACK_PUSH16'
opcodesEffects[PREFIX_OPERAND_SIZE][0x51] = 'STACK_PUSH16'
opcodesEffects[PREFIX_OPERAND_SIZE][0x52] = 'STACK_PUSH16'
opcodesEffects[PREFIX_OPERAND_SIZE][0x53] = 'STACK_PUSH16'
opcodesEffects[PREFIX_OPERAND_SIZE][0x54] = 'STACK_PUSH16'
opcodesEffects[PREFIX_OPERAND_SIZE][0x55] = 'STACK_PUSH16'
opcodesEffects[PREFIX_OPERAND_SIZE][0x56] = 'STACK_PUSH16'
opcodesEffects[PREFIX_OPERAND_SIZE][0x57] = 'STACK_PUSH16'
opcodesEffects[PREFIX_OPERAND_SIZE][0x60] = 'STACK_PUSHALL16'
opcodesEffects[PREFIX_OPERAND_SIZE][0x68] = 'STACK_PUSH16'
opcodesEffects[PREFIX_OPERAND_SIZE][0x6a] = 'STACK_PUSH8'
opcodesEffects[PREFIX_OPERAND_SIZE][0x9a] = 'STACK_PUSH16'
opcodesEffects[PREFIX_OPERAND_SIZE][0x9c] = 'STACK_PUSH16'

opcodesEffects[PREFIX_ADDRESS_SIZE][PREFIX_OPERAND_SIZE][0x06] = 'STACK_PUSH16'
opcodesEffects[PREFIX_ADDRESS_SIZE][PREFIX_OPERAND_SIZE][0x0E] = 'STACK_PUSH16'
opcodesEffects[PREFIX_ADDRESS_SIZE][PREFIX_OPERAND_SIZE][0x16] = 'STACK_PUSH16'
opcodesEffects[PREFIX_ADDRESS_SIZE][PREFIX_OPERAND_SIZE][0x1E] = 'STACK_PUSH16'
opcodesEffects[PREFIX_ADDRESS_SIZE][PREFIX_OPERAND_SIZE][0x50] = 'STACK_PUSH16'
opcodesEffects[PREFIX_ADDRESS_SIZE][PREFIX_OPERAND_SIZE][0x51] = 'STACK_PUSH16'
opcodesEffects[PREFIX_ADDRESS_SIZE][PREFIX_OPERAND_SIZE][0x52] = 'STACK_PUSH16'
opcodesEffects[PREFIX_ADDRESS_SIZE][PREFIX_OPERAND_SIZE][0x53] = 'STACK_PUSH16'
opcodesEffects[PREFIX_ADDRESS_SIZE][PREFIX_OPERAND_SIZE][0x54] = 'STACK_PUSH16'
opcodesEffects[PREFIX_ADDRESS_SIZE][PREFIX_OPERAND_SIZE][0x55] = 'STACK_PUSH16'
opcodesEffects[PREFIX_ADDRESS_SIZE][PREFIX_OPERAND_SIZE][0x56] = 'STACK_PUSH16'
opcodesEffects[PREFIX_ADDRESS_SIZE][PREFIX_OPERAND_SIZE][0x57] = 'STACK_PUSH16'
opcodesEffects[PREFIX_ADDRESS_SIZE][PREFIX_OPERAND_SIZE][0x60] = 'STACK_PUSHALL16'
opcodesEffects[PREFIX_ADDRESS_SIZE][PREFIX_OPERAND_SIZE][0x68] = 'STACK_PUSH16'
opcodesEffects[PREFIX_ADDRESS_SIZE][PREFIX_OPERAND_SIZE][0x6a] = 'STACK_PUSH8'
opcodesEffects[PREFIX_ADDRESS_SIZE][PREFIX_OPERAND_SIZE][0x9a] = 'STACK_PUSH16'
opcodesEffects[PREFIX_ADDRESS_SIZE][PREFIX_OPERAND_SIZE][0x9c] = 'STACK_PUSH16'

opcodesEffects[PREFIX_OPERAND_SIZE][PREFIX_ADDRESS_SIZE][0x06] = 'STACK_PUSH16'
opcodesEffects[PREFIX_OPERAND_SIZE][PREFIX_ADDRESS_SIZE][0x0E] = 'STACK_PUSH16'
opcodesEffects[PREFIX_OPERAND_SIZE][PREFIX_ADDRESS_SIZE][0x16] = 'STACK_PUSH16'
opcodesEffects[PREFIX_OPERAND_SIZE][PREFIX_ADDRESS_SIZE][0x1E] = 'STACK_PUSH16'
opcodesEffects[PREFIX_OPERAND_SIZE][PREFIX_ADDRESS_SIZE][0x50] = 'STACK_PUSH16'
opcodesEffects[PREFIX_OPERAND_SIZE][PREFIX_ADDRESS_SIZE][0x51] = 'STACK_PUSH16'
opcodesEffects[PREFIX_OPERAND_SIZE][PREFIX_ADDRESS_SIZE][0x52] = 'STACK_PUSH16'
opcodesEffects[PREFIX_OPERAND_SIZE][PREFIX_ADDRESS_SIZE][0x53] = 'STACK_PUSH16'
opcodesEffects[PREFIX_OPERAND_SIZE][PREFIX_ADDRESS_SIZE][0x54] = 'STACK_PUSH16'
opcodesEffects[PREFIX_OPERAND_SIZE][PREFIX_ADDRESS_SIZE][0x55] = 'STACK_PUSH16'
opcodesEffects[PREFIX_OPERAND_SIZE][PREFIX_ADDRESS_SIZE][0x56] = 'STACK_PUSH16'
opcodesEffects[PREFIX_OPERAND_SIZE][PREFIX_ADDRESS_SIZE][0x57] = 'STACK_PUSH16'
opcodesEffects[PREFIX_OPERAND_SIZE][PREFIX_ADDRESS_SIZE][0x60] = 'STACK_PUSHALL16'
opcodesEffects[PREFIX_OPERAND_SIZE][PREFIX_ADDRESS_SIZE][0x68] = 'STACK_PUSH16'
opcodesEffects[PREFIX_OPERAND_SIZE][PREFIX_ADDRESS_SIZE][0x6a] = 'STACK_PUSH8'
opcodesEffects[PREFIX_OPERAND_SIZE][PREFIX_ADDRESS_SIZE][0x9a] = 'STACK_PUSH16'
opcodesEffects[PREFIX_OPERAND_SIZE][PREFIX_ADDRESS_SIZE][0x9c] = 'STACK_PUSH16'

opcodesEffects[PREFIX_LOCK] = 'CONTINUE'
opcodesEffects[PREFIX_REPZ] = 'CONTINUE'
opcodesEffects[PREFIX_REPNZ] = 'CONTINUE'

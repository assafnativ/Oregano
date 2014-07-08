
import distorm3
import types
import copy

execfile('x86header.py')
execfile('x86sets.py')

class DisasmGenerator( object ):
    def __init__(self):
        self.fullTable32 = None
        self.fullTable64 = None

    def getTable32(self):
        if None == self.fullTable32:
            self.generateTables()
        return self.fullTable32
    def getTable64(self):
        if None == self.fullTable64:
            self.generateTables()
        return self.fullTable64

    def _makeArray(self, d):
        if len(d) > 1:
            return [self._makeArray(d[1:]) for i in range(d[0])]
        return [None] * d[0]

    def printOpcode(self, opcode):
        print '%4x %-20s %s' % (opcode[1], opcode[3], opcode[2])

    def generateTables(self):
        self.insts = []
        Instructions( lambda c, *args: self.insts.append((c, args)) )

        self.t32 = self._makeArray([4, 0x100])
        self.t64 = self._makeArray([4, 0x10, 0x100])

        OperandType.PREFIX = 70
        self.insts.append((12, (0, [0xf0], ["LOCK"], [OperandType.PREFIX], 0)))
        self.insts.append((12, (0, [0xf2], ["REPNZ"], [OperandType.PREFIX], 0)))
        self.insts.append((12, (0, [0xf3], ["REP"], [OperandType.PREFIX], 0)))
        self.insts.append((12, (0, [0x2e], ["CS"], [OperandType.PREFIX], 0)))
        self.insts.append((12, (0, [0x36], ["SS"], [OperandType.PREFIX], 0)))
        self.insts.append((12, (0, [0x3e], ["DS"], [OperandType.PREFIX], 0)))
        self.insts.append((12, (0, [0x26], ["ES"], [OperandType.PREFIX], 0)))
        self.insts.append((12, (0, [0x64], ["FS"], [OperandType.PREFIX], 0)))
        self.insts.append((12, (0, [0x65], ["GS"], [OperandType.PREFIX], 0)))
        self.insts.append((12, (0, [0x66], ["op_size"], [OperandType.PREFIX], 0)))
        self.insts.append((12, (0, [0x67], ["address_size"], [OperandType.PREFIX], 0)))

        self.REGS8_IDS   = ['AL',  'CL',  'DL',  'BL',  'AH',  'CH',  'DH',  'BH']
        self.REGS16_IDS  = ['AX',  'CX',  'DX',  'BX',  'SP',  'BP',  'SI',  'DI']
        self.REGS32_IDS  = ['EAX', 'ECX', 'EDX', 'EBX', 'ESP', 'EBP', 'ESI', 'EDI']
        self.REGS64_IDS  = ['RAX', 'RCX', 'RDX', 'RBX', 'RSP', 'RBP', 'RSI', 'RDI']
        self.DISP16_IDS  = ['BX_PLUS_SI', 'BX_PLUS_DI', 'BP_PLUS_SI', 'BP_PLUS_DI', 'SI', 'DI', 'BP', 'BX']
        self.REGS8A_IDS  = ['R8B', 'R9B', 'R10B', 'R11B', 'R12B', 'R13B', 'R14B', 'R15B']
        self.REGS16A_IDS = ['R8W', 'R9W', 'R10W', 'R11W', 'R12W', 'R13W', 'R14W', 'R15W']
        self.REGS32A_IDS = ['R8D', 'R9D', 'R10D', 'R11D', 'R12D', 'R13D', 'R14D', 'R15D']
        self.REGS64A_IDS = ['R8',  'R9',  'R10', 'R11', 'R12', 'R13', 'R14', 'R15']

        self.sibTable      = [None] * 0x100
        self.sib64Table    = self._makeArray([4, 0x100])
        self.sib32Table    = self._makeArray([4, 0x100])

        for index in range(8):
            for base in range(8):
                index_base = (index << 3) + base
                if 0x04 != index:
                    if 0x05 != base:
                        self.sibTable     [0x00 + index_base] = self.REGS32_IDS[base]  + '_' + self.REGS32_IDS[index]  + '_1' + '_SIB'
                        self.sibTable     [0x40 + index_base] = self.REGS32_IDS[base]  + '_' + self.REGS32_IDS[index]  + '_2' + '_SIB'
                        self.sibTable     [0x80 + index_base] = self.REGS32_IDS[base]  + '_' + self.REGS32_IDS[index]  + '_4' + '_SIB'
                        self.sibTable     [0xc0 + index_base] = self.REGS32_IDS[base]  + '_' + self.REGS32_IDS[index]  + '_8' + '_SIB'
                        self.sib64Table[0][0x00 + index_base] = self.REGS64_IDS[base]  + '_' + self.REGS64_IDS[index]  + '_1' + '_SIB'
                        self.sib64Table[0][0x40 + index_base] = self.REGS64_IDS[base]  + '_' + self.REGS64_IDS[index]  + '_2' + '_SIB'
                        self.sib64Table[0][0x80 + index_base] = self.REGS64_IDS[base]  + '_' + self.REGS64_IDS[index]  + '_4' + '_SIB'
                        self.sib64Table[0][0xc0 + index_base] = self.REGS64_IDS[base]  + '_' + self.REGS64_IDS[index]  + '_8' + '_SIB'
                        self.sib64Table[1][0x00 + index_base] = self.REGS64A_IDS[base] + '_' + self.REGS64_IDS[index]  + '_1' + '_SIB'
                        self.sib64Table[1][0x40 + index_base] = self.REGS64A_IDS[base] + '_' + self.REGS64_IDS[index]  + '_2' + '_SIB'
                        self.sib64Table[1][0x80 + index_base] = self.REGS64A_IDS[base] + '_' + self.REGS64_IDS[index]  + '_4' + '_SIB'
                        self.sib64Table[1][0xc0 + index_base] = self.REGS64A_IDS[base] + '_' + self.REGS64_IDS[index]  + '_8' + '_SIB'
                        self.sib64Table[2][0x00 + index_base] = self.REGS64_IDS[base]  + '_' + self.REGS64A_IDS[index] + '_1' + '_SIB'
                        self.sib64Table[2][0x40 + index_base] = self.REGS64_IDS[base]  + '_' + self.REGS64A_IDS[index] + '_2' + '_SIB'
                        self.sib64Table[2][0x80 + index_base] = self.REGS64_IDS[base]  + '_' + self.REGS64A_IDS[index] + '_4' + '_SIB'
                        self.sib64Table[2][0xc0 + index_base] = self.REGS64_IDS[base]  + '_' + self.REGS64A_IDS[index] + '_8' + '_SIB'
                        self.sib64Table[3][0x00 + index_base] = self.REGS64A_IDS[base] + '_' + self.REGS64A_IDS[index] + '_1' + '_SIB'
                        self.sib64Table[3][0x40 + index_base] = self.REGS64A_IDS[base] + '_' + self.REGS64A_IDS[index] + '_2' + '_SIB'
                        self.sib64Table[3][0x80 + index_base] = self.REGS64A_IDS[base] + '_' + self.REGS64A_IDS[index] + '_4' + '_SIB'
                        self.sib64Table[3][0xc0 + index_base] = self.REGS64A_IDS[base] + '_' + self.REGS64A_IDS[index] + '_8' + '_SIB'
                        self.sib32Table[0][0x00 + index_base] = self.REGS32_IDS[base]  + '_' + self.REGS32_IDS[index]  + '_1' + '_SIB'
                        self.sib32Table[0][0x40 + index_base] = self.REGS32_IDS[base]  + '_' + self.REGS32_IDS[index]  + '_2' + '_SIB'
                        self.sib32Table[0][0x80 + index_base] = self.REGS32_IDS[base]  + '_' + self.REGS32_IDS[index]  + '_4' + '_SIB'
                        self.sib32Table[0][0xc0 + index_base] = self.REGS32_IDS[base]  + '_' + self.REGS32_IDS[index]  + '_8' + '_SIB'
                        self.sib32Table[1][0x00 + index_base] = self.REGS32A_IDS[base] + '_' + self.REGS32_IDS[index]  + '_1' + '_SIB'
                        self.sib32Table[1][0x40 + index_base] = self.REGS32A_IDS[base] + '_' + self.REGS32_IDS[index]  + '_2' + '_SIB'
                        self.sib32Table[1][0x80 + index_base] = self.REGS32A_IDS[base] + '_' + self.REGS32_IDS[index]  + '_4' + '_SIB'
                        self.sib32Table[1][0xc0 + index_base] = self.REGS32A_IDS[base] + '_' + self.REGS32_IDS[index]  + '_8' + '_SIB'
                        self.sib32Table[2][0x00 + index_base] = self.REGS32_IDS[base]  + '_' + self.REGS32A_IDS[index] + '_1' + '_SIB'
                        self.sib32Table[2][0x40 + index_base] = self.REGS32_IDS[base]  + '_' + self.REGS32A_IDS[index] + '_2' + '_SIB'
                        self.sib32Table[2][0x80 + index_base] = self.REGS32_IDS[base]  + '_' + self.REGS32A_IDS[index] + '_4' + '_SIB'
                        self.sib32Table[2][0xc0 + index_base] = self.REGS32_IDS[base]  + '_' + self.REGS32A_IDS[index] + '_8' + '_SIB'
                        self.sib32Table[3][0x00 + index_base] = self.REGS32A_IDS[base] + '_' + self.REGS32A_IDS[index] + '_1' + '_SIB'
                        self.sib32Table[3][0x40 + index_base] = self.REGS32A_IDS[base] + '_' + self.REGS32A_IDS[index] + '_2' + '_SIB'
                        self.sib32Table[3][0x80 + index_base] = self.REGS32A_IDS[base] + '_' + self.REGS32A_IDS[index] + '_4' + '_SIB'
                        self.sib32Table[3][0xc0 + index_base] = self.REGS32A_IDS[base] + '_' + self.REGS32A_IDS[index] + '_8' + '_SIB'
                    else:
                        self.sibTable     [0x00 + index_base] = '_NOBASE_' + self.REGS32_IDS[index]  + '_1' + '_SIB'
                        self.sibTable     [0x40 + index_base] = '_NOBASE_' + self.REGS32_IDS[index]  + '_2' + '_SIB'
                        self.sibTable     [0x80 + index_base] = '_NOBASE_' + self.REGS32_IDS[index]  + '_4' + '_SIB'
                        self.sibTable     [0xc0 + index_base] = '_NOBASE_' + self.REGS32_IDS[index]  + '_8' + '_SIB'
                        self.sib64Table[0][0x00 + index_base] = '_NOBASE_' + self.REGS64_IDS[index]  + '_1' + '_SIB'
                        self.sib64Table[0][0x40 + index_base] = '_NOBASE_' + self.REGS64_IDS[index]  + '_2' + '_SIB'
                        self.sib64Table[0][0x80 + index_base] = '_NOBASE_' + self.REGS64_IDS[index]  + '_4' + '_SIB'
                        self.sib64Table[0][0xc0 + index_base] = '_NOBASE_' + self.REGS64_IDS[index]  + '_8' + '_SIB'
                        self.sib64Table[1][0x00 + index_base] = '_NOBASE_' + self.REGS64_IDS[index]  + '_1' + '_SIB'
                        self.sib64Table[1][0x40 + index_base] = '_NOBASE_' + self.REGS64_IDS[index]  + '_2' + '_SIB'
                        self.sib64Table[1][0x80 + index_base] = '_NOBASE_' + self.REGS64_IDS[index]  + '_4' + '_SIB'
                        self.sib64Table[1][0xc0 + index_base] = '_NOBASE_' + self.REGS64_IDS[index]  + '_8' + '_SIB'
                        self.sib64Table[2][0x00 + index_base] = '_NOBASE_' + self.REGS64A_IDS[index] + '_1' + '_SIB'
                        self.sib64Table[2][0x40 + index_base] = '_NOBASE_' + self.REGS64A_IDS[index] + '_2' + '_SIB'
                        self.sib64Table[2][0x80 + index_base] = '_NOBASE_' + self.REGS64A_IDS[index] + '_4' + '_SIB'
                        self.sib64Table[2][0xc0 + index_base] = '_NOBASE_' + self.REGS64A_IDS[index] + '_8' + '_SIB'
                        self.sib64Table[3][0x00 + index_base] = '_NOBASE_' + self.REGS64A_IDS[index] + '_1' + '_SIB'
                        self.sib64Table[3][0x40 + index_base] = '_NOBASE_' + self.REGS64A_IDS[index] + '_2' + '_SIB'
                        self.sib64Table[3][0x80 + index_base] = '_NOBASE_' + self.REGS64A_IDS[index] + '_4' + '_SIB'
                        self.sib64Table[3][0xc0 + index_base] = '_NOBASE_' + self.REGS64A_IDS[index] + '_8' + '_SIB'
                        self.sib32Table[0][0x00 + index_base] = '_NOBASE_' + self.REGS32_IDS[index]  + '_1' + '_SIB'
                        self.sib32Table[0][0x40 + index_base] = '_NOBASE_' + self.REGS32_IDS[index]  + '_2' + '_SIB'
                        self.sib32Table[0][0x80 + index_base] = '_NOBASE_' + self.REGS32_IDS[index]  + '_4' + '_SIB'
                        self.sib32Table[0][0xc0 + index_base] = '_NOBASE_' + self.REGS32_IDS[index]  + '_8' + '_SIB'
                        self.sib32Table[1][0x00 + index_base] = '_NOBASE_' + self.REGS32_IDS[index]  + '_1' + '_SIB'
                        self.sib32Table[1][0x40 + index_base] = '_NOBASE_' + self.REGS32_IDS[index]  + '_2' + '_SIB'
                        self.sib32Table[1][0x80 + index_base] = '_NOBASE_' + self.REGS32_IDS[index]  + '_4' + '_SIB'
                        self.sib32Table[1][0xc0 + index_base] = '_NOBASE_' + self.REGS32_IDS[index]  + '_8' + '_SIB'
                        self.sib32Table[2][0x00 + index_base] = '_NOBASE_' + self.REGS32A_IDS[index] + '_1' + '_SIB'
                        self.sib32Table[2][0x40 + index_base] = '_NOBASE_' + self.REGS32A_IDS[index] + '_2' + '_SIB'
                        self.sib32Table[2][0x80 + index_base] = '_NOBASE_' + self.REGS32A_IDS[index] + '_4' + '_SIB'
                        self.sib32Table[2][0xc0 + index_base] = '_NOBASE_' + self.REGS32A_IDS[index] + '_8' + '_SIB'
                        self.sib32Table[3][0x00 + index_base] = '_NOBASE_' + self.REGS32A_IDS[index] + '_1' + '_SIB'
                        self.sib32Table[3][0x40 + index_base] = '_NOBASE_' + self.REGS32A_IDS[index] + '_2' + '_SIB'
                        self.sib32Table[3][0x80 + index_base] = '_NOBASE_' + self.REGS32A_IDS[index] + '_4' + '_SIB'
                        self.sib32Table[3][0xc0 + index_base] = '_NOBASE_' + self.REGS32A_IDS[index] + '_8' + '_SIB'
                else:
                    if 0x05 != base:
                        self.sibTable     [0x00 + index_base] = self.REGS32_IDS[base]
                        self.sibTable     [0x40 + index_base] = self.REGS32_IDS[base]
                        self.sibTable     [0x80 + index_base] = self.REGS32_IDS[base]
                        self.sibTable     [0xc0 + index_base] = self.REGS32_IDS[base]
                        self.sib64Table[0][0x00 + index_base] = self.REGS64_IDS[base]
                        self.sib64Table[0][0x40 + index_base] = self.REGS64_IDS[base]
                        self.sib64Table[0][0x80 + index_base] = self.REGS64_IDS[base]
                        self.sib64Table[0][0xc0 + index_base] = self.REGS64_IDS[base]
                        self.sib64Table[1][0x00 + index_base] = self.REGS64A_IDS[base]
                        self.sib64Table[1][0x40 + index_base] = self.REGS64A_IDS[base]
                        self.sib64Table[1][0x80 + index_base] = self.REGS64A_IDS[base]
                        self.sib64Table[1][0xc0 + index_base] = self.REGS64A_IDS[base]
                        self.sib64Table[2][0x00 + index_base] = self.REGS64_IDS[base]
                        self.sib64Table[2][0x40 + index_base] = self.REGS64_IDS[base]
                        self.sib64Table[2][0x80 + index_base] = self.REGS64_IDS[base]
                        self.sib64Table[2][0xc0 + index_base] = self.REGS64_IDS[base]
                        self.sib64Table[3][0x00 + index_base] = self.REGS64A_IDS[base]
                        self.sib64Table[3][0x40 + index_base] = self.REGS64A_IDS[base]
                        self.sib64Table[3][0x80 + index_base] = self.REGS64A_IDS[base]
                        self.sib64Table[3][0xc0 + index_base] = self.REGS64A_IDS[base]
                        self.sib32Table[0][0x00 + index_base] = self.REGS32_IDS[base]
                        self.sib32Table[0][0x40 + index_base] = self.REGS32_IDS[base]
                        self.sib32Table[0][0x80 + index_base] = self.REGS32_IDS[base]
                        self.sib32Table[0][0xc0 + index_base] = self.REGS32_IDS[base]
                        self.sib32Table[1][0x00 + index_base] = self.REGS32A_IDS[base]
                        self.sib32Table[1][0x40 + index_base] = self.REGS32A_IDS[base]
                        self.sib32Table[1][0x80 + index_base] = self.REGS32A_IDS[base]
                        self.sib32Table[1][0xc0 + index_base] = self.REGS32A_IDS[base]
                        self.sib32Table[2][0x00 + index_base] = self.REGS32_IDS[base]
                        self.sib32Table[2][0x40 + index_base] = self.REGS32_IDS[base]
                        self.sib32Table[2][0x80 + index_base] = self.REGS32_IDS[base]
                        self.sib32Table[2][0xc0 + index_base] = self.REGS32_IDS[base]
                        self.sib32Table[3][0x00 + index_base] = self.REGS32A_IDS[base]
                        self.sib32Table[3][0x40 + index_base] = self.REGS32A_IDS[base]
                        self.sib32Table[3][0x80 + index_base] = self.REGS32A_IDS[base]
                        self.sib32Table[3][0xc0 + index_base] = self.REGS32A_IDS[base]
                    else:
                        self.sibTable[0x00 + index_base] = ''
                        self.sibTable[0x40 + index_base] = ''
                        self.sibTable[0x80 + index_base] = ''
                        self.sibTable[0xc0 + index_base] = ''
                        for rex in range(4):
                            self.sib64Table[rex][0x00 + index_base] = ''
                            self.sib64Table[rex][0x40 + index_base] = ''
                            self.sib64Table[rex][0x80 + index_base] = ''
                            self.sib64Table[rex][0xc0 + index_base] = ''
                            self.sib32Table[rex][0x00 + index_base] = ''
                            self.sib32Table[rex][0x40 + index_base] = ''
                            self.sib32Table[rex][0x80 + index_base] = ''
                            self.sib32Table[rex][0xc0 + index_base] = ''

        self.buildRMTable()
        self.buildOOTable()

        for opcode in self.insts:
            t, desc = opcode
            opcode_length, opcode_bytes, opcode_name, operand_type, inst_flags = desc
            mask = None
            maskTarget = 0

            if OpcodeLength.OL_1 == opcode_length:
                opcodeByte = opcode_bytes[0]
                if 0x06 == opcodeByte:
                    # PUSH
                    self.setOpcodeEffect(opcode_bytes, 'DWORDPTR_STACK_PUSH', 'WORDPTR_STACK_PUSH', 'DWORDPTR_STACK_PUSH', 'WORDPTR_STACK_PUSH')
                    continue
                elif 0x07 == opcodeByte:
                    # POP
                    self.setOpcodeEffect(opcode_bytes, 'DWORDPTR_STACK_POP', 'WORDPTR_STACK_POP', 'DWORDPTR_STACK_POP', 'WORDPTR_STACK_POP')
                    continue
                elif 0x0e == opcodeByte:
                    # PUSH
                    self.setOpcodeEffect(opcode_bytes, 'DWORDPTR_STACK_PUSH', 'WORDPTR_STACK_PUSH', 'DWORDPTR_STACK_PUSH', 'WORDPTR_STACK_PUSH')
                    continue
                elif 0x16 == opcodeByte:
                    # PUSH
                    self.setOpcodeEffect(opcode_bytes, 'DWORDPTR_STACK_PUSH', 'WORDPTR_STACK_PUSH', 'DWORDPTR_STACK_PUSH', 'WORDPTR_STACK_PUSH')
                    continue
                elif 0x17 == opcodeByte:
                    # POP
                    self.setOpcodeEffect(opcode_bytes, 'DWORDPTR_STACK_POP', 'WORDPTR_STACK_POP', 'DWORDPTR_STACK_POP', 'WORDPTR_STACK_POP')
                    continue
                elif 0x1e == opcodeByte:
                    # PUSH seg
                    self.setOpcodeEffect(opcode_bytes, 'DWORDPTR_STACK_PUSH', 'WORDPTR_STACK_PUSH', 'DWORDPTR_STACK_PUSH', 'WORDPTR_STACK_PUSH')
                    continue
                elif 0x1f == opcodeByte:
                    # POP seg
                    self.setOpcodeEffect(opcode_bytes, 'DWORDPTR_STACK_POP', 'WORDPTR_STACK_POP', 'DWORDPTR_STACK_POP', 'WORDPTR_STACK_POP')
                    continue
                elif 0x50 == opcodeByte:
                    # PUSH reg
                    self.setOpcodeEffect([opcodeByte + 0], 'DWORDPTR_STACK_PUSH', 'WORDPTR_STACK_PUSH', 'DWORDPTR_STACK_PUSH', 'WORDPTR_STACK_PUSH')
                    self.setOpcodeEffect([opcodeByte + 1], 'DWORDPTR_STACK_PUSH', 'WORDPTR_STACK_PUSH', 'DWORDPTR_STACK_PUSH', 'WORDPTR_STACK_PUSH')
                    self.setOpcodeEffect([opcodeByte + 2], 'DWORDPTR_STACK_PUSH', 'WORDPTR_STACK_PUSH', 'DWORDPTR_STACK_PUSH', 'WORDPTR_STACK_PUSH')
                    self.setOpcodeEffect([opcodeByte + 3], 'DWORDPTR_STACK_PUSH', 'WORDPTR_STACK_PUSH', 'DWORDPTR_STACK_PUSH', 'WORDPTR_STACK_PUSH')
                    self.setOpcodeEffect([opcodeByte + 4], 'DWORDPTR_STACK_PUSH', 'WORDPTR_STACK_PUSH', 'DWORDPTR_STACK_PUSH', 'WORDPTR_STACK_PUSH')
                    self.setOpcodeEffect([opcodeByte + 5], 'DWORDPTR_STACK_PUSH', 'WORDPTR_STACK_PUSH', 'DWORDPTR_STACK_PUSH', 'WORDPTR_STACK_PUSH')
                    self.setOpcodeEffect([opcodeByte + 6], 'DWORDPTR_STACK_PUSH', 'WORDPTR_STACK_PUSH', 'DWORDPTR_STACK_PUSH', 'WORDPTR_STACK_PUSH')
                    self.setOpcodeEffect([opcodeByte + 7], 'DWORDPTR_STACK_PUSH', 'WORDPTR_STACK_PUSH', 'DWORDPTR_STACK_PUSH', 'WORDPTR_STACK_PUSH')
                    for rex in range(0x10):
                        self.setOpcodeEffect([opcodeByte + 0], ['QWORDPTR_STACK_PUSH'] * 0x10, ['WORDPTR_STACK_PUSH'] * 0x10, ['QWORDPTR_STACK_PUSH'] * 0x10, ['WORDPTR_STACK_PUSH'] * 0x10, is64=True, rex=rex)
                        self.setOpcodeEffect([opcodeByte + 1], ['QWORDPTR_STACK_PUSH'] * 0x10, ['WORDPTR_STACK_PUSH'] * 0x10, ['QWORDPTR_STACK_PUSH'] * 0x10, ['WORDPTR_STACK_PUSH'] * 0x10, is64=True, rex=rex)
                        self.setOpcodeEffect([opcodeByte + 2], ['QWORDPTR_STACK_PUSH'] * 0x10, ['WORDPTR_STACK_PUSH'] * 0x10, ['QWORDPTR_STACK_PUSH'] * 0x10, ['WORDPTR_STACK_PUSH'] * 0x10, is64=True, rex=rex)
                        self.setOpcodeEffect([opcodeByte + 3], ['QWORDPTR_STACK_PUSH'] * 0x10, ['WORDPTR_STACK_PUSH'] * 0x10, ['QWORDPTR_STACK_PUSH'] * 0x10, ['WORDPTR_STACK_PUSH'] * 0x10, is64=True, rex=rex)
                        self.setOpcodeEffect([opcodeByte + 4], ['QWORDPTR_STACK_PUSH'] * 0x10, ['WORDPTR_STACK_PUSH'] * 0x10, ['QWORDPTR_STACK_PUSH'] * 0x10, ['WORDPTR_STACK_PUSH'] * 0x10, is64=True, rex=rex)
                        self.setOpcodeEffect([opcodeByte + 5], ['QWORDPTR_STACK_PUSH'] * 0x10, ['WORDPTR_STACK_PUSH'] * 0x10, ['QWORDPTR_STACK_PUSH'] * 0x10, ['WORDPTR_STACK_PUSH'] * 0x10, is64=True, rex=rex)
                        self.setOpcodeEffect([opcodeByte + 6], ['QWORDPTR_STACK_PUSH'] * 0x10, ['WORDPTR_STACK_PUSH'] * 0x10, ['QWORDPTR_STACK_PUSH'] * 0x10, ['WORDPTR_STACK_PUSH'] * 0x10, is64=True, rex=rex)
                        self.setOpcodeEffect([opcodeByte + 7], ['QWORDPTR_STACK_PUSH'] * 0x10, ['WORDPTR_STACK_PUSH'] * 0x10, ['QWORDPTR_STACK_PUSH'] * 0x10, ['WORDPTR_STACK_PUSH'] * 0x10, is64=True, rex=rex)
                    continue
                elif 0x58 == opcodeByte:
                    # POP reg
                    self.setOpcodeEffect([opcodeByte + 0], 'DWORDPTR_STACK_POP', 'WORDPTR_STACK_POP', 'DWORDPTR_STACK_POP', 'WORDPTR_STACK_POP')
                    self.setOpcodeEffect([opcodeByte + 1], 'DWORDPTR_STACK_POP', 'WORDPTR_STACK_POP', 'DWORDPTR_STACK_POP', 'WORDPTR_STACK_POP')
                    self.setOpcodeEffect([opcodeByte + 2], 'DWORDPTR_STACK_POP', 'WORDPTR_STACK_POP', 'DWORDPTR_STACK_POP', 'WORDPTR_STACK_POP')
                    self.setOpcodeEffect([opcodeByte + 3], 'DWORDPTR_STACK_POP', 'WORDPTR_STACK_POP', 'DWORDPTR_STACK_POP', 'WORDPTR_STACK_POP')
                    self.setOpcodeEffect([opcodeByte + 4], 'DWORDPTR_STACK_POP', 'WORDPTR_STACK_POP', 'DWORDPTR_STACK_POP', 'WORDPTR_STACK_POP')
                    self.setOpcodeEffect([opcodeByte + 5], 'DWORDPTR_STACK_POP', 'WORDPTR_STACK_POP', 'DWORDPTR_STACK_POP', 'WORDPTR_STACK_POP')
                    self.setOpcodeEffect([opcodeByte + 6], 'DWORDPTR_STACK_POP', 'WORDPTR_STACK_POP', 'DWORDPTR_STACK_POP', 'WORDPTR_STACK_POP')
                    self.setOpcodeEffect([opcodeByte + 7], 'DWORDPTR_STACK_POP', 'WORDPTR_STACK_POP', 'DWORDPTR_STACK_POP', 'WORDPTR_STACK_POP')
                    for rex in range(0x10):
                        self.setOpcodeEffect([opcodeByte + 0], ['QWORDPTR_STACK_POP'] * 0x10, ['WORDPTR_STACK_POP'] * 0x10, ['QWORDPTR_STACK_POP'] * 0x10, ['WORDPTR_STACK_POP'] * 0x10, is64=True, rex=rex)
                        self.setOpcodeEffect([opcodeByte + 1], ['QWORDPTR_STACK_POP'] * 0x10, ['WORDPTR_STACK_POP'] * 0x10, ['QWORDPTR_STACK_POP'] * 0x10, ['WORDPTR_STACK_POP'] * 0x10, is64=True, rex=rex)
                        self.setOpcodeEffect([opcodeByte + 2], ['QWORDPTR_STACK_POP'] * 0x10, ['WORDPTR_STACK_POP'] * 0x10, ['QWORDPTR_STACK_POP'] * 0x10, ['WORDPTR_STACK_POP'] * 0x10, is64=True, rex=rex)
                        self.setOpcodeEffect([opcodeByte + 3], ['QWORDPTR_STACK_POP'] * 0x10, ['WORDPTR_STACK_POP'] * 0x10, ['QWORDPTR_STACK_POP'] * 0x10, ['WORDPTR_STACK_POP'] * 0x10, is64=True, rex=rex)
                        self.setOpcodeEffect([opcodeByte + 4], ['QWORDPTR_STACK_POP'] * 0x10, ['WORDPTR_STACK_POP'] * 0x10, ['QWORDPTR_STACK_POP'] * 0x10, ['WORDPTR_STACK_POP'] * 0x10, is64=True, rex=rex)
                        self.setOpcodeEffect([opcodeByte + 5], ['QWORDPTR_STACK_POP'] * 0x10, ['WORDPTR_STACK_POP'] * 0x10, ['QWORDPTR_STACK_POP'] * 0x10, ['WORDPTR_STACK_POP'] * 0x10, is64=True, rex=rex)
                        self.setOpcodeEffect([opcodeByte + 6], ['QWORDPTR_STACK_POP'] * 0x10, ['WORDPTR_STACK_POP'] * 0x10, ['QWORDPTR_STACK_POP'] * 0x10, ['WORDPTR_STACK_POP'] * 0x10, is64=True, rex=rex)
                        self.setOpcodeEffect([opcodeByte + 7], ['QWORDPTR_STACK_POP'] * 0x10, ['WORDPTR_STACK_POP'] * 0x10, ['QWORDPTR_STACK_POP'] * 0x10, ['WORDPTR_STACK_POP'] * 0x10, is64=True, rex=rex)
                    continue
                elif 0x60 == opcodeByte:
                    # PUSHA
                    self.setOpcodeEffect(opcode_bytes, 'ALL32PTR_STACK_PUSH', 'ALL16PTR_STACK_PUSH', 'ALL32PTR_STACK_PUSH', 'ALL16PTR_STACK_PUSH')
                    continue
                elif 0x61 == opcodeByte:
                    # PUSHA
                    self.setOpcodeEffect(opcode_bytes, 'ALL32PTR_STACK_POP', 'ALL16PTR_STACK_POP', 'ALL32PTR_STACK_POP', 'ALL16PTR_STACK_POP')
                    continue
                elif 0x68 == opcodeByte:
                    # PUSH imm64 / imm32 / imm16
                    self.setOpcodeEffect(opcode_bytes, 'DWORDPTR_STACK_PUSH', 'WORDPTR_STACK_PUSH', 'DWORDPTR_STACK_PUSH', 'WORDPTR_STACK_PUSH')
                    for rex in range(0x10):
                        self.setOpcodeEffect(opcode_bytes, ['QWORDPTR_STACK_PUSH'] * 0x10, ['QWORDPTR_STACK_PUSH'] * 0x10, ['QWORDPTR_STACK_PUSH'] * 0x10, ['QWORDPTR_STACK_PUSH'] * 0x10, is64=True, rex=rex)
                    continue
                elif 0x6a == opcodeByte:
                    # PUSH imm8
                    self.setOpcodeEffect(opcode_bytes, 'BYTEPTR_STACK_PUSH', 'BYTEPTR_STACK_PUSH', 'BYTEPTR_STACK_PUSH', 'BYTEPTR_STACK_PUSH')
                    for rex in range(0x10):
                        self.setOpcodeEffect(opcode_bytes, ['BYTEPTR_STACK_PUSH'] * 0x10, ['BYTEPTR_STACK_PUSH'] * 0x10, ['BYTEPTR_STACK_PUSH'] * 0x10, ['BYTEPTR_STACK_PUSH'] * 0x10, is64=True, rex=rex)
                    continue
                elif 0xe8 == opcodeByte:
                    # Call
                    self.setOpcodeEffect(opcode_bytes, 'DWORDPTR_STACK_PUSH', 'DWORDPTR_STACK_PUSH', 'DWORDPTR_STACK_PUSH', 'DWORDPTR_STACK_PUSH')
                    for rex in range(0x10):
                        self.setOpcodeEffect(opcode_bytes, ['QWORDPTR_STACK_PUSH'] * 0x10, ['QWORDPTR_STACK_PUSH'] * 0x10, ['QWORDPTR_STACK_PUSH'] * 0x10, ['QWORDPTR_STACK_PUSH'] * 0x10, is64=True, rex=rex)
                    continue
                elif 0x9a == opcodeByte:
                    # Call far
                    self.setOpcodeEffect(opcode_bytes, 'DWORDPTR_STACK_PUSH', 'DWORDPTR_STACK_PUSH', 'DWORDPTR_STACK_PUSH', 'DWORDPTR_STACK_PUSH')
                    continue
                elif 0xc8 == opcodeByte:
                    # ENTER
                    self.setOpcodeEffect(opcode_bytes, 'DWORDPTR_STACK_PUSH', 'DWORDPTR_STACK_PUSH', 'DWORDPTR_STACK_PUSH', 'DWORDPTR_STACK_PUSH')
                    for rex in range(0x10):
                        self.setOpcodeEffect(opcode_bytes, ['QWORDPTR_STACK_PUSH'] * 0x10, ['QWORDPTR_STACK_PUSH'] * 0x10, ['QWORDPTR_STACK_PUSH'] * 0x10, ['QWORDPTR_STACK_PUSH'] * 0x10, is64=True, rex=rex)
                    continue
                elif 0xc9 == opcodeByte:
                    # LEAVE
                    self.setOpcodeEffect(opcode_bytes, 'DWORDPTR_STACK_POP', 'DWORDPTR_STACK_POP', 'DWORDPTR_STACK_POP', 'DWORDPTR_STACK_POP')
                    for rex in range(0x10):
                        self.setOpcodeEffect(opcode_bytes, ['QWORDPTR_STACK_POP'] * 0x10, ['QWORDPTR_STACK_POP'] * 0x10, ['QWORDPTR_STACK_POP'] * 0x10, ['QWORDPTR_STACK_POP'] * 0x10, is64=True, rex=rex)
                    continue
                elif 0x9c == opcodeByte:
                    # PUSHF
                    self.setOpcodeEffect(opcode_bytes, 'DWORDPTR_STACK_PUSH', 'WORDPTR_STACK_PUSH', 'DWORDPTR_STACK_PUSH', 'WORDPTR_STACK_PUSH')
                    for rex in range(0x10):
                        self.setOpcodeEffect(opcode_bytes, ['QWORDPTR_STACK_PUSH'] * 0x10, ['WORDPTR_STACK_PUSH'] * 0x10, ['QWORDPTR_STACK_PUSH'] * 0x10, ['WORDPTR_STACK_PUSH'] * 0x10, is64=True, rex=rex)
                    continue
                elif 0x9d == opcodeByte:
                    # POPF
                    self.setOpcodeEffect(opcode_bytes, 'DWORDPTR_STACK_POP', 'WORDPTR_STACK_POP', 'DWORDPTR_STACK_POP', 'WORDPTR_STACK_POP')
                    for rex in range(0x10):
                        self.setOpcodeEffect(opcode_bytes, ['QWORDPTR_STACK_POP'] * 0x10, ['WORDPTR_STACK_POP'] * 0x10, ['QWORDPTR_STACK_POP'] * 0x10, ['WORDPTR_STACK_POP'] * 0x10, is64=True, rex=rex)
                    continue
                # MOFFS
                elif 0xa0 == opcodeByte:
                    # mov [abs addr], 8bit
                    self.setOpcodeEffect(opcode_bytes, 'BYTEPTR_DISPLACEMENT32', 'BYTEPTR_DISPLACEMENT32', None, None)
                    for rex in range(0x10):
                        self.setOpcodeEffect(opcode_bytes, ['BYTEPTR_DISPLACEMENT64'] * 0x10, ['BYTEPTR_DISPLACEMENT64'] * 0x10, [None] * 0x10, [None] * 0x10, is64=True, rex=rex)
                    continue
                elif 0xa1 == opcodeByte:
                    # mov [abs addr], full
                    self.setOpcodeEffect(opcode_bytes, 'DWORDPTR_DISPLACEMENT32', 'WORDPTR_DISPLACEMENT32', None, None)
                    for rex in range(0x8):
                        self.setOpcodeEffect(opcode_bytes, ['DWORDPTR_DISPLACEMENT64'] * 0x10, ['WORDPTR_DISPLACEMENT64'] * 0x10, [None] * 0x10, [None] * 0x10, is64=True, rex=rex)
                    for rex in range(0x8, 0x10):
                        self.setOpcodeEffect(opcode_bytes, ['QWORDPTR_DISPLACEMENT64'] * 0x10, ['BYTEPTR_DISPLACEMENT64'] * 0x10, [None] * 0x10, [None] * 0x10, is64=True, rex=rex)
                    continue
                elif 0xa2 == opcodeByte:
                    # mov [abs addr], 8bit
                    self.setOpcodeEffect(opcode_bytes, 'BYTEPTR_DISPLACEMENT32', 'BYTEPTR_DISPLACEMENT32', None, None)
                    for rex in range(0x10):
                        self.setOpcodeEffect(opcode_bytes, ['BYTEPTR_DISPLACEMENT64'] * 0x10, ['BYTEPTR_DISPLACEMENT64'] * 0x10, [None] * 0x10, [None] * 0x10, is64=True, rex=rex)
                    continue
                elif 0xa3 == opcodeByte:
                    # mov [abs addr], full
                    self.setOpcodeEffect(opcode_bytes, 'DWORDPTR_DISPLACEMENT32', 'WORDPTR_DISPLACEMENT32', None, None)
                    for rex in range(0x8):
                        self.setOpcodeEffect(opcode_bytes, ['DWORDPTR_DISPLACEMENT64'] * 0x10, ['WORDPTR_DISPLACEMENT64'] * 0x10, [None] * 0x10, [None] * 0x10, is64=True, rex=rex)
                    for rex in range(0x8, 0x10):
                        self.setOpcodeEffect(opcode_bytes, ['QWORDPTR_DISPLACEMENT64'] * 0x10, ['BYTEPTR_DISPLACEMENT64'] * 0x10, [None] * 0x10, [None] * 0x10, is64=True, rex=rex)
                    continue
                elif 0xa4 == opcodeByte:
                    # MOVSB
                    self.setOpcodeEffect(opcode_bytes, 'BYTEPTR_EDI_PTR2_ESI', 'BYTEPTR_EDI_PTR2_ESI', 'BYTEPTR_DI_PTR2_SI', 'BYTEPTR_DI_PTR2_SI')
                    # TODO: Recheck the sizes of the regs
                    for rex in range(0x10):
                        self.setOpcodeEffect(opcode_bytes, ['BYTEPTR_RDI_PTR2_RSI'] * 0x10, ['BYTEPTR_RDI_PTR2_RSI'] * 0x10, ['BYTEPTR_DI_PTR2_SI'] * 0x10, ['BYTEPTR_DI_PTR2_SI'] * 0x10, is64=True, rex=rex)
                    continue
                elif 0xa5 == opcodeByte:
                    # MOVSD / MOVSW
                    self.setOpcodeEffect(opcode_bytes, 'DWORDPTR_EDI_PTR2_ESI', 'WORDPTR_EDI_PTR2_ESI', 'DWORDPTR_DI_PTR2_SI', 'WORDPTR_DI_PTR2_SI')
                    # TODO: Recheck the sizes of the regs
                    for rex in range(0x10):
                        self.setOpcodeEffect(opcode_bytes, ['DWORDPTR_RDI_PTR2_RSI'] * 0x10, ['WORDPTR_RDI_PTR2_RSI'] * 0x10, ['DWORDPTR_DI_PTR2_SI'] * 0x10, ['WORDPTR_DI_PTR2_SI'] * 0x10, is64=True, rex=rex)
                    continue
                elif 0xa6 == opcodeByte:
                    # CMPSB
                    self.setOpcodeEffect(opcode_bytes, 'BYTEPTR_EDI_PTR2_ESI', 'BYTEPTR_EDI_PTR2_ESI', 'BYTEPTR_DI_PTR2_SI', 'BYTEPTR_DI_PTR2_SI')
                    # TODO: Recheck the sizes of the regs
                    for rex in range(0x10):
                        self.setOpcodeEffect(opcode_bytes, ['BYTEPTR_RDI_PTR2_RSI'] * 0x10, ['BYTEPTR_RDI_PTR2_RSI'] * 0x10, ['BYTEPTR_DI_PTR2_SI'] * 0x10, ['BYTEPTR_DI_PTR2_SI'] * 0x10, is64=True, rex=rex)
                    continue
                elif 0xa7 == opcodeByte:
                    # CMPSD / CMPSW
                    self.setOpcodeEffect(opcode_bytes, 'DWORDPTR_EDI_PTR2_ESI', 'WORDPTR_EDI_PTR2_ESI', 'DWORDPTR_DI_PTR2_SI', 'WORDPTR_DI_PTR2_SI')
                    # TODO: Recheck the sizes of the regs
                    for rex in range(0x10):
                        self.setOpcodeEffect(opcode_bytes, ['DWORDPTR_RDI_PTR2_RSI'] * 0x10, ['WORDPTR_RDI_PTR2_RSI'] * 0x10, ['DWORDPTR_DI_PTR2_SI'] * 0x10, ['WORDPTR_DI_PTR2_SI'] * 0x10, is64=True, rex=rex)
                    continue
                elif 0xaa == opcodeByte:
                    # STOSB
                    self.setOpcodeEffect(opcode_bytes, 'BYTEPTR_EDI', 'BYTEPTR_EDI', 'BYTEPTR_DI', 'BYTEPTR_DI')
                    # TODO: Recheck the sizes of the regs
                    for rex in range(0x10):
                        self.setOpcodeEffect(opcode_bytes, ['BYTEPTR_RDI'] * 0x10, ['BYTEPTR_RDI'] * 0x10, ['BYTEPTR_DI'] * 0x10, ['BYTEPTR_DI'] * 0x10, is64=True, rex=rex)
                    continue
                elif 0xab == opcodeByte:
                    # STOSD / STOSW
                    self.setOpcodeEffect(opcode_bytes, 'DWORDPTR_EDI', 'WORDPTR_EDI', 'DWORDPTR_DI', 'WORDPTR_DI')
                    # TODO: Recheck the sizes of the regs
                    for rex in range(0x10):
                        self.setOpcodeEffect(opcode_bytes, ['DWORDPTR_RDI'] * 0x10, ['WORDPTR_RDI'] * 0x10, ['DWORDPTR_DI'] * 0x10, ['WORDPTR_DI'] * 0x10, is64=True, rex=rex)
                    continue
                elif 0xac == opcodeByte:
                    # LODSB
                    self.setOpcodeEffect(opcode_bytes, 'BYTEPTR_ESI', 'BYTEPTR_ESI', 'BYTEPTR_SI', 'BYTEPTR_SI')
                    # TODO: Recheck the sizes of the regs
                    for rex in range(0x10):
                        self.setOpcodeEffect(opcode_bytes, ['BYTEPTR_RSI'] * 0x10, ['BYTEPTR_RSI'] * 0x10, ['BYTEPTR_SI'] * 0x10, ['BYTEPTR_SI'] * 0x10, is64=True, rex=rex)
                    continue
                elif 0xad == opcodeByte:
                    # LODSD / LODSW
                    self.setOpcodeEffect(opcode_bytes, 'DWORDPTR_ESI', 'WORDPTR_ESI', 'DWORDPTR_SI', 'WORDPTR_SI')
                    # TODO: Recheck the sizes of the regs
                    for rex in range(0x10):
                        self.setOpcodeEffect(opcode_bytes, ['DWORDPTR_RSI'] * 0x10, ['WORDPTR_RSI'] * 0x10, ['DWORDPTR_SI'] * 0x10, ['WORDPTR_SI'] * 0x10, is64=True, rex=rex)
                    continue
                elif 0xae == opcodeByte:
                    # SCASB
                    self.setOpcodeEffect(opcode_bytes, 'BYTEPTR_EDI', 'BYTEPTR_EDI', 'BYTEPTR_DI', 'BYTEPTR_DI')
                    # TODO: Recheck the sizes of the regs
                    for rex in range(0x10):
                        self.setOpcodeEffect(opcode_bytes, ['BYTEPTR_RDI'] * 0x10, ['BYTEPTR_RDI'] * 0x10, ['BYTEPTR_DI'] * 0x10, ['BYTEPTR_DI'] * 0x10, is64=True, rex=rex)
                    continue
                elif 0xaf == opcodeByte:
                    # SCASD / SCASW
                    self.setOpcodeEffect(opcode_bytes, 'DWORDPTR_EDI', 'WORDPTR_EDI', 'DWORDPTR_DI', 'WORDPTR_DI')
                    # TODO: Recheck the sizes of the regs
                    for rex in range(0x10):
                        self.setOpcodeEffect(opcode_bytes, ['QWORDPTR_EDI'] * 0x10, ['WORDPTR_EDI'] * 0x10, ['QWORDPTR_DI'] * 0x10, ['WORDPTR_DI'] * 0x10, is64=True, rex=rex)
                    continue
                elif 0x8d == opcodeByte:
                    # LEA
                    continue
                elif 0x62 == opcodeByte:
                    # BOUND
                    continue
                elif 0x63 == opcodeByte:
                    # ARPL
                    continue

                # TODO: 0xff is also call, need to add it

                route = [opcodeByte]
            
            elif OpcodeLength.OL_2 == opcode_length:
                self.buildEmptyBlock(self.t32, opcode_bytes[:1])
                route = opcode_bytes[:2]
                if 0x0f == opcode_bytes[0]:
                    if 0x34 == opcode_bytes[1]:
                        # SYSENTER
                        for prefixFlags in range(4):
                            self.writeToTable(self.t32, [prefixFlags] + route, 'SYSENTER')
                            for rex in range(0x10):
                                self.writeToTable(self.t64, [prefixFlags, rex] + route, 'SYSENTER')
                        continue

            elif OpcodeLength.OL_3 == opcode_length:
                self.buildEmptyBlock(self.t32, opcode_bytes[:2])
                route = opcode_bytes[:]
            elif OpcodeLength.OL_4 == opcode_length:
                self.buildEmptyBlock(self.t32, opcode_bytes[:3])
                route = opcode_bytes[:]

            elif OpcodeLength.OL_1d == opcode_length:
                if 0x40 < opcode_bytes[-1]:
                    continue
                self.buildEmptyBlock(self.t32, opcode_bytes[:1])
                route = [opcode_bytes[0]]
                mask = 0x38
                maskTarget = opcode_bytes[-1] << 3
            elif OpcodeLength.OL_2d == opcode_length:
                # Only opcodes I don't care about
                continue

            elif OpcodeLength.OL_13 == opcode_length:
                route = opcode_bytes[:1]
                mask = 0x38
                maskTarget = opcode_bytes[-1] << 3
            elif OpcodeLength.OL_23 == opcode_length:
                self.buildEmptyBlock(self.t32, opcode_bytes[:1])
                route = opcode_bytes[:2]
                mask = 0x38
                maskTarget = opcode_bytes[-1] << 3
            elif OpcodeLength.OL_33 == OpcodeLength:
                self.buildEmptyBlock(self.t32, opcode_bytes[:2])
                route = opcode_bytes[:3]
                mask = 0x38
                maskTarget = opcode_bytes[-1] << 3

            if      (OperandType.RM8 in operand_type) and \
                    (OperandType.REG8 in operand_type) and \
                    (0 != (inst_flags & InstFlag.INCLUDE_MODRM)):

                self.setMaskedOpcodeEffect(route, mask, maskTarget, self.rm8Effects, self.rm8Effects, self.rm8PfEffects, self.rm8PfEffects)
                if 0 == (inst_flags & InstFlag.INVALID_64BITS):
                    for rex in range(0x10):
                        self.setMaskedOpcodeEffect(
                                route, 
                                mask, maskTarget, 
                                self.rm8On64Effects, 
                                self.rm8On64Effects, 
                                self.rm8On64PfEffects, 
                                self.rm8On64PfEffects, 
                                is64=True, 
                                rex=rex)

            elif    (   (OperandType.RM16 in operand_type) or
                        (OperandType.RFULL_M16 in operand_type) or
                        (OperandType.REG_FULL in operand_type) ) and \
                    (   (OperandType.REG16 in operand_type) or \
                        (OperandType.SREG in operand_type) or
                        (OperandType.MEM16_FULL in operand_type) ) and \
                    (0 != (inst_flags & InstFlag.INCLUDE_MODRM)):

                self.setMaskedOpcodeEffect(
                        route, 
                        mask, 
                        maskTarget, 
                        self.rm16Effects, 
                        self.rm16Effects, 
                        self.rm16PfEffects, 
                        self.rm16PfEffects)
                if 0 == (inst_flags & InstFlag.INVALID_64BITS):
                    for rex in range(0x10):
                        self.setMaskedOpcodeEffect(
                                route, 
                                mask, 
                                maskTarget, 
                                self.rm16On64Effects, 
                                self.rm16On64Effects, 
                                self.rm16On64PfEffects, 
                                self.rm16On64PfEffects, 
                                is64=True, 
                                rex=rex)

            # MODRM 0xc0 is invalid for OperandType.MEM / OperandType.MEM16_3264, but fuck it!
            elif (   (OperandType.MEM in operand_type) or \
                     (OperandType.MEM16_3264 in operand_type) or \
                     (OperandType.RM32 in operand_type) or \
                     (OperandType.RM32_64 in operand_type) or \
                     (OperandType.RM_FULL in operand_type) ) and \
                 (  (OperandType.REG32 in operand_type) or \
                    (OperandType.REG32_64 in operand_type) or \
                    (OperandType.REG_FULL in operand_type) ) and \
                     (0 != (inst_flags & InstFlag.INCLUDE_MODRM)):

                self.setMaskedOpcodeEffect(route, mask, maskTarget, self.rm32Effects, self.rm16Effects, self.rm32PfEffects, self.rm16PfEffects)
                if 0 == (inst_flags & InstFlag.INVALID_64BITS):
                    for rex in range(0x10):
                        self.setMaskedOpcodeEffect(
                                route, 
                                mask, 
                                maskTarget, 
                                self.rm64Effects, 
                                self.rm32On64Effects, 
                                self.rm64PfEffects, 
                                self.rm32On64PfEffects, 
                                is64=True,
                                rex=rex)

            elif    (OperandType.RM8 in operand_type) and \
                    (0 != (inst_flags & InstFlag.INCLUDE_MODRM)):

                self.setMaskedOpcodeEffect( 
                        route, 
                        mask, 
                        maskTarget, 
                        self.oo8Effects, 
                        self.oo8Effects, 
                        self.oo8PfEffects, 
                        self.oo8PfEffects )
                if 0 == (inst_flags & InstFlag.INVALID_64BITS):
                    for rex in range(0x10):
                        self.setMaskedOpcodeEffect(
                                route, 
                                mask, 
                                maskTarget, 
                                self.oo8On64Effects, 
                                self.oo8On64Effects, 
                                self.oo8On64PfEffects, 
                                self.oo8On64PfEffects, 
                                is64=True,
                                rex=rex)
            
            elif    (OperandType.RM16 in operand_type) and \
                    (0 != (inst_flags & InstFlag.INCLUDE_MODRM)):

                self.setMaskedOpcodeEffect( 
                        route, 
                        mask, 
                        maskTarget, 
                        self.oo16Effects, 
                        self.oo16Effects, 
                        self.oo16PfEffects, 
                        self.oo16PfEffects )
                if 0 == (inst_flags & InstFlag.INVALID_64BITS):
                    for rex in range(0x10):
                        self.setMaskedOpcodeEffect( 
                                route, 
                                mask, maskTarget, 
                                self.oo16On64Effects, 
                                self.oo16On64Effects, 
                                self.oo16On64PfEffects, 
                                self.oo16On64PfEffects, 
                                is64=True,
                                rex=rex)

            elif (   (OperandType.RM32 in operand_type) or \
                     (OperandType.RM32_64 in operand_type) or \
                     (OperandType.RM_FULL in operand_type) ) and \
                    (0 != (inst_flags & InstFlag.INCLUDE_MODRM)):

                self.setMaskedOpcodeEffect( 
                        route, 
                        mask, 
                        maskTarget, 
                        self.oo32Effects, 
                        self.oo16Effects, 
                        self.oo32PfEffects, 
                        self.oo16PfEffects )
                if 0 == (inst_flags & InstFlag.INVALID_64BITS):
                    for rex in range(0x10):
                        self.setMaskedOpcodeEffect( 
                                route, 
                                mask, 
                                maskTarget, 
                                self.oo64Effects, 
                                self.oo32On64Effects, 
                                self.oo64PfEffects, 
                                self.oo32On64PfEffects, 
                                is64=True,
                                rex=rex)

        # Overwrite for Nops
        for prefixFlags in range(4):
            self.t32[prefixFlags][0x90] = None
            self.t32[prefixFlags][0x8b][0xff] = None
            for rex in range(0x10):
                self.t64[prefixFlags][rex][0x90] = None
                self.t64[prefixFlags][rex][0x8b][0xff] = None

        # Add ignored prefiex
        IGNORED_PREFIXES = [0xf0, 0xf2, 0xf3]   # LOCK, REP, REPNZ
        for prefix in IGNORED_PREFIXES:
            for prefixFlags in range(4):
                self.t32[prefixFlags][prefix] = 'CONTINUE'
                for rex in range(0x10):
                    self.t64[prefixFlags][rex][prefix] = 'CONTINUE'

        # Combine tables
        self.fullTable32 = copy.deepcopy(self.t32[0])
        self.fullTable32[0x66] = copy.deepcopy(self.t32[1])
        self.fullTable32[0x66][0x66] = None
        self.fullTable32[0x67] = copy.deepcopy(self.t32[2])
        self.fullTable32[0x67][0x67] = None
        self.fullTable32[0x66][0x67] = copy.deepcopy(self.t32[3])
        self.fullTable32[0x67][0x66] = copy.deepcopy(self.t32[3])
        self.fullTable32[0x66][0x67][0x66] = None
        self.fullTable32[0x66][0x67][0x67] = None
        self.fullTable64 = copy.deepcopy(self.t64[0][0])
        self.fullTable64[0x66] = copy.deepcopy(self.t64[1][0])
        self.fullTable64[0x66][0x66] = None
        self.fullTable64[0x67] = copy.deepcopy(self.t64[2][0])
        self.fullTable64[0x67][0x67] = None
        self.fullTable64[0x66][0x67] = copy.deepcopy(self.t64[3][0])
        self.fullTable64[0x67][0x66] = copy.deepcopy(self.t64[3][0])
        self.fullTable64[0x66][0x67][0x66] = None
        self.fullTable64[0x66][0x67][0x67] = None
        for rex in range(0x10):
            self.fullTable64[0x40 + rex] = copy.deepcopy(self.t64[0][rex])
            self.fullTable64[0x40 + rex][0x66] = copy.deepcopy(self.t64[1][rex])
            self.fullTable64[0x40 + rex][0x66][0x66] = None
            self.fullTable64[0x40 + rex][0x67] = copy.deepcopy(self.t64[2][rex])
            self.fullTable64[0x40 + rex][0x67][0x67] = None
            self.fullTable64[0x40 + rex][0x66][0x67] = copy.deepcopy(self.t64[3][rex])
            self.fullTable64[0x40 + rex][0x67][0x66] = copy.deepcopy(self.t64[3][rex])
            self.fullTable64[0x40 + rex][0x66][0x67][0x66] = None
            self.fullTable64[0x40 + rex][0x66][0x67][0x67] = None
            self.fullTable64[0x66][0x40 + rex] = copy.deepcopy(self.t64[1][rex])
            self.fullTable64[0x67][0x40 + rex] = copy.deepcopy(self.t64[2][rex])
            self.fullTable64[0x66][0x67][0x40 + rex] = copy.deepcopy(self.t64[3][rex])
            self.fullTable64[0x67][0x66][0x40 + rex] = copy.deepcopy(self.t64[3][rex])
        self.fullTable64[0x66][0x66] = None
        self.fullTable64[0x67][0x67] = None
        self.fullTable64[0x66][0x67][0x66] = None
        self.fullTable64[0x66][0x67][0x67] = None

    def buildRMTable(self):
        self.rm8Effects = [None] * 0x100
        self.rm8PfEffects = [None] * 0x100
        self.rm16Effects = [None] * 0x100
        self.rm16PfEffects = [None] * 0x100
        self.rm32Effects = [None] * 0x100
        self.rm32PfEffects = [None] * 0x100
        self.rm8On64Effects = self._makeArray([0x10, 0x100])
        self.rm8On64PfEffects = self._makeArray([0x10, 0x100])
        self.rm16On64Effects = self._makeArray([0x10, 0x100])
        self.rm16On64PfEffects = self._makeArray([0x10, 0x100])
        self.rm32On64Effects = self._makeArray([0x10, 0x100])
        self.rm32On64PfEffects = self._makeArray([0x10, 0x100])
        self.rm64Effects = self._makeArray([0x10, 0x100])
        self.rm64PfEffects = self._makeArray([0x10, 0x100])
        # Need to handle the REX extention 15 combinations
        for dst in range(8):
            for src in range(8):
                src_dst = (src << 3) + dst
                self.rm8Effects     [src_dst]  = 'BYTEPTR_'  + self.REGS32_IDS[dst]
                self.rm8PfEffects   [src_dst]  = 'BYTEPTR_'  + self.DISP16_IDS[dst]
                self.rm16Effects    [src_dst]  = 'WORDPTR_'  + self.REGS32_IDS[dst]
                self.rm16PfEffects  [src_dst]  = 'WORDPTR_'  + self.DISP16_IDS[dst]
                self.rm32Effects    [src_dst]  = 'DWORDPTR_' + self.REGS32_IDS[dst]
                self.rm32PfEffects  [src_dst]  = 'DWORDPTR_' + self.DISP16_IDS[dst]
                for rex in range(0x10):
                    self.rm8On64Effects    [rex][src_dst] = 'BYTEPTR_'  + self.REGS64_IDS[dst]
                    self.rm16On64Effects   [rex][src_dst] = 'WORDPTR_'  + self.REGS64_IDS[dst]
                    self.rm32On64Effects   [rex][src_dst] = 'DWORDPTR_' + self.REGS64_IDS[dst]
                    self.rm8On64PfEffects  [rex][src_dst] = 'BYTEPTR_'  + self.REGS32_IDS[dst]
                    self.rm16On64PfEffects [rex][src_dst] = 'WORDPTR_'  + self.REGS32_IDS[dst]
                    self.rm32On64PfEffects [rex][src_dst] = 'DWORDPTR_' + self.REGS32_IDS[dst]
                    if rex & 8:
                        self.rm64Effects   [rex][src_dst] = 'QWORDPTR_' + self.REGS64_IDS[dst]
                        self.rm64PfEffects [rex][src_dst] = 'QWORDPTR_' + self.REGS32_IDS[dst]
                    else:
                        self.rm64Effects   [rex][src_dst] = 'DWORDPTR_' + self.REGS64_IDS[dst]
                        self.rm64PfEffects [rex][src_dst] = 'DWORDPTR_' + self.REGS32_IDS[dst]
                
                # Overwrite for no register flag
                if 0x05 == dst:
                    self.rm8Effects           [src_dst]  = 'BYTEPTR_'      + 'DISPLACEMENT32'
                    self.rm16Effects          [src_dst]  = 'WORDPTR_'      + 'DISPLACEMENT32'
                    self.rm32Effects          [src_dst]  = 'DWORDPTR_'     + 'DISPLACEMENT32'
                    for rex in range(0x10):
                        self.rm8On64Effects   [rex][src_dst] = 'BYTEPTR_'  + 'DISPLACEMENT32_' + 'RIP'
                        self.rm16On64Effects  [rex][src_dst] = 'WORDPTR_'  + 'DISPLACEMENT32_' + 'RIP'
                        self.rm32On64Effects  [rex][src_dst] = 'DWORDPTR_' + 'DISPLACEMENT32_' + 'RIP'
                        self.rm8On64PfEffects [rex][src_dst] = 'BYTEPTR_'  + 'DISPLACEMENT32_' + 'RIP'
                        self.rm16On64PfEffects[rex][src_dst] = 'WORDPTR_'  + 'DISPLACEMENT32_' + 'RIP'
                        self.rm32On64PfEffects[rex][src_dst] = 'DWORDPTR_' + 'DISPLACEMENT32_' + 'RIP'
                        if rex & 8:
                            self.rm64Effects  [rex][src_dst]  = 'QWORDPTR_' + 'DISPLACEMENT32_' + 'RIP'
                        else:
                            self.rm64Effects  [rex][src_dst]  = 'DWORDPTR_' + 'DISPLACEMENT32_' + 'RIP'
                elif 0x06 == dst:
                    # Only displacement is not supported
                    self.rm8PfEffects   [src_dst]  = '' # 'BYTEPTR_'  + 'DISPLACEMENT16'
                    self.rm16PfEffects  [src_dst]  = '' # 'WORDPTR_'  + 'DISPLACEMENT16'
                    self.rm32PfEffects  [src_dst]  = '' # 'DWORDPTR_' + 'DISPLACEMENT16'
                    # 64 bit is not effected by this

                # Not SIB
                self.rm8Effects         [0x40 + src_dst]   = 'BYTEPTR_DISPLACEMENT8_'   + self.REGS32_IDS[dst]
                self.rm8Effects         [0x80 + src_dst]   = 'BYTEPTR_DISPLACEMENT32_'  + self.REGS32_IDS[dst]
                self.rm8PfEffects       [0x40 + src_dst]   = 'BYTEPTR_DISPLACEMENT8_'   + self.DISP16_IDS[dst]
                self.rm8PfEffects       [0x80 + src_dst]   = 'BYTEPTR_DISPLACEMENT16_'  + self.DISP16_IDS[dst]
                self.rm16Effects        [0x40 + src_dst]   = 'WORDPTR_DISPLACEMENT8_'   + self.REGS32_IDS[dst]
                self.rm16Effects        [0x80 + src_dst]   = 'WORDPTR_DISPLACEMENT32_'  + self.REGS32_IDS[dst]
                self.rm16PfEffects      [0x40 + src_dst]   = 'WORDPTR_DISPLACEMENT8_'   + self.DISP16_IDS[dst]
                self.rm16PfEffects      [0x80 + src_dst]   = 'WORDPTR_DISPLACEMENT16_'  + self.DISP16_IDS[dst]
                self.rm32Effects        [0x40 + src_dst]   = 'DWORDPTR_DISPLACEMENT8_'  + self.REGS32_IDS[dst]
                self.rm32Effects        [0x80 + src_dst]   = 'DWORDPTR_DISPLACEMENT32_' + self.REGS32_IDS[dst]
                self.rm32PfEffects      [0x40 + src_dst]   = 'DWORDPTR_DISPLACEMENT8_'  + self.DISP16_IDS[dst]
                self.rm32PfEffects      [0x80 + src_dst]   = 'DWORDPTR_DISPLACEMENT16_' + self.DISP16_IDS[dst]
                for rex in range(0x10):
                    self.rm8On64Effects    [rex][0x40 + src_dst] = 'BYTEPTR_DISPLACEMENT8_'   + self.REGS64_IDS[dst]
                    self.rm8On64Effects    [rex][0x80 + src_dst] = 'BYTEPTR_DISPLACEMENT32_'  + self.REGS64_IDS[dst]
                    self.rm16On64Effects   [rex][0x40 + src_dst] = 'WORDPTR_DISPLACEMENT8_'   + self.REGS64_IDS[dst]
                    self.rm16On64Effects   [rex][0x80 + src_dst] = 'WORDPTR_DISPLACEMENT32_'  + self.REGS64_IDS[dst]
                    self.rm32On64Effects   [rex][0x40 + src_dst] = 'DWORDPTR_DISPLACEMENT8_'  + self.REGS64_IDS[dst]
                    self.rm32On64Effects   [rex][0x80 + src_dst] = 'DWORDPTR_DISPLACEMENT32_' + self.REGS64_IDS[dst]
                    self.rm8On64PfEffects  [rex][0x40 + src_dst] = 'BYTEPTR_DISPLACEMENT8_'   + self.REGS32_IDS[dst]
                    self.rm8On64PfEffects  [rex][0x80 + src_dst] = 'BYTEPTR_DISPLACEMENT32_'  + self.REGS32_IDS[dst]
                    self.rm16On64PfEffects [rex][0x40 + src_dst] = 'WORDPTR_DISPLACEMENT8_'   + self.REGS32_IDS[dst]
                    self.rm16On64PfEffects [rex][0x80 + src_dst] = 'WORDPTR_DISPLACEMENT32_'  + self.REGS32_IDS[dst]
                    self.rm32On64PfEffects [rex][0x40 + src_dst] = 'DWORDPTR_DISPLACEMENT8_'  + self.REGS32_IDS[dst]
                    self.rm32On64PfEffects [rex][0x80 + src_dst] = 'DWORDPTR_DISPLACEMENT32_' + self.REGS32_IDS[dst]
                    if rex & 8:
                        self.rm64Effects    [rex][0x40 + src_dst] = 'QWORDPTR_DISPLACEMENT8_'  + self.REGS64_IDS[dst]
                        self.rm64Effects    [rex][0x80 + src_dst] = 'QWORDPTR_DISPLACEMENT32_' + self.REGS64_IDS[dst]
                        self.rm64PfEffects  [rex][0x40 + src_dst] = 'QWORDPTR_DISPLACEMENT8_'  + self.REGS32_IDS[dst]
                        self.rm64PfEffects  [rex][0x80 + src_dst] = 'QWORDPTR_DISPLACEMENT32_' + self.REGS32_IDS[dst]
                    else:
                        self.rm64Effects    [rex][0x40 + src_dst] = 'DWORDPTR_DISPLACEMENT8_'  + self.REGS64_IDS[dst]
                        self.rm64Effects    [rex][0x80 + src_dst] = 'DWORDPTR_DISPLACEMENT32_' + self.REGS64_IDS[dst]
                        self.rm64PfEffects  [rex][0x40 + src_dst] = 'DWORDPTR_DISPLACEMENT8_'  + self.REGS32_IDS[dst]
                        self.rm64PfEffects  [rex][0x80 + src_dst] = 'DWORDPTR_DISPLACEMENT32_' + self.REGS32_IDS[dst]

                # Overwrite for SIB
                if 0x04 == dst:
                    # Overwrite the No Displacement
                    # In 32bit the size prefix cancel the SIB, while in 64bit it cut it down to 32bit
                    self.rm8Effects           [src_dst]          = self.getSibEffectsTable('BYTEPTR_', modBits=0)
                    self.rm16Effects          [src_dst]          = self.getSibEffectsTable('WORDPTR_', modBits=0)
                    self.rm32Effects          [src_dst]          = self.getSibEffectsTable('DWORDPTR_', modBits=0)

                    self.rm8Effects           [0x40 + src_dst]   = self.getSibEffectsTable('BYTEPTR_', modBits=1)
                    self.rm8Effects           [0x80 + src_dst]   = self.getSibEffectsTable('BYTEPTR_', modBits=2)
                    self.rm16Effects          [0x40 + src_dst]   = self.getSibEffectsTable('WORDPTR_', modBits=1)
                    self.rm16Effects          [0x80 + src_dst]   = self.getSibEffectsTable('WORDPTR_', modBits=2)
                    self.rm32Effects          [0x40 + src_dst]   = self.getSibEffectsTable('DWORDPTR_', modBits=1)
                    self.rm32Effects          [0x80 + src_dst]   = self.getSibEffectsTable('DWORDPTR_', modBits=2)
                    for rex in range(0x10):
                        self.rm8On64Effects   [rex][src_dst]        = self.getSib64EffectsTable('BYTEPTR_', rex=(rex & 3), modBits=0)
                        self.rm8On64Effects   [rex][0x40 + src_dst] = self.getSib64EffectsTable('BYTEPTR_', rex=(rex & 3), modBits=1)
                        self.rm8On64Effects   [rex][0x80 + src_dst] = self.getSib64EffectsTable('BYTEPTR_', rex=(rex & 3), modBits=2)
                        self.rm16On64Effects  [rex][src_dst]        = self.getSib64EffectsTable('WORDPTR_', rex=(rex & 3), modBits=0)
                        self.rm16On64Effects  [rex][0x40 + src_dst] = self.getSib64EffectsTable('WORDPTR_', rex=(rex & 3), modBits=1)
                        self.rm16On64Effects  [rex][0x80 + src_dst] = self.getSib64EffectsTable('WORDPTR_', rex=(rex & 3), modBits=2)
                        self.rm32On64Effects  [rex][src_dst]        = self.getSib64EffectsTable('DWORDPTR_', rex=(rex & 3), modBits=0)
                        self.rm32On64Effects  [rex][0x40 + src_dst] = self.getSib64EffectsTable('DWORDPTR_', rex=(rex & 3), modBits=1)
                        self.rm32On64Effects  [rex][0x80 + src_dst] = self.getSib64EffectsTable('DWORDPTR_', rex=(rex & 3), modBits=2)
                        self.rm8On64PfEffects [rex][src_dst]        = self.getSib64EffectsTable('BYTEPTR_', rex=(rex & 3), modBits=0, sizePrefix=True)
                        self.rm8On64PfEffects [rex][0x40 + src_dst] = self.getSib64EffectsTable('BYTEPTR_', rex=(rex & 3), modBits=1, sizePrefix=True)
                        self.rm8On64PfEffects [rex][0x80 + src_dst] = self.getSib64EffectsTable('BYTEPTR_', rex=(rex & 3), modBits=2, sizePrefix=True)
                        self.rm16On64PfEffects[rex][src_dst]        = self.getSib64EffectsTable('WORDPTR_', rex=(rex & 3), modBits=0, sizePrefix=True)
                        self.rm16On64PfEffects[rex][0x40 + src_dst] = self.getSib64EffectsTable('WORDPTR_', rex=(rex & 3), modBits=1, sizePrefix=True)
                        self.rm16On64PfEffects[rex][0x80 + src_dst] = self.getSib64EffectsTable('WORDPTR_', rex=(rex & 3), modBits=2, sizePrefix=True)
                        self.rm32On64PfEffects[rex][src_dst]        = self.getSib64EffectsTable('DWORDPTR_', rex=(rex & 3), modBits=0, sizePrefix=True)
                        self.rm32On64PfEffects[rex][0x40 + src_dst] = self.getSib64EffectsTable('DWORDPTR_', rex=(rex & 3), modBits=1, sizePrefix=True)
                        self.rm32On64PfEffects[rex][0x80 + src_dst] = self.getSib64EffectsTable('DWORDPTR_', rex=(rex & 3), modBits=2, sizePrefix=True)
                        if rex & 8:
                            self.rm64Effects  [rex][src_dst]          = self.getSib64EffectsTable('QWORDPTR_', rex=(rex & 3), modBits=0)
                            self.rm64Effects  [rex][0x40 + src_dst]   = self.getSib64EffectsTable('QWORDPTR_', rex=(rex & 3), modBits=1)
                            self.rm64Effects  [rex][0x80 + src_dst]   = self.getSib64EffectsTable('QWORDPTR_', rex=(rex & 3), modBits=2)
                            self.rm64PfEffects[rex][src_dst]          = self.getSib64EffectsTable('QWORDPTR_', rex=(rex & 3), modBits=0, sizePrefix=True)
                            self.rm64PfEffects[rex][0x40 + src_dst]   = self.getSib64EffectsTable('QWORDPTR_', rex=(rex & 3), modBits=1, sizePrefix=True)
                            self.rm64PfEffects[rex][0x80 + src_dst]   = self.getSib64EffectsTable('QWORDPTR_', rex=(rex & 3), modBits=2, sizePrefix=True)
                        else:
                            self.rm64Effects  [rex][src_dst]          = self.getSib64EffectsTable('DWORDPTR_', rex=(rex & 3), modBits=0)
                            self.rm64Effects  [rex][0x40 + src_dst]   = self.getSib64EffectsTable('DWORDPTR_', rex=(rex & 3), modBits=1)
                            self.rm64Effects  [rex][0x80 + src_dst]   = self.getSib64EffectsTable('DWORDPTR_', rex=(rex & 3), modBits=2)
                            self.rm64PfEffects[rex][src_dst]          = self.getSib64EffectsTable('DWORDPTR_', rex=(rex & 3), modBits=0, sizePrefix=True)
                            self.rm64PfEffects[rex][0x40 + src_dst]   = self.getSib64EffectsTable('DWORDPTR_', rex=(rex & 3), modBits=1, sizePrefix=True)
                            self.rm64PfEffects[rex][0x80 + src_dst]   = self.getSib64EffectsTable('DWORDPTR_', rex=(rex & 3), modBits=2, sizePrefix=True)
            
    def buildOOTable(self):
        self.oo8Effects        = [None] * 0x100
        self.oo8PfEffects      = [None] * 0x100
        self.oo16Effects       = [None] * 0x100
        self.oo16PfEffects     = [None] * 0x100
        self.oo32Effects       = [None] * 0x100
        self.oo32PfEffects     = [None] * 0x100
        self.oo8On64Effects    = self._makeArray([0x10, 0x100])
        self.oo8On64PfEffects  = self._makeArray([0x10, 0x100])
        self.oo16On64Effects   = self._makeArray([0x10, 0x100])
        self.oo16On64PfEffects = self._makeArray([0x10, 0x100])
        self.oo32On64Effects   = self._makeArray([0x10, 0x100])
        self.oo32On64PfEffects = self._makeArray([0x10, 0x100])
        self.oo64Effects       = self._makeArray([0x10, 0x100])
        self.oo64PfEffects     = self._makeArray([0x10, 0x100])
        for dst in range(8):
            for opc in range(8):
                opc_dst = (opc << 3) + dst
                self.oo8Effects         [opc_dst]  = 'BYTEPTR_' +  self.REGS32_IDS[dst]
                self.oo8PfEffects       [opc_dst]  = 'BYTEPTR_' +  self.DISP16_IDS[dst]
                self.oo16Effects        [opc_dst]  = 'WORDPTR_' +  self.REGS32_IDS[dst]
                self.oo16PfEffects      [opc_dst]  = 'WORDPTR_' +  self.DISP16_IDS[dst]
                self.oo32Effects        [opc_dst]  = 'DWORDPTR_' + self.REGS32_IDS[dst]
                self.oo32PfEffects      [opc_dst]  = 'DWORDPTR_' + self.DISP16_IDS[dst]
                for rex in range(0x10):
                    self.oo8On64Effects    [rex][opc_dst]  = 'BYTEPTR_' +  self.REGS64_IDS[dst]
                    self.oo8On64PfEffects  [rex][opc_dst]  = 'BYTEPTR_' +  self.REGS32_IDS[dst]
                    self.oo16On64Effects   [rex][opc_dst]  = 'WORDPTR_' +  self.REGS64_IDS[dst]
                    self.oo16On64PfEffects [rex][opc_dst]  = 'WORDPTR_' +  self.REGS32_IDS[dst]
                    self.oo32On64Effects   [rex][opc_dst]  = 'DWORDPTR_' + self.REGS64_IDS[dst]
                    self.oo32On64PfEffects [rex][opc_dst]  = 'DWORDPTR_' + self.REGS32_IDS[dst]
                    if rex & 8:
                        self.oo64Effects    [rex][opc_dst]  = 'QWORDPTR_' + self.REGS64_IDS[dst]
                        self.oo64PfEffects  [rex][opc_dst]  = 'QWORDPTR_' + self.REGS32_IDS[dst]
                    else:
                        self.oo64Effects    [rex][opc_dst]  = 'DWORDPTR_' + self.REGS32_IDS[dst]
                        self.oo64PfEffects  [rex][opc_dst]  = 'DWORDPTR_' + self.REGS32_IDS[dst]
                # Overwrite for no register flag
                if 0x05 == dst:
                    self.oo8Effects         [opc_dst]  = 'BYTEPTR_'      + 'DISPLACEMENT32'
                    self.oo16Effects        [opc_dst]  = 'WORDPTR_'      + 'DISPLACEMENT32'
                    self.oo32Effects        [opc_dst]  = 'DWORDPTR_'     + 'DISPLACEMENT32'
                    for rex in range(0x10):
                        self.oo8On64Effects    [rex][opc_dst]  = 'BYTEPTR_' +  'DISPLACEMENT32_' + 'RIP'
                        self.oo8On64PfEffects  [rex][opc_dst]  = 'BYTEPTR_' +  'DISPLACEMENT32_' + 'RIP'
                        self.oo16On64Effects   [rex][opc_dst]  = 'WORDPTR_' +  'DISPLACEMENT32_' + 'RIP'
                        self.oo16On64PfEffects [rex][opc_dst]  = 'WORDPTR_' +  'DISPLACEMENT32_' + 'RIP'
                        self.oo32On64Effects   [rex][opc_dst]  = 'DWORDPTR_' + 'DISPLACEMENT32_' + 'RIP'
                        self.oo32On64PfEffects [rex][opc_dst]  = 'DWORDPTR_' + 'DISPLACEMENT32_' + 'RIP'
                        if rex & 8:
                            self.oo64Effects [rex][opc_dst]  = 'QWORDPTR_' + 'DISPLACEMENT32_' + 'RIP'
                        else:
                            self.oo64Effects [rex][opc_dst]  = 'DWORDPTR_' + 'DISPLACEMENT32_' + 'RIP'
                elif 0x06 == dst:
                    # Only displacement is not supported
                    self.oo8PfEffects   [opc_dst]  = '' # 'BYTEPTR_' +  'DISPLACEMENT16'
                    self.oo16PfEffects  [opc_dst]  = '' # 'WORDPTR_' +  'DISPLACEMENT16'
                    self.oo32PfEffects  [opc_dst]  = '' # 'DWORDPTR_' + 'DISPLACEMENT16'
                    # 64 bit does not effected by this

                # Not SIB
                self.oo8Effects    [0x40 + opc_dst]   = 'BYTEPTR_DISPLACEMENT8_'   + self.REGS32_IDS[dst]
                self.oo8Effects    [0x80 + opc_dst]   = 'BYTEPTR_DISPLACEMENT32_'  + self.REGS32_IDS[dst]
                self.oo8PfEffects  [0x40 + opc_dst]   = 'BYTEPTR_DISPLACEMENT8_'   + self.DISP16_IDS[dst]
                self.oo8PfEffects  [0x80 + opc_dst]   = 'BYTEPTR_DISPLACEMENT16_'  + self.DISP16_IDS[dst]
                self.oo16Effects   [0x40 + opc_dst]   = 'WORDPTR_DISPLACEMENT8_'   + self.REGS32_IDS[dst]
                self.oo16Effects   [0x80 + opc_dst]   = 'WORDPTR_DISPLACEMENT32_'  + self.REGS32_IDS[dst]
                self.oo16PfEffects [0x40 + opc_dst]   = 'WORDPTR_DISPLACEMENT8_'   + self.DISP16_IDS[dst]
                self.oo16PfEffects [0x80 + opc_dst]   = 'WORDPTR_DISPLACEMENT16_'  + self.DISP16_IDS[dst]
                self.oo32Effects   [0x40 + opc_dst]   = 'DWORDPTR_DISPLACEMENT8_'  + self.REGS32_IDS[dst]
                self.oo32Effects   [0x80 + opc_dst]   = 'DWORDPTR_DISPLACEMENT32_' + self.REGS32_IDS[dst]
                self.oo32PfEffects [0x40 + opc_dst]   = 'DWORDPTR_DISPLACEMENT8_'  + self.DISP16_IDS[dst]
                self.oo32PfEffects [0x80 + opc_dst]   = 'DWORDPTR_DISPLACEMENT16_' + self.DISP16_IDS[dst]
                for rex in range(0x10):
                    self.oo8On64Effects   [rex][0x40 + opc_dst]  = 'BYTEPTR_DISPLACEMENT8_'   + self.REGS32_IDS[dst]
                    self.oo8On64Effects   [rex][0x80 + opc_dst]  = 'BYTEPTR_DISPLACEMENT32_'  + self.REGS32_IDS[dst]
                    self.oo8On64PfEffects [rex][0x40 + opc_dst]  = 'BYTEPTR_DISPLACEMENT8_'   + self.DISP16_IDS[dst]
                    self.oo8On64PfEffects [rex][0x80 + opc_dst]  = 'BYTEPTR_DISPLACEMENT16_'  + self.DISP16_IDS[dst]
                    self.oo16On64Effects  [rex][0x40 + opc_dst]  = 'WORDPTR_DISPLACEMENT8_'   + self.REGS32_IDS[dst]
                    self.oo16On64Effects  [rex][0x80 + opc_dst]  = 'WORDPTR_DISPLACEMENT32_'  + self.REGS32_IDS[dst]
                    self.oo16On64PfEffects[rex][0x40 + opc_dst]  = 'WORDPTR_DISPLACEMENT8_'   + self.DISP16_IDS[dst]
                    self.oo16On64PfEffects[rex][0x80 + opc_dst]  = 'WORDPTR_DISPLACEMENT16_'  + self.DISP16_IDS[dst]
                    self.oo32On64Effects  [rex][0x40 + opc_dst]  = 'DWORDPTR_DISPLACEMENT8_'  + self.REGS32_IDS[dst]
                    self.oo32On64Effects  [rex][0x80 + opc_dst]  = 'DWORDPTR_DISPLACEMENT32_' + self.REGS32_IDS[dst]
                    self.oo32On64PfEffects[rex][0x40 + opc_dst]  = 'DWORDPTR_DISPLACEMENT8_'  + self.DISP16_IDS[dst]
                    self.oo32On64PfEffects[rex][0x80 + opc_dst]  = 'DWORDPTR_DISPLACEMENT16_' + self.DISP16_IDS[dst]
                    if rex & 8:
                        self.oo64Effects  [rex][0x40 + opc_dst]  = 'QWORDPTR_DISPLACEMENT8_'  + self.REGS64_IDS[dst]
                        self.oo64Effects  [rex][0x80 + opc_dst]  = 'QWORDPTR_DISPLACEMENT32_' + self.REGS64_IDS[dst]
                        self.oo64PfEffects[rex][0x40 + opc_dst]  = 'QWORDPTR_DISPLACEMENT8_'  + self.DISP16_IDS[dst]
                        self.oo64PfEffects[rex][0x80 + opc_dst]  = 'QWORDPTR_DISPLACEMENT16_' + self.DISP16_IDS[dst]
                    else:
                        self.oo64Effects  [rex][0x40 + opc_dst]  = 'DWORDPTR_DISPLACEMENT8_'  + self.REGS64_IDS[dst]
                        self.oo64Effects  [rex][0x80 + opc_dst]  = 'DWORDPTR_DISPLACEMENT32_' + self.REGS64_IDS[dst]
                        self.oo64PfEffects[rex][0x40 + opc_dst]  = 'DWORDPTR_DISPLACEMENT8_'  + self.DISP16_IDS[dst]
                        self.oo64PfEffects[rex][0x80 + opc_dst]  = 'DWORDPTR_DISPLACEMENT16_' + self.DISP16_IDS[dst]

                # Overwrite for SIB
                if 0x04 == dst:
                    # Overwrite the No Displacement
                    self.oo8Effects  [opc_dst]        = self.getSibEffectsTable('BYTEPTR_', modBits=0)
                    self.oo16Effects [opc_dst]        = self.getSibEffectsTable('WORDPTR_', modBits=0)
                    self.oo32Effects [opc_dst]        = self.getSibEffectsTable('DWORDPTR_', modBits=0)

                    self.oo8Effects  [0x40 + opc_dst] = self.getSibEffectsTable('BYTEPTR_', modBits=1)
                    self.oo8Effects  [0x80 + opc_dst] = self.getSibEffectsTable('BYTEPTR_', modBits=2)
                    self.oo16Effects [0x40 + opc_dst] = self.getSibEffectsTable('WORDPTR_', modBits=1)
                    self.oo16Effects [0x80 + opc_dst] = self.getSibEffectsTable('WORDPTR_', modBits=2)
                    self.oo32Effects [0x40 + opc_dst] = self.getSibEffectsTable('DWORDPTR_', modBits=1)
                    self.oo32Effects [0x80 + opc_dst] = self.getSibEffectsTable('DWORDPTR_', modBits=2)

                    for rex in range(0x10):
                        self.oo8On64Effects   [rex][opc_dst]          = self.getSib64EffectsTable('BYTEPTR_', modBits=0)
                        self.oo16On64Effects  [rex][opc_dst]          = self.getSib64EffectsTable('WORDPTR_', modBits=0)
                        self.oo32On64Effects  [rex][opc_dst]          = self.getSib64EffectsTable('DWORDPTR_', modBits=0)

                        self.oo8On64Effects   [rex][0x40 + opc_dst]   = self.getSib64EffectsTable('BYTEPTR_', modBits=1)
                        self.oo8On64Effects   [rex][0x80 + opc_dst]   = self.getSib64EffectsTable('BYTEPTR_', modBits=2)
                        self.oo16On64Effects  [rex][0x40 + opc_dst]   = self.getSib64EffectsTable('WORDPTR_', modBits=1)
                        self.oo16On64Effects  [rex][0x80 + opc_dst]   = self.getSib64EffectsTable('WORDPTR_', modBits=2)
                        self.oo32On64Effects  [rex][0x40 + opc_dst]   = self.getSib64EffectsTable('DWORDPTR_', modBits=1)
                        self.oo32On64Effects  [rex][0x80 + opc_dst]   = self.getSib64EffectsTable('DWORDPTR_', modBits=2)
                        if rex & 8:
                            self.oo64Effects  [rex][opc_dst]          = self.getSib64EffectsTable('QWORDPTR_', rex=(rex & 3), modBits=0)
                            self.oo64Effects  [rex][0x40 + opc_dst]   = self.getSib64EffectsTable('QWORDPTR_', rex=(rex & 3), modBits=1)
                            self.oo64Effects  [rex][0x80 + opc_dst]   = self.getSib64EffectsTable('QWORDPTR_', rex=(rex & 3), modBits=2)
                            self.oo64PfEffects[rex][opc_dst]          = self.getSib64EffectsTable('QWORDPTR_', rex=(rex & 3), modBits=0, sizePrefix=True)
                            self.oo64PfEffects[rex][0x40 + opc_dst]   = self.getSib64EffectsTable('QWORDPTR_', rex=(rex & 3), modBits=1, sizePrefix=True)
                            self.oo64PfEffects[rex][0x80 + opc_dst]   = self.getSib64EffectsTable('QWORDPTR_', rex=(rex & 3), modBits=2, sizePrefix=True)
                        else:
                            self.oo64Effects  [rex][opc_dst]          = self.getSib64EffectsTable('DWORDPTR_', rex=(rex & 3), modBits=0)
                            self.oo64Effects  [rex][0x40 + opc_dst]   = self.getSib64EffectsTable('DWORDPTR_', rex=(rex & 3), modBits=1)
                            self.oo64Effects  [rex][0x80 + opc_dst]   = self.getSib64EffectsTable('DWORDPTR_', rex=(rex & 3), modBits=2)
                            self.oo64PfEffects[rex][opc_dst]          = self.getSib64EffectsTable('DWORDPTR_', rex=(rex & 3), modBits=0, sizePrefix=True)
                            self.oo64PfEffects[rex][0x40 + opc_dst]   = self.getSib64EffectsTable('DWORDPTR_', rex=(rex & 3), modBits=1, sizePrefix=True)
                            self.oo64PfEffects[rex][0x80 + opc_dst]   = self.getSib64EffectsTable('DWORDPTR_', rex=(rex & 3), modBits=2, sizePrefix=True)

    def getSibEffectsTable( self, addBefore, addAfter = '', modBits=0):
        table = [None] * 0x100
        for i in range(0x100):
            base = i & 0x7
            if 0x5 == base:
                    if 0 == modBits:
                        table[i] = addBefore + 'DISPLACEMENT32' + self.sibTable[i] + addAfter
                    elif 1 == modBits:
                        table[i] = addBefore + 'DISPLACEMENT8_EBP' + self.sibTable[i].replace('_NOBASE', '') + addAfter
                    elif 2 == modBits:
                        table[i] = addBefore + 'DISPLACEMENT32_EBP' + self.sibTable[i].replace('_NOBASE', '') + addAfter
                    elif 3 == modBits:
                        table[i] = ''
                    else:
                        raise Exception("Invalid mod bits")
            else:
                if 0 == modBits:
                    table[i] = addBefore + self.sibTable[i] + addAfter
                elif 1 == modBits:
                    table[i] = addBefore + 'DISPLACEMENT8_' + self.sibTable[i] + addAfter
                elif 2 == modBits:
                    table[i] = addBefore + 'DISPLACEMENT32_' + self.sibTable[i] + addAfter
                else:
                    table[i] = ''
        return table

    def getSib64EffectsTable( self, addBefore, addAfter='', rex=0, sizePrefix=False, modBits=0):
        table = [None] * 0x100
        if False == sizePrefix:
            sibTable64 = copy.deepcopy(self.sib64Table[rex])
        else:
            sibTable64 = copy.deepcopy(self.sib32Table[rex])
        for i in range(0x100):
            base = i & 0x7
            if 0x5 == base:
                    if 0 == modBits:
                        table[i] = addBefore + 'DISPLACEMENT32' + sibTable64[i] + addAfter
                    elif 1 == modBits:
                        table[i] = addBefore + 'DISPLACEMENT8_RBP' + sibTable64[i].replace('_NOBASE', '') + addAfter
                    elif 2 == modBits:
                        table[i] = addBefore + 'DISPLACEMENT32_RBP' + sibTable64[i].replace('_NOBASE', '') + addAfter
                    elif 3 == modBits:
                        table[i] = ''
                    else:
                        raise Exception("Invalid mod bits")
            else:
                if 0 == modBits:
                    table[i] = addBefore + sibTable64[i] + addAfter
                elif 1 == modBits:
                    table[i] = addBefore + 'DISPLACEMENT8_' + sibTable64[i] + addAfter
                elif 2 == modBits:
                    table[i] = addBefore + 'DISPLACEMENT32_' + sibTable64[i] + addAfter
                else:
                    table[i] = ''
        return table

    def buildEmptyBlock(self, table, routeToBuild, startRoute=[]):
        if None == self.getTableVal(table, [0] + startRoute + routeToBuild[:1]):
            temp_table = self._makeArray([4, 0x100])
            temp_table64 = self._makeArray([4, 0x10, 0x100])
            self.setOpcodeEffect(startRoute + routeToBuild[:1], temp_table[0], temp_table[1], temp_table[2], temp_table[3])
            for rex in range(0x10):
                self.setOpcodeEffect(startRoute + routeToBuild[:1], temp_table64[0], temp_table64[1], temp_table64[2], temp_table64[3], is64=True, rex=rex)
        if len(routeToBuild) > 1:
            self.buildEmptyBlock(table, routeToBuild[1:], startRoute + routeToBuild[:1])

    def writeToTable(self, table, route, value):
        t = table
        for x in route[:-1]:
            t = t[x]
        t[route[-1]] = copy.copy(value)

    def getTableVal(self, table, route):
        t = table
        for x in route:
            t = t[x]
        return t

    def setOpcodeEffect(self, route, noPrefixEffect, sizePrefixEffect, addrPrefixEffect, sizeAddrEffect, is64=False, rex=None):
        if is64:
            self.writeToTable(self.t64, [0, rex] + route, noPrefixEffect[rex])
            self.writeToTable(self.t64, [1, rex] + route, sizePrefixEffect[rex])
            self.writeToTable(self.t64, [2, rex] + route, addrPrefixEffect[rex])
            self.writeToTable(self.t64, [3, rex] + route, sizeAddrEffect[rex])
        else:
            self.writeToTable(self.t32, [0] + route, noPrefixEffect)
            self.writeToTable(self.t32, [1] + route, sizePrefixEffect)
            self.writeToTable(self.t32, [2] + route, addrPrefixEffect)
            self.writeToTable(self.t32, [3] + route, sizeAddrEffect)

    def setMaskedOpcodeEffect(self, route, mask, target, noPrefixEffect, sizePrefixEffect, addrPrefixEffect, sizeAddrEffect, is64=False, rex=None):
        if None == mask:
            self.setOpcodeEffect(route, noPrefixEffect, sizePrefixEffect, addrPrefixEffect, sizeAddrEffect, is64=is64, rex=rex)
            return
        elif    (tuple != type(noPrefixEffect)) and\
                (list  != type(noPrefixEffect)):

            raise "Invalid: mask with none MODRM"

        if (False==is64) and (None == self.getTableVal(self.t32, [0] + route)):
            self.writeToTable(self.t32, [0] + route, [None] * 0x100)
            self.writeToTable(self.t32, [1] + route, [None] * 0x100)
            self.writeToTable(self.t32, [2] + route, [None] * 0x100)
            self.writeToTable(self.t32, [3] + route, [None] * 0x100)
        if (True==is64) and (None == self.getTableVal(self.t64, [0, rex] + route)):
            self.writeToTable(self.t64, [0, rex] + route, [None] * 0x100)
            self.writeToTable(self.t64, [1, rex] + route, [None] * 0x100)
            self.writeToTable(self.t64, [2, rex] + route, [None] * 0x100)
            self.writeToTable(self.t64, [3, rex] + route, [None] * 0x100)
        for i in range(0x100):
            if target != (i & mask):
                continue
            if True==is64:
                self.writeToTable(self.t64, [0, rex] + route + [i], noPrefixEffect[rex][i])
                self.writeToTable(self.t64, [1, rex] + route + [i], sizePrefixEffect[rex][i])
                self.writeToTable(self.t64, [2, rex] + route + [i], addrPrefixEffect[rex][i])
                self.writeToTable(self.t64, [3, rex] + route + [i], sizeAddrEffect[rex][i])
            else:
                self.writeToTable(self.t32, [0] + route + [i], noPrefixEffect[i])
                self.writeToTable(self.t32, [1] + route + [i], sizePrefixEffect[i])
                self.writeToTable(self.t32, [2] + route + [i], addrPrefixEffect[i])
                self.writeToTable(self.t32, [3] + route + [i], sizeAddrEffect[i])

    def setOpcodeGroupEffect(self, route, mask, noPrefixEffect, sizePrefixEffect, addrPrefixEffect, sizeAddrEffect, is64=False, rex=None):
        if None == mask:
            raise "Invalid: group without mask"

        for i in range(0x100):
            if route[-1] != (i & mask):
                continue
            self.setOpcodeEffect(i, noPrefixEffect[i], sizePrefixEffect[i], addrPrefixEffect[i], sizeAddrEffect[i], is64=is64, rex=rex)

    def testRecursiveParser( self, table, data ):
        b = ord(data[0])
        effect = table[b]
        if type(effect) == types.StringType or None == effect:
            return effect
        else:
            return testRecursiveParser( effect, data[1:] )

    def testSizeParser( self, table, data ):
        b = ord(data[0])
        if 0x67 == b:
            testSizeAddrParser( table, data[1:] )
        if 0x66 == b:
            testSizeParser( table, data[1:] )

        return testRecursiveParser( table[1], data )

    def testAddrParser( self, table, data ):
        b = ord(data[0])
        if 0x66 == b:
            testSizeAddrParser( data[1:] )
        if 0x67 == b:
            testAddrParser( table, data[1:] )

        return testRecursiveParser( table[2], data )

    def testSizeAddrParser( self, table, data ):
        b = ord(data[0])
        if 0x66 == b:
            testSizeAddrParser( table, data[1:] )
        if 0x67 == b:
            testSizeAddrParser( table, data[1:] )

        return testRecursiveParser( table[3], data )

    def testParser( self, table, data ):
        b = ord(data[0])
        if 0x66 == b:
            testSizeParser( table, data[1:] )
        if 0x67 == b:
            testAddrParser( table, data[1:] )

        return testRecursiveParser( table[0], data )
    
    def __getAllKindsOfEffects(self, table, allKindsOfEffects=None, done=None):
        if None == allKindsOfEffects:
            allKindsOfEffects = []
        if None == done:
            done = []
        for i in table:
            if i not in done:
                done.append(i)
                if type(i) == str:
                    if i not in allKindsOfEffects:
                        allKindsOfEffects.append(i)
                elif type(i) == list or type(i) == dict:
                    allKindsOfEffects, done = self.__getAllKindsOfEffects(i, allKindsOfEffects, done)
        return allKindsOfEffects, done

    def getAllKindsOfEffects(self, table):
        return self.__getAllKindsOfEffects(table)[0]

    def countNodesRecursive(self, table):
        nodes_counter = 0
        for i in range(0x100):
            nodes_counter += 1
            effect = table[i]
            if types.StringType == type(effect) or None == effect:
                continue
            else:
                nodes_counter += self.countNodesRecursive(effect)
        return nodes_counter

def countNodes(table):
    nodes_counter = 0
    print 'Counting table effects'
    nodes_counter += self.countNodesRecursive(table[0])
    print 'Nodes so far %d' % nodes_counter
    print 'Counting size_prefix_table effects'
    nodes_counter += self.countNodesRecursive(table[1])
    print 'Nodes so far %d' % nodes_counter
    print 'Counting addr_prefix_table effects'
    nodes_counter += self.countNodesRecursive(table[2])
    print 'Nodes so far %d' % nodes_counter
    print 'Counting size_n_addr effects'
    nodes_counter += self.countNodesRecursive(table[3])
    return nodes_counter

def diffTables(t1, t2, opcode=None, done=None):
    if None == opcode:
        opcode = []
    if None == done:
        done = []
    for i in range(0x100):
        effect1 = t1[i]
        effect2 = t2[i]
        if '' == effect1:
            effect1 = None
        if '' == effect2:
            effect2 = None
        if type(effect1) == str and type(effect2) != str:
            if 'POP' in effect1:
                pass
            else:
                print map(hex, opcode + [i])
                continue
        if type(effect2) == str and type(effect1) != str:
            if 'POP' in effect2:
                pass
            else:
                print map(hex, opcode + [i])
                continue
        if type(effect1) == str:
            if 'POP' in effect1 or 'POP' in effect2:
                pass
            elif effect1 != effect2:
                print (''.join(map(chr, opcode + [i]))).encode('hex')
        elif effect1 == None or effect2 == None:
            if effect1 != effect2:
                print map(hex, opcode + [i])
            pass
        else:
            if effect1 not in done:
                done.append(effect1)
                diffTables(effect1, effect2, opcode + [i], done)

def findOpcodeWithEffect(table, target, opcode=None):
    if None == opcode:
        opcode = []
    for i in range(0x100):
        effect = table[i]
        if type(effect) == types.StringType:
            if effect == target:
                opcode.append(i)
                return (''.join(map(chr, opcode))).encode('hex')
        elif None == effect:
            pass
        else:
            result = findOpcodeWithEffect(effect, target, opcode + [i])
            if result != None:
                return result
    return None

def getEffect(table, code):
    pos = 1
    effect = table[ord(code[0])]
    while type(effect) != types.StringType and effect != None:
        effect = effect[ord(code[pos])]
        pos += 1
        if pos == (len(code) - 1):
            return None, None
    return (pos, str(effect))

def printEffects(table, code):
    pos = 0
    while pos < (len(code) - 1):
        byte = ord(code[pos])
        opcode_size, effect = getEffect(table, code[pos:][:12])
        if None == opcode_size or None == effect:
            return
        print '%4d %s\t' % (opcode_size, effect),
        decoded = distorm3.Decode(0, code[pos:][:12])[0]
        pos += decoded[1]
        self.printOpcode(decoded)


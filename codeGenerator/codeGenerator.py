import time

startTime = time.time()
execfile('disasmTablesGenerator.py')

OUTPUT_FILE = 'opcodeSideEffects.auto.asm'
OUTPUT_FILE64 = 'opcodeSideEffects64.auto.asm'
EIP_REG = 'ebx'
RIP_REG = 'rbx'
OUTPUT_REG = 'eax'
OUTPUT_REG64 = 'rax'

REGISTERS_OFFSETS = {
        'RDI': 'LAST_RDI',
        'EDI': 'LAST_EDI',
        'DI' : 'LAST_EDI',
        'RSI': 'LAST_RDI',
        'ESI': 'LAST_ESI',
        'SI' : 'LAST_ESI',
        'RBP': 'LAST_RBP',
        'EBP': 'LAST_EBP',
        'BP' : 'LAST_EBP',
        # krenel ESP
        'RBX': 'LAST_RBX',
        'EBX': 'LAST_EBX',
        'BX' : 'LAST_EBX',
        'BL' : 'LAST_EBX',
        'BH' : 'LAST_BH',
        'RDX': 'LAST_RDX',
        'EDX': 'LAST_EDX',
        'DX' : 'LAST_EDX',
        'DL' : 'LAST_EDX',
        'DH' : 'LAST_DH',
        'RCX': 'LAST_RCX',
        'ECX': 'LAST_ECX',
        'CX' : 'LAST_ECX',
        'CL' : 'LAST_ECX',
        'CH' : 'LAST_CH',
        'RAX': 'LAST_RAX',
        'EAX': 'LAST_EAX',
        'AX' : 'LAST_EAX',
        'AL' : 'LAST_EAX',
        'AH' : 'LAST_AH',
        'RIP': 'LAST_RIP',
        'EIP': 'LAST_EIP',
        'IP' : 'LAST_EIP',
        'RFLAGS': 'LAST_RFLAGS',
        'EFLAGS': 'LAST_EFLAGS',
        'FLAGS': 'LAST_EFLAGS',
        'RSP' : 'LAST_RSP',
        'ESP' : 'LAST_ESP',
        'SP'  : 'LAST_ESP',
        'R8'  : 'LAST_R8',
        'R8B' : 'LAST_R8',
        'R8W' : 'LAST_R8',
        'R8D' : 'LAST_R8',
        'R9'  : 'LAST_R9',
        'R9B' : 'LAST_R9',
        'R9W' : 'LAST_R9',
        'R9D' : 'LAST_R9',
        'R10' : 'LAST_R10',
        'R10B': 'LAST_R10',
        'R10W': 'LAST_R10',
        'R10D': 'LAST_R10',
        'R11' : 'LAST_R11',
        'R11B': 'LAST_R11',
        'R11W': 'LAST_R11',
        'R11D': 'LAST_R11',
        'R12' : 'LAST_R12',
        'R12B': 'LAST_R12',
        'R12W': 'LAST_R12',
        'R12D': 'LAST_R12',
        'R13' : 'LAST_R13',
        'R13B': 'LAST_R13',
        'R13W': 'LAST_R13',
        'R13D': 'LAST_R13',
        'R14' : 'LAST_R14',
        'R14B': 'LAST_R14',
        'R14W': 'LAST_R14',
        'R14D': 'LAST_R14',
        'R15' : 'LAST_R15',
        'R15B': 'LAST_R15',
        'R15W': 'LAST_R15',
        'R15D': 'LAST_R15' }
REGISTERS_SIZES = {
        'RDI': 8,
        'EDI': 4,
        'DI' : 2,
        'RSI': 8,
        'ESI': 4,
        'SI' : 2,
        'RBP': 8,
        'EBP': 4,
        'BP' : 2,
        'RSP': 8,
        'ESP': 4,
        'SP' : 2,
        'RBX': 8,
        'EBX': 4,
        'BX' : 2,
        'BL' : 1,
        'BH' : 1,
        'RDX': 8,
        'EDX': 4,
        'DX' : 2,
        'DL' : 1,
        'DH' : 1,
        'RCX': 8,
        'ECX': 4,
        'CX' : 2,
        'CL' : 1,
        'CH' : 1,
        'RAX': 8,
        'EAX': 4,
        'AX' : 2,
        'AL' : 1,
        'AH' : 1,
        'RIP': 8,
        'EIP': 4,
        'IP' : 2,
        'EFLAGS': 4,
        'ECS' : 4,
        'R8'  : 8,
        'R8B' : 1,
        'R8W' : 2,
        'R8D' : 4,
        'R9'  : 8,
        'R9B' : 1,
        'R9W' : 2,
        'R9D' : 4,
        'R10' : 8,
        'R10B': 1,
        'R10W': 2,
        'R10D': 4,
        'R11' : 8,
        'R11B': 1,
        'R11W': 2,
        'R11D': 4,
        'R12' : 8,
        'R12B': 1,
        'R12W': 2,
        'R12D': 4,
        'R13' : 8,
        'R13B': 1,
        'R13W': 2,
        'R13D': 4,
        'R14' : 8,
        'R14B': 1,
        'R14W': 2,
        'R14D': 4,
        'R15' : 8,
        'R15B': 1,
        'R15W': 2,
        'R15D': 4 }
ACCESSES_IDS = {
        'BYTE'    : 28,
        'WORD'    : 29,
        'DWORD'   : 30,
        'QWORD'   : 31,
        'STACK_BYTE'    : 28,
        'STACK_WORD'    : 29,
        'STACK_DWORD'   : 30,
        'STACK_QWORD'   : 31,
        'STACK_ALL32'   : 32,
        'STACK_ALL16'   : 33 }

EDX_PART_BY_SIZE = {
        1 : 'dl',
        2 : 'dx',
        4 : 'edx',
        8 : 'rdx' }
SIZE_NAME = {
        1 : 'BYTE',
        2 : 'WORD',
        4 : 'DWORD',
        8 : 'QWORD' }
NAME_SIZE = {
        'BYTE'  : 1,
        'WORD'  : 2,
        'DWORD' : 4,
        'QWORD' : 8,
        }
ECX_PART_BY_MEMORY_ACCESS_SIZE = {
        'BYTE'   : 'cl',
        'WORD'   : 'cx',
        'DWORD'  : 'ecx',
        'QWORD'  : 'rcx' }

SIZE_NAME_OF_DISPLACEMENT = {
        'DISPLACEMENT8' : 'BYTE',
        'DISPLACEMENT16': 'WORD',
        'DISPLACEMENT32': 'DWORD' }

INC_EAX_1 = """
    inc eax
"""[1:]
INC_EAX_2 = """
    inc eax
    inc eax
"""[1:]
INC_EAX_4 = """
    add eax, 4
"""[1:]
INC_RAX_1 = """
    inc rax
"""[1:]
INC_RAX_2 = """
    inc rax
    inc rax
"""[1:]
INC_RAX_4 = """
    add rax, 4
"""[1:]
INC_RAX_8 = """
    add rax, 8
"""[1:]

ADVANCE_OUTPUT_BUFFER32 = {
        1 : INC_EAX_1,
        2 : INC_EAX_2,
        4 : INC_EAX_4 }
ADVANCE_OUTPUT_BUFFER64 = {
        1 : INC_RAX_1,
        2 : INC_RAX_2,
        4 : INC_RAX_4,
        8 : INC_RAX_8 }

#################
# Pieces of code:

NEXT_BYTE_ACCORDING_TO_TABLE_CODE = """
    mov cl, BYTE [#CODE_POINTER#]
    inc #CODE_POINTER#
    #EXTRA_LOADING_CODE#
    jmp #POINTER_SIZE_NAME# [#TABLE_NAME# + #ECX_MAX_SIZE# * 4]
"""[1:]

WRITE_ACCESS_ID_CODE = """
    mov cl, #ACCESS_ID#
    mov BYTE [#OUTPUT_POINTER#], cl
    inc #OUTPUT_POINTER#
"""[1:]
WRITE_MEM_REG_ACCESS_ID_CODE = WRITE_ACCESS_ID_CODE.replace("#ACCESS_ID#", '#MEM_REG_ACCESS_ID#')

INC_EAX_CODE = """
    #INC_EAX#
"""[1:]

RET_CODE = """
    ; Return
    #ADVANCE_OUTPUT_BUFFER#
    jmp FINISH_LOG_CYCLE
"""[1:]

# Not implemented
LOG_REG_CODE = """
    #NOT_IMPLEMENTED#
"""[1:]

# Note ecx must point to the mem value
# Mem pointer is either ecx or rcx
# Output pointer is either eax or rax
WRITE_MEM_VALUE = """
    ; Writting value
    mov #ECX_PART#, #ACCESS_SIZE# [#MEM_POINTER#]
    mov #ACCESS_SIZE# [#OUTPUT_POINTER#], #ECX_PART#
"""[1:]

# Temp reg should be either ecx or rcx
# Output pointer is either eax or rax
LOG_MOD_MEM_CODE = """
    ; MOD MEM ACCESS
    mov #MEM_POINTER_PART#, #MEM_REG_SIZE_NAME# [#BASE_POINTER# + #MEM_REG_OFFSET#]
    mov #POINTER_SIZE_NAME# [#OUTPUT_POINTER#], #MEM_POINTER#
    add #OUTPUT_POINTER#, #POINTER_SIZE#
"""[1:]

# Note ebx must point to the displacement
# Displacement pointer is either edx or rdx
# Temp reg 1 is ecx / rcx and 2 is edx / rdx
LOG_MOD_MEM_DISPLACEMENT_CODE = """
    ; DISPLACEMENT #DISPLACEMENT_SIZE#
    ; Write the mem address
    mov #MEM_POINTER_PART#, #MEM_REG_SIZE_NAME# [#BASE_POINTER# + #MEM_REG_OFFSET#]
    #MOVE_TYPE# #OFFSET_REG#, #DISPLACEMENT_SIZE# [#CODE_POINTER#]
    lea #MEM_POINTER#, [#MEM_POINTER# + #OFFSET_REG_FULL#]
    mov #POINTER_SIZE_NAME# [#OUTPUT_POINTER#], #MEM_POINTER#
    add #OUTPUT_POINTER#, #POINTER_SIZE#
"""[1:]

LOG_STACK_PUSH_CODE = """
    ; PUSH
    ; Write the mem address
    mov #MEM_POINTER#, #POINTER_SIZE_NAME# [#STACK_POINTER# + SAVED_ESP]
    mov #POINTER_SIZE_NAME# [#OUTPUT_POINTER#], #MEM_POINTER#
    add #OUTPUT_POINTER#, #POINTER_SIZE#
"""[1:]

# 32bits only!
LOG_STACK_PUSH_ALL_CODE = """
    ; PUSHA 32bit
    ; Get esp
    mov ecx, DWORD [esp + SAVED_ESP]
    mov DWORD [eax], ecx
    add eax, 4
    ; Copy block from process tack to log buffer
    push esi
    push edi
    mov esi, ecx
    mov edi, eax
    mov ecx, 8
    rep movsd
    add eax, 20h
    pop edi
    pop esi
    ; No need for ret code
    jmp FINISH_LOG_CYCLE
"""[1:]

# 32bits only!
LOG_STACK_PUSH_ALL_16_CODE = """
    ; PUSHA 16bit
    ; Get esp
    mov ecx, DWORD [esp + SAVED_ESP]
    mov DWORD [eax], ecx
    add eax, 4
    ; Copy block from process tack to log buffer
    push esi
    push edi
    mov esi, ecx
    mov edi, eax
    mov ecx, 4
    rep movsd
    add eax, 10h
    pop edi
    pop esi
    ; No need for ret code
    jmp FINISH_LOG_CYCLE
"""[1:]

LOG_STACK_POP_CODE = """
    ; POP
    ; Write the mem address
    mov #MEM_POINTER#, #POINTER_SIZE_NAME# [#BASE_POINTER# + LAST_ESP]
    sub #MEM_POINTER#, 4
    mov #POINTER_SIZE_NAME# [#OUTPUT_POINTER#], #MEM_POINTER#
    add #OUTPUT_POINTER#, #POINTER_SIZE#
"""[1:]

# 32bits only!
LOG_STACK_POP_ALL_CODE = """
    ; POPA 32bit
    ; Get esp
    mov ecx, DWORD [ebp + LAST_ESP]
    sub ecx, 20h
    mov DWORD [eax], ecx
    add eax, 4
    ; Copy block from process tack to log buffer
    push esi
    push edi
    mov esi, ecx
    mov edi, eax
    mov ecx, 8
    rep movsd
    add eax, 20h
    pop edi
    pop esi
    ; No need for ret code
    jmp FINISH_LOG_CYCLE
"""[1:]

# 32bits only!
LOG_STACK_POP_ALL_16_CODE = """
    ; PUSHA 16bit
    ; Get esp
    mov ecx, DWORD [ebp + LAST_ESP]
    sub ecx, 10h
    mov DWORD [eax], ecx
    add eax, 4
    ; Copy block from process tack to log buffer
    push esi
    push edi
    mov esi, ecx
    mov edi, eax
    mov ecx, 4
    rep movsd
    add eax, 10h
    pop edi
    pop esi
    ; No need for ret code
    jmp FINISH_LOG_CYCLE
"""[1:]

# Displacement pointer should be either ebx or rbx
LOG_DISPLACEMENT32_ONLY_CODE = """
    ; DISPLACEMENT DWORD
    ; Write the mem address
    mov ecx, DWORD [#CODE_POINTER#]
    mov DWORD [#OUTPUT_POINTER#], ecx
    add #OUTPUT_POINTER#, 4
"""[1:]

# Displacement pointer should be either ebx or rbx
LOG_DISPLACEMENT64_ONLY_CODE = """
    ; DISPLACEMENT DWORD
    ; Write the mem address
    mov rcx, QWORD [#CODE_POINTER#]
    mov QWORD [#OUTPUT_POINTER#], rcx
    add #OUTPUT_POINTER#, 8
"""[1:]

# Temp reg should be either ecx or rcx
LOG_SIB_CODE = """
    ; SIB #BASE# + #SCALE# * #INDEX#
    ; Get reg1
    mov #MEM_POINTER#, #POINTER_SIZE_NAME# [#BASE_POINTER# + LAST_#BASE#]
    ; Get reg2
    mov #HOLD_INDEX_REG#, #POINTER_SIZE_NAME# [#BASE_POINTER# + LAST_#INDEX#]
    ; Add and mul by scale
    lea #MEM_POINTER#, [#MEM_POINTER# + #HOLD_INDEX_REG# * #SCALE#]
    ; Write the result, which is the address
    mov #POINTER_SIZE_NAME# [#OUTPUT_POINTER#], #MEM_POINTER#
    add #OUTPUT_POINTER#, #POINTER_SIZE#
"""[1:]

LOG_SIB_SAME_BASE_N_INDEX_CODE = """
    ; SIB #BASE# + #SCALE# * #BASE# (BASE n' INDEX are the same)
    ; Get reg
    mov #MEM_POINTER#, #POINTER_SIZE_NAME# [#BASE_POINTER# + LAST_#BASE#]
    ; Add and mul by scale
    lea #MEM_POINTER#, [#MEM_POINTER# + #MEM_POINTER# * #SCALE#]
    ; Write the result, which is the address
    mov #POINTER_SIZE_NAME# [#OUTPUT_POINTER#], #MEM_POINTER#
    add #OUTPUT_POINTER#, #POINTER_SIZE#
"""[1:]

# Note ebx must point to the displacement
# Temp -> ecx / rcx
# Temp2 -> edx / rdx
LOG_SIB_WITH_DISPLACEMENT_CODE = """
    ; SIB #BASE# + #SCALE# * #INDEX# + DISPLACEMENT #DISPLACEMENT_SIZE#
    ; Get reg1
    mov #MEM_POINTER#, #POINTER_SIZE_NAME# [#BASE_POINTER# + LAST_#BASE#]
    ; Get reg2
    mov #HOLD_INDEX_REG#, #POINTER_SIZE_NAME# [#BASE_POINTER# + LAST_#INDEX#]
    ; Add reg2 and mul by scale
    lea #MEM_POINTER#, [#MEM_POINTER# + #HOLD_INDEX_REG# * #SCALE#]
    ; Read the displacement
    #MOVE_TYPE# #OFFSET_REG#, #DISPLACEMENT_SIZE# [#CODE_POINTER#]
    lea #MEM_POINTER#, [#MEM_POINTER# + #OFFSET_REG_FULL#]
    ; Write the result, which is the address
    mov #POINTER_SIZE_NAME# [#OUTPUT_POINTER#], #MEM_POINTER#
    add #OUTPUT_POINTER#, #POINTER_SIZE#
"""[1:]

LOG_SIB_WITH_DISPLACEMENT_SAME_BASE_N_INDEX_CODE = """
    ; SIB #BASE# + #SCALE# * #BASE# + DISPLACEMENT #DISPLACEMENT_SIZE# (BASE n' INDEX are the same)
    ; Get reg
    mov #MEM_POINTER#, #POINTER_SIZE_NAME# [#BASE_POINTER# + LAST_#BASE#]
    ; Add and mul by scale
    lea #MEM_POINTER#, [#MEM_POINTER# + #MEM_POINTER# * #SCALE#]
    ; Read the displacement
    #MOVE_TYPE# #OFFSET_REG#, #DISPLACEMENT_SIZE# [#CODE_POINTER#]
    lea #MEM_POINTER#, [#MEM_POINTER# + #OFFSET_REG_FULL#]
    ; Write the result, which is the address
    mov #POINTER_SIZE_NAME# [#OUTPUT_POINTER#], #MEM_POINTER#
    add #OUTPUT_POINTER#, #POINTER_SIZE#
"""[1:]

# Note ebx must point to the displacement
LOG_SIB_WITH_DISPLACEMENT_NOBASE_CODE = """
    ; SIB #SCALE# * #INDEX# + DISPLACEMENT #DISPLACEMENT_SIZE#
    ; Get reg1
    mov #MEM_POINTER#, #POINTER_SIZE_NAME# [#BASE_POINTER# + LAST_#INDEX#]
    ; Read the displacement
    #MOVE_TYPE# #OFFSET_REG#, #DISPLACEMENT_SIZE# [#CODE_POINTER#]
    ; Add displacement and mul by scale
    lea #MEM_POINTER#, [#OFFSET_REG_FULL# + #MEM_POINTER# * #SCALE#]
    ; Write the result, which is the address
    mov #POINTER_SIZE_NAME# [#OUTPUT_POINTER#], #MEM_POINTER#
    add #OUTPUT_POINTER#, #POINTER_SIZE#
"""[1:]


LOG_REG_FUNCTION                    = WRITE_ACCESS_ID_CODE + LOG_REG_CODE + RET_CODE
LOG_MOD_MEM_FUNCTION                = WRITE_ACCESS_ID_CODE + LOG_MOD_MEM_CODE + WRITE_MEM_VALUE + RET_CODE
LOG_2_MEM_ACCESSES_FUNCTION         = WRITE_ACCESS_ID_CODE + \
        LOG_MOD_MEM_CODE.replace('MEM_REG_OFFSET', 'MEM_REG1_OFFSET').replace('MEM_REG_SIZE_NAME', 'MEM_REG1_SIZE_NAME') + \
        WRITE_MEM_VALUE + INC_EAX_CODE + \
        LOG_MOD_MEM_CODE.replace('MEM_REG_OFFSET', 'MEM_REG2_OFFSET').replace('MEM_REG_SIZE_NAME', 'MEM_REG2_SIZE_NAME') + \
        WRITE_MEM_VALUE + RET_CODE
LOG_MOD_MEM_DISPLACEMENT_FUNCTION   = WRITE_ACCESS_ID_CODE + LOG_MOD_MEM_DISPLACEMENT_CODE + WRITE_MEM_VALUE + RET_CODE
LOG_DISPLACEMENT32_ONLY_FUNCTION    = WRITE_ACCESS_ID_CODE + LOG_DISPLACEMENT32_ONLY_CODE + WRITE_MEM_VALUE + RET_CODE
LOG_DISPLACEMENT64_ONLY_FUNCTION    = WRITE_ACCESS_ID_CODE + LOG_DISPLACEMENT64_ONLY_CODE + WRITE_MEM_VALUE + RET_CODE
LOG_STACK_PUSH_FUNCTION             = WRITE_ACCESS_ID_CODE + LOG_STACK_PUSH_CODE + WRITE_MEM_VALUE + RET_CODE
LOG_STACK_PUSH_ALL_FUNCTION         = WRITE_ACCESS_ID_CODE + LOG_STACK_PUSH_ALL_CODE
LOG_STACK_PUSH_ALL_16_FUNCTION      = WRITE_ACCESS_ID_CODE + LOG_STACK_PUSH_ALL_16_CODE
LOG_STACK_POP_FUNCTION              = WRITE_ACCESS_ID_CODE + LOG_STACK_POP_CODE + WRITE_MEM_VALUE + RET_CODE
LOG_STACK_POP_ALL_FUNCTION          = WRITE_ACCESS_ID_CODE + LOG_STACK_POP_ALL_CODE
LOG_STACK_POP_ALL_16_FUNCTION       = WRITE_ACCESS_ID_CODE + LOG_STACK_POP_ALL_16_CODE
LOG_SIB_MEM_FUNCTION                = WRITE_ACCESS_ID_CODE + LOG_SIB_CODE + WRITE_MEM_VALUE + RET_CODE
LOG_SIB_MEM_SAME_BASE_N_INDEX_FUNCTION = WRITE_ACCESS_ID_CODE + LOG_SIB_SAME_BASE_N_INDEX_CODE + WRITE_MEM_VALUE + RET_CODE
LOG_SIB_WITH_DISPLACEMENT_FUNCTION  = WRITE_ACCESS_ID_CODE + LOG_SIB_WITH_DISPLACEMENT_CODE + WRITE_MEM_VALUE + RET_CODE
LOG_SIB_WITH_DISPLACEMENT_SAME_BASE_N_INDEX_FUNCTION  = WRITE_ACCESS_ID_CODE + LOG_SIB_WITH_DISPLACEMENT_SAME_BASE_N_INDEX_CODE + WRITE_MEM_VALUE + RET_CODE
LOG_SIB_WITH_DISPLACEMENT_NOBASE_FUNCTION = WRITE_ACCESS_ID_CODE + LOG_SIB_WITH_DISPLACEMENT_NOBASE_CODE + WRITE_MEM_VALUE + RET_CODE

#filters:
EMPTY_FILTER            = set()
PUSH_FILTER             = set(['PUSH'])
POP_FILTER              = set(['POP'])
STACK_FILTER            = set(['STACK'])
DISPLACEMENT_FILTER     = set(['DISPLACEMENT8', 'DISPLACEMENT16', 'DISPLACEMENT32', 'DISPLACEMENT64'])
DISPLACEMENT32_FILTER   = set(['DISPLACEMENT32'])
DISPLACEMENT64_FILTER   = set(['DISPLACEMENT64'])
REGISTERS_FILTER        = set(REGISTERS_SIZES.keys())
PLUS_FILTER             = set(['PLUS'])
SIB_FILTER              = set(['SIB'])
ANOTHER_POINTER_FILTER  = set(['PTR2'])
NOBASE_FILTER           = set(['NOBASE'])

class OreganoCodeGenerator(object):
    def __init__(self):
        print 'Creating disasm tables',
        dg = DisasmGenerator()
        print 'DONE'
        print 'Gen code',
        self.jumpTables = []
        self.uniqueChecker = {}
        self.opcodesWithSameEffect = []
        self.allKindsOfEffects = {}
        self.codeMissing = {}
        self.highestTableId = 0
        self.fullTable   = dg.getTable32()
        code, tableId = self.genJumpTable(self.fullTable)
        print 'DONE'
        print 'Writting everything',
        if tableId != 1:
            raise Exception("Main table is not ided 1")
        code += '\n\n\n;Jump tables\n'
        code += "section .JTABLE rdata align=4"
        for jumps in self.jumpTables:
            code += '\n'.join(jumps)
        code += '\n\n'
        file(OUTPUT_FILE, 'wb').write(code)
        print 'DONE'

        print 'Gen code 64',
        self.jumpTables = []
        self.uniqueChecker = {}
        self.opcodesWithSameEffect = []
        self.allKindsOfEffects = {}
        self.highestTableId = 0
        self.fullTable64 = dg.getTable64()
        code64, table64Id = self.genJumpTable(self.fullTable64, is64=True)
        print 'DONE'
        print 'Writting everything',
        if table64Id != 1:
            raise Exception("Main table is not ided 1")
        code64 += '\n\n\n;Jump tables\n'
        code64 += "section .JTABLE rdata align=4"
        for jumps in self.jumpTables:
            code64 += '\n'.join(jumps)
        code64 += '\n\n'
        file(OUTPUT_FILE64, 'wb').write(code64)
        print 'DONE'

    # Skeleton is one of the functions defined above
    # args is a dic of the #args# values
    def genFunction( self, skeleton, args ):
        argsNames = []
        i = 0
        while i < (len(skeleton) - 1):
            if skeleton[i] == '#':
                argNameEnd = skeleton[i+1:].find('#')
                argName = skeleton[i:i+argNameEnd+2]
                i += argNameEnd + 1
                if argName not in argsNames:
                    argsNames.append(argName)
            i += 1
        func = skeleton[:]
        for i in argsNames:
            if i not in args:
                raise Exception('Missing arg %s (%s)' % (str(i), str(argsNames)) )
            func = func.replace(i, str(args[i]))
        return( '\n' + func + '\n')

    def filterEffects( self, s, includedSet, cutSet, excludedSet ):
        if None != cutSet:
            if ( \
                (s >= includedSet) and
                (set() != (s & cutSet)) and
                (set() == (s & excludedSet)) ):
                return True
        else:
            if ( \
                (s >= includedSet) and
                (set() == (s & excludedSet)) ):
                return True
        return False

    def getHighestTableId(self):
        self.highestTableId += 1
        return self.highestTableId

    def genCodeForEffect(self, effect, is64=False):
        pos = effect.find('_')
        if -1 == pos:
            if '' == effect:
                return ('', 'FINISH_LOG_CYCLE')
            else:
                raise Exception("Don't know how to handle effect")
        
        if is64:
            POINTER_SIZE    = 8
            POINTER_SIZE_NAME = 'QWORD'
            OUTPUT_POINTER  = 'rax'
            CODE_POINTER    = 'rbx'
            MEM_POINTER     = 'rcx'
            OFFSET_REG      = 'rdx'
            BASE_POINTER    = 'rbp'
            STACK_POINTER   = 'rsp'
            INC_EAX         = [\
                    'inc rax\n', \
                    'inc rax\ninc rax\n', \
                    'add rax, 3\n', \
                    'add rax, 4\n', \
                    'add rax, 5\n', \
                    'add rax, 6\n', \
                    'add rax, 7\n', \
                    'add rax, 8\n' ]
            ADVANCE_OUTPUT_BUFFER = ADVANCE_OUTPUT_BUFFER64
        else:
            POINTER_SIZE    = 4
            POINTER_SIZE_NAME = 'DWORD'
            OUTPUT_POINTER  = 'eax'
            CODE_POINTER    = 'ebx'
            MEM_POINTER     = 'ecx'
            STACK_POINTER   = 'esp'
            OFFSET_REG      = 'edx'
            BASE_POINTER    = 'ebp'
            INC_EAX         = [
                    'inc eax\n', \
                    'inc eax\ninc eax\n', \
                    'add eax, 3\n',
                    'add eax, 4\n' ]
            ADVANCE_OUTPUT_BUFFER = ADVANCE_OUTPUT_BUFFER32
        POINTER_SIZE_NAME = SIZE_NAME[POINTER_SIZE]

        accessSize = effect[:pos].replace('PTR', '')
        effectParts = effect.split('_')
        effectSet = set(effectParts)
        if self.filterEffects(effectSet, STACK_FILTER, None, EMPTY_FILTER):  # ex: DWORDPTR_STACK_PUSH
            if self.filterEffects(effectSet, set(['ALL32PTR']) | PUSH_FILTER, None, EMPTY_FILTER):
                self.allKindsOfEffects[effect] = None
                code = effect + '_LOG:'
                code += self.genFunction(LOG_STACK_PUSH_ALL_FUNCTION, {
                    '#OUTPUT_POINTER#'  : OUTPUT_POINTER,
                    '#ACCESS_ID#'       : ACCESSES_IDS['STACK_' + accessSize] })
                return (code, effect + '_LOG')
            elif self.filterEffects(effectSet, set(['ALL16PTR']) | PUSH_FILTER, None, EMPTY_FILTER):
                self.allKindsOfEffects[effect] = None
                code = effect + '_LOG:'
                code += self.genFunction(LOG_STACK_PUSH_ALL_16_FUNCTION, {
                    '#OUTPUT_POINTER#'  : OUTPUT_POINTER,
                    '#ACCESS_ID#'       : ACCESSES_IDS['STACK_' + accessSize] })
                return (code, effect + '_LOG')
            elif self.filterEffects(effectSet, PUSH_FILTER, None, EMPTY_FILTER):
                self.allKindsOfEffects[effect] = None
                code = effect + '_LOG:'
                code += self.genFunction(LOG_STACK_PUSH_FUNCTION, {
                    '#OUTPUT_POINTER#'      : OUTPUT_POINTER,
                    '#MEM_POINTER#'         : MEM_POINTER,
                    '#STACK_POINTER#'       : STACK_POINTER,
                    '#POINTER_SIZE#'        : POINTER_SIZE,
                    '#POINTER_SIZE_NAME#'   : POINTER_SIZE_NAME,
                    '#BASE_POINTER#'        : BASE_POINTER,
                    '#ACCESS_ID#'           : ACCESSES_IDS['STACK_' + accessSize],
                    '#ECX_PART#'            : ECX_PART_BY_MEMORY_ACCESS_SIZE[accessSize],
                    '#ACCESS_SIZE#'         : accessSize,
                    '#ADVANCE_OUTPUT_BUFFER#'       : ADVANCE_OUTPUT_BUFFER[NAME_SIZE[accessSize]] })
                return (code, effect + '_LOG')
            elif self.filterEffects(effectSet, set(['ALL32PTR']) | POP_FILTER, None, EMPTY_FILTER):
                self.allKindsOfEffects[effect] = None
                code = effect + '_LOG:'
                code += self.genFunction(LOG_STACK_POP_ALL_FUNCTION, {
                    '#OUTPUT_POINTER#'      : OUTPUT_POINTER,
                    '#POINTER_SIZE#'        : POINTER_SIZE,
                    '#POINTER_SIZE_NAME#'   : POINTER_SIZE_NAME,
                    '#ACCESS_ID#'           : ACCESSES_IDS['STACK_' + accessSize] })
                return (code, effect + '_LOG')
            elif self.filterEffects(effectSet, set(['ALL16PTR']) | POP_FILTER, None, EMPTY_FILTER):
                self.allKindsOfEffects[effect] = None
                code = effect + '_LOG:'
                code += self.genFunction(LOG_STACK_POP_ALL_16_FUNCTION, {
                    '#OUTPUT_POINTER#'      : OUTPUT_POINTER,
                    '#POINTER_SIZE#'        : POINTER_SIZE,
                    '#POINTER_SIZE_NAME#'   : POINTER_SIZE_NAME,
                    '#ACCESS_ID#'           : ACCESSES_IDS['STACK_' + accessSize] })
                return (code, effect + '_LOG')
            elif self.filterEffects(effectSet, POP_FILTER, None, EMPTY_FILTER):
                self.allKindsOfEffects[effect] = None
                code = effect + '_LOG:'
                code += self.genFunction(LOG_STACK_POP_FUNCTION, {
                    '#OUTPUT_POINTER#'          : OUTPUT_POINTER,
                    '#MEM_POINTER#'             : MEM_POINTER,
                    '#POINTER_SIZE#'            : POINTER_SIZE,
                    '#POINTER_SIZE_NAME#'       : POINTER_SIZE_NAME,
                    '#BASE_POINTER#'            : BASE_POINTER,
                    '#ACCESS_ID#'               : ACCESSES_IDS['STACK_' + accessSize],
                    '#ECX_PART#'                : ECX_PART_BY_MEMORY_ACCESS_SIZE[accessSize],
                    '#ACCESS_SIZE#'             : accessSize,
                    '#ADVANCE_OUTPUT_BUFFER#'   : ADVANCE_OUTPUT_BUFFER[NAME_SIZE[accessSize]] })
                return (code, effect + '_LOG')
            else:
                raise Exception('Stack handling missing')

        elif self.filterEffects(effectSet, SIB_FILTER, None, EMPTY_FILTER):
            if self.filterEffects(effectSet, EMPTY_FILTER, None, DISPLACEMENT_FILTER): # ex: BYTEPTR_EAX_EAX_1_SIB
                self.allKindsOfEffects[effect] = None
                baseReg     = effectParts[1]
                indexReg    = effectParts[2]
                scale       = effectParts[3]

                code = effect + '_LOG:'
                if baseReg != indexReg:
                    code += self.genFunction(LOG_SIB_MEM_FUNCTION, {
                        '#OUTPUT_POINTER#'      : OUTPUT_POINTER,
                        '#POINTER_SIZE#'        : POINTER_SIZE,
                        '#POINTER_SIZE_NAME#'   : POINTER_SIZE_NAME,
                        '#MEM_POINTER#'         : MEM_POINTER,
                        '#BASE_POINTER#'        : BASE_POINTER,
                        '#ACCESS_ID#'           : ACCESSES_IDS[accessSize],
                        '#ECX_PART#'            : ECX_PART_BY_MEMORY_ACCESS_SIZE[accessSize],
                        '#ACCESS_SIZE#'         : accessSize,
                        '#SCALE#'               : scale,
                        '#HOLD_INDEX_REG#'      : OFFSET_REG,
                        '#INDEX#'               : indexReg,
                        '#BASE#'                : baseReg,
                        '#ADVANCE_OUTPUT_BUFFER#'       : ADVANCE_OUTPUT_BUFFER[NAME_SIZE[accessSize]] })
                else:
                    code += self.genFunction(LOG_SIB_MEM_SAME_BASE_N_INDEX_FUNCTION, {
                        '#OUTPUT_POINTER#'      : OUTPUT_POINTER,
                        '#POINTER_SIZE#'        : POINTER_SIZE,
                        '#POINTER_SIZE_NAME#'   : POINTER_SIZE_NAME,
                        '#OFFSET_REG#'          : OFFSET_REG,
                        '#MEM_POINTER#'         : MEM_POINTER,
                        '#BASE_POINTER#'        : BASE_POINTER,
                        '#ACCESS_ID#'           : ACCESSES_IDS[accessSize],
                        '#ECX_PART#'            : ECX_PART_BY_MEMORY_ACCESS_SIZE[accessSize],
                        '#ACCESS_SIZE#'         : accessSize,
                        '#SCALE#'               : scale,
                        '#BASE#'                : baseReg,
                        '#ADVANCE_OUTPUT_BUFFER#'       : ADVANCE_OUTPUT_BUFFER[NAME_SIZE[accessSize]] })

                return (code, effect + '_LOG')

            elif self.filterEffects(effectSet, EMPTY_FILTER, DISPLACEMENT_FILTER, NOBASE_FILTER): # ex: BYTEPTR_DISPLACEMENT32_EAX_EAX_1_SIB
                self.allKindsOfEffects[effect] = None

                displacementSize = SIZE_NAME_OF_DISPLACEMENT[effectParts[1]]
                if False == is64:
                    if 'DWORD' != displacementSize:
                        movType = 'movsx'
                    else:
                        movType = 'mov'
                    offsetReg = OFFSET_REG
                else:
                    if 'DWORD' == displacementSize:
                        offsetReg = 'edx'
                        movType = 'mov'
                    elif 'WORD' == displacementSize:
                        offsetReg = 'edx'
                        movType = 'movsx'
                    elif 'BYTE' == displacementSize:
                        offsetReg = 'edx'
                        movType = 'movsx'
                    elif 'QWORD' == displacementSize:
                        offsetReg = 'rdx'
                        movType = 'mov'
                    else:
                        raise Exception('Invalid displacement %s' % displacementSize)

                baseReg = effectParts[2]
                indexReg = effectParts[3]
                scale = effectParts[4]

                code = effect + '_LOG:'
                if baseReg != indexReg:
                    code += self.genFunction(LOG_SIB_WITH_DISPLACEMENT_FUNCTION, {
                        '#OUTPUT_POINTER#'      : OUTPUT_POINTER,
                        '#CODE_POINTER#'        : CODE_POINTER,
                        '#POINTER_SIZE#'        : POINTER_SIZE,
                        '#POINTER_SIZE_NAME#'   : POINTER_SIZE_NAME,
                        '#OFFSET_REG#'          : offsetReg,
                        '#OFFSET_REG_FULL#'     : OFFSET_REG,
                        '#MEM_POINTER#'         : MEM_POINTER,
                        '#BASE_POINTER#'        : BASE_POINTER,
                        '#ACCESS_ID#'           : ACCESSES_IDS[accessSize],
                        '#ECX_PART#'            : ECX_PART_BY_MEMORY_ACCESS_SIZE[accessSize],
                        '#ACCESS_SIZE#'         : accessSize,
                        '#SCALE#'               : scale,
                        '#INDEX#'               : indexReg,
                        '#HOLD_INDEX_REG#'      : OFFSET_REG,
                        '#BASE#'                : baseReg,
                        '#DISPLACEMENT_SIZE#'   : displacementSize,
                        '#MOVE_TYPE#'           : movType,
                        '#ADVANCE_OUTPUT_BUFFER#'       : ADVANCE_OUTPUT_BUFFER[NAME_SIZE[accessSize]] })
                else:
                    code += self.genFunction(LOG_SIB_WITH_DISPLACEMENT_SAME_BASE_N_INDEX_FUNCTION, {
                        '#OUTPUT_POINTER#'      : OUTPUT_POINTER,
                        '#CODE_POINTER#'        : CODE_POINTER,
                        '#POINTER_SIZE#'        : POINTER_SIZE,
                        '#POINTER_SIZE_NAME#'   : POINTER_SIZE_NAME,
                        '#OFFSET_REG#'          : offsetReg,
                        '#OFFSET_REG_FULL#'     : OFFSET_REG,
                        '#MEM_POINTER#'         : MEM_POINTER,
                        '#BASE_POINTER#'        : BASE_POINTER,
                        '#ACCESS_ID#'           : ACCESSES_IDS[accessSize],
                        '#ECX_PART#'            : ECX_PART_BY_MEMORY_ACCESS_SIZE[accessSize],
                        '#ACCESS_SIZE#'         : accessSize,
                        '#SCALE#'               : scale,
                        '#BASE#'                : baseReg,
                        '#DISPLACEMENT_SIZE#'   : displacementSize,
                        '#MOVE_TYPE#'           : movType,
                        '#ADVANCE_OUTPUT_BUFFER#'       : ADVANCE_OUTPUT_BUFFER[NAME_SIZE[accessSize]] })

                return (code, effect + '_LOG')

            elif self.filterEffects(effectSet, NOBASE_FILTER, DISPLACEMENT_FILTER, EMPTY_FILTER): # ex: BYTEPTR_DISPLACEMENT32_NOBASE_EAX_1_SIB
                self.allKindsOfEffects[effect] = None

                displacementSize = SIZE_NAME_OF_DISPLACEMENT[effectParts[1]]
                if False == is64:
                    if 'DWORD' != displacementSize:
                        movType = 'movsx'
                    else:
                        movType = 'mov'
                    offsetReg = OFFSET_REG
                else:
                    if 'DWORD' == displacementSize:
                        offsetReg = 'edx'
                        movType = 'mov'
                    elif 'WORD' == displacementSize:
                        offsetReg = 'edx'
                        movType = 'movsx'
                    elif 'BYTE' == displacementSize:
                        offsetReg = 'edx'
                        movType = 'movsx'
                    elif 'QWORD' == displacementSize:
                        offsetReg = 'rdx'
                        movType = 'mov'
                    else:
                        raise Exception('Invalid displacement %s' % displacementSize)

                indexReg = effectParts[3]
                scale = effectParts[4]

                code = effect + '_LOG:'
                code += self.genFunction(LOG_SIB_WITH_DISPLACEMENT_NOBASE_FUNCTION, {
                    '#OUTPUT_POINTER#'      : OUTPUT_POINTER,
                    '#CODE_POINTER#'        : CODE_POINTER,
                    '#POINTER_SIZE#'        : POINTER_SIZE,
                    '#POINTER_SIZE_NAME#'   : POINTER_SIZE_NAME,
                    '#OFFSET_REG_FULL#'     : OFFSET_REG,
                    '#OFFSET_REG#'          : offsetReg,
                    '#MEM_POINTER#'         : MEM_POINTER,
                    '#BASE_POINTER#'        : BASE_POINTER,
                    '#ACCESS_ID#'           : ACCESSES_IDS[accessSize],
                    '#ECX_PART#'            : ECX_PART_BY_MEMORY_ACCESS_SIZE[accessSize],
                    '#ACCESS_SIZE#'         : accessSize,
                    '#SCALE#'               : scale,
                    '#INDEX#'               : indexReg,
                    '#DISPLACEMENT_SIZE#'   : displacementSize,
                    '#MOVE_TYPE#'           : movType,
                    '#ADVANCE_OUTPUT_BUFFER#'       : ADVANCE_OUTPUT_BUFFER[NAME_SIZE[accessSize]] })
                return (code, effect + '_LOG')
            else:
                raise Exception('Unhandled sib effect %s' % effect)

        elif self.filterEffects(effectSet, PLUS_FILTER, EMPTY_FILTER, EMPTY_FILTER): # BYTEPTR_BP_PLUS_DI
            # Not supported at the moment
            if effect not in self.codeMissing:
                self.codeMissing[effect] = None
            return ('', 'FINISH_LOG_CYCLE')

        elif self.filterEffects(effectSet, EMPTY_FILTER, REGISTERS_FILTER, DISPLACEMENT_FILTER): # ex: BYTEPTR_EAX
            self.allKindsOfEffects[effect] = None
            memReg = effectParts[1]
            memRegSize = SIZE_NAME[REGISTERS_SIZES[memReg]]
            memPointerPart = ECX_PART_BY_MEMORY_ACCESS_SIZE[memRegSize]
            
            code = effect + '_LOG:'
            code += self.genFunction(LOG_MOD_MEM_FUNCTION, {
                    '#OUTPUT_POINTER#'      : OUTPUT_POINTER,
                    '#POINTER_SIZE#'        : POINTER_SIZE,
                    '#POINTER_SIZE_NAME#'   : POINTER_SIZE_NAME,
                    '#MEM_POINTER#'         : MEM_POINTER,
                    '#BASE_POINTER#'        : BASE_POINTER,
                    '#ACCESS_ID#'           : ACCESSES_IDS[accessSize],
                    '#REG_SIZE#'            : memReg,
                    '#ECX_PART#'            : ECX_PART_BY_MEMORY_ACCESS_SIZE[accessSize],
                    '#MEM_POINTER_PART#'    : memPointerPart,
                    '#MEM_REG_SIZE_NAME#'   : memRegSize,
                    '#MEM_REG_OFFSET#'      : REGISTERS_OFFSETS[memReg],
                    '#ACCESS_SIZE#'         : accessSize,
                    '#ADVANCE_OUTPUT_BUFFER#'       : ADVANCE_OUTPUT_BUFFER[NAME_SIZE[accessSize]] })
            return (code, effect + '_LOG')

        elif self.filterEffects(effectSet, EMPTY_FILTER, DISPLACEMENT32_FILTER, REGISTERS_FILTER ) and False == is64:    # ex: BYTEPTR_DISPLACEMENT32
            self.allKindsOfEffects[effect] = None

            code = effect + '_LOG:'
            code += self.genFunction(LOG_DISPLACEMENT32_ONLY_FUNCTION, {
                    '#OUTPUT_POINTER#'      : OUTPUT_POINTER,
                    '#CODE_POINTER#'        : CODE_POINTER,
                    '#MEM_POINTER#'         : MEM_POINTER,
                    '#POINTER_SIZE#'        : POINTER_SIZE,
                    '#POINTER_SIZE_NAME#'   : POINTER_SIZE_NAME,
                    '#ACCESS_ID#'           : ACCESSES_IDS[accessSize],
                    '#ECX_PART#'            : ECX_PART_BY_MEMORY_ACCESS_SIZE[accessSize],
                    '#ACCESS_SIZE#'         : accessSize,
                    '#ADVANCE_OUTPUT_BUFFER#'       : ADVANCE_OUTPUT_BUFFER[NAME_SIZE[accessSize]] })
            return (code, effect + '_LOG')

        elif self.filterEffects(effectSet, EMPTY_FILTER, DISPLACEMENT32_FILTER, REGISTERS_FILTER ) and True == is64:    # ex: QWORDPTR_DISPLACEMENT32
            self.allKindsOfEffects[effect] = None
            code = effect + '_LOG:'
            code += self.genFunction(RET_CODE, {
                '#ADVANCE_OUTPUT_BUFFER#'   : '' })
            return (code, effect + '_LOG')

        elif self.filterEffects(effectSet, EMPTY_FILTER, DISPLACEMENT64_FILTER, REGISTERS_FILTER ):    # ex: BYTEPTR_DISPLACEMENT64
            if False == is64:
                raise Exception("64bit displacement is only allowed in x64")
            self.allKindsOfEffects[effect] = None

            code = effect + '_LOG:'
            code += self.genFunction(LOG_DISPLACEMENT64_ONLY_FUNCTION, {
                    '#OUTPUT_POINTER#'      : OUTPUT_POINTER,
                    '#CODE_POINTER#'        : CODE_POINTER,
                    '#MEM_POINTER#'         : MEM_POINTER,
                    '#POINTER_SIZE#'        : POINTER_SIZE,
                    '#POINTER_SIZE_NAME#'   : POINTER_SIZE_NAME,
                    '#ACCESS_ID#'           : ACCESSES_IDS[accessSize],
                    '#ECX_PART#'            : ECX_PART_BY_MEMORY_ACCESS_SIZE[accessSize],
                    '#ACCESS_SIZE#'         : accessSize,
                    '#ADVANCE_OUTPUT_BUFFER#'       : ADVANCE_OUTPUT_BUFFER[NAME_SIZE[accessSize]] })
            return (code, effect + '_LOG')

        elif self.filterEffects(effectSet, EMPTY_FILTER, DISPLACEMENT_FILTER | REGISTERS_FILTER, NOBASE_FILTER): # ex: BYTEPTR_DISPLACEMENT8_EAX
            self.allKindsOfEffects[effect] = None
            memReg = effectParts[2]
            memRegSize = SIZE_NAME[REGISTERS_SIZES[memReg]]
            memPointerPart = ECX_PART_BY_MEMORY_ACCESS_SIZE[memRegSize]
            displacementSize = SIZE_NAME_OF_DISPLACEMENT[effectParts[1]]
            if False == is64:
                if 'DWORD' != displacementSize:
                    movType = 'movsx'
                else:
                    movType = 'mov'
                offsetReg = OFFSET_REG
            else:
                if 'DWORD' == displacementSize:
                    offsetReg = 'edx'
                    movType = 'mov'
                elif 'WORD' == displacementSize:
                    offsetReg = 'edx'
                    movType = 'movsx'
                elif 'BYTE' == displacementSize:
                    offsetReg = 'edx'
                    movType = 'movsx'
                elif 'QWORD' == displacementSize:
                    offsetReg = 'rdx'
                    movType = 'mov'
                else:
                    raise Exception('Invalid displacement %s' % displacementSize)

            code = effect + '_LOG:'
            code += self.genFunction(LOG_MOD_MEM_DISPLACEMENT_FUNCTION, {
                    '#OUTPUT_POINTER#'      : OUTPUT_POINTER,
                    '#CODE_POINTER#'        : CODE_POINTER,
                    '#POINTER_SIZE#'        : POINTER_SIZE,
                    '#POINTER_SIZE_NAME#'   : POINTER_SIZE_NAME,
                    '#MEM_POINTER#'         : MEM_POINTER,
                    '#OFFSET_REG_FULL#'     : OFFSET_REG,
                    '#OFFSET_REG#'          : offsetReg,
                    '#BASE_POINTER#'        : BASE_POINTER,
                    '#ACCESS_ID#'           : ACCESSES_IDS[accessSize],
                    '#ECX_PART#'            : ECX_PART_BY_MEMORY_ACCESS_SIZE[accessSize],
                    '#ACCESS_SIZE#'         : accessSize,
                    '#MEM_POINTER_PART#'    : memPointerPart,
                    '#MEM_REG_SIZE_NAME#'   : memRegSize,
                    '#MEM_REG_OFFSET#'      : REGISTERS_OFFSETS[memReg],
                    '#DISPLACEMENT_SIZE#'   : displacementSize,
                    '#MOVE_TYPE#'           : movType,
                    '#ADVANCE_OUTPUT_BUFFER#'       : ADVANCE_OUTPUT_BUFFER[NAME_SIZE[accessSize]] })
            return (code, effect + '_LOG')

        elif self.filterEffects(effectSet, ANOTHER_POINTER_FILTER, REGISTERS_FILTER, DISPLACEMENT_FILTER ): # ex: DWORDPTR_EDI_PTR2_ESI (movsd)
            self.allKindsOfEffects[effect] = None
            memReg1 = effectParts[1]
            memReg2 = effectParts[3]

            code = effect + '_LOG:'
            code += self.genFunction(LOG_2_MEM_ACCESSES_FUNCTION, {
                    '#OUTPUT_POINTER#'      : OUTPUT_POINTER,
                    '#POINTER_SIZE#'        : POINTER_SIZE,
                    '#POINTER_SIZE_NAME#'   : POINTER_SIZE_NAME,
                    '#MEM_POINTER#'         : MEM_POINTER,
                    '#BASE_POINTER#'        : BASE_POINTER,
                    '#ACCESS_ID#'           : ACCESSES_IDS[accessSize],
                    '#ECX_PART#'            : ECX_PART_BY_MEMORY_ACCESS_SIZE[accessSize],
                    '#ACCESS_SIZE#'         : accessSize,
                    '#MEM_POINTER_PART#'    : memPointerPart,
                    '#MEM_REG1_SIZE_NAME#'  : SIZE_NAME[REGISTERS_SIZES[memReg1]],
                    '#MEM_REG2_SIZE_NAME#'  : SIZE_NAME[REGISTERS_SIZES[memReg2]],
                    '#MEM_REG1_OFFSET#'     : REGISTERS_OFFSETS[memReg1],
                    '#MEM_REG2_OFFSET#'     : REGISTERS_OFFSETS[memReg2],
                    '#INC_EAX#'             : INC_EAX[NAME_SIZE[accessSize]],
                    '#ADVANCE_OUTPUT_BUFFER#'       : ADVANCE_OUTPUT_BUFFER[NAME_SIZE[accessSize]] })
            return (code, effect + '_LOG')

        else:
            if effect not in self.codeMissing:
                self.codeMissing[effect] = None
            return ('', 'FINISH_LOG_CYCLE')

    def genJumpTable(self, table, opcode = '', is64=False):
        tableId = self.getHighestTableId()
        if is64:
            CODE_POINTER = 'rbx'
            CODE_POINTER_SIZE_NAME = 'QWORD'
            EXTRA_LOADING_CODE = "lea rdx, QWORD [TABLE_ID_%04X]" % tableId
            TABLE_NAME = 'rdx'
            ECX_MAX_SIZE = 'rcx'
        else:
            CODE_POINTER = 'ebx'
            CODE_POINTER_SIZE_NAME = 'DWORD'
            TABLE_NAME = 'TABLE_ID_%04X' % tableId
            EXTRA_LOADING_CODE = ""
            ECX_MAX_SIZE = 'ecx'
        
        code = ''
        # Gen code to jump according to table
        code += 'NEXT_BYTE_ACCORDING_TO_TABLE_%04X:' % tableId
        code += self.genFunction( NEXT_BYTE_ACCORDING_TO_TABLE_CODE, {
                        '#TABLE_NAME#'          : TABLE_NAME,
                        '#ECX_MAX_SIZE#'        : ECX_MAX_SIZE,
                        '#CODE_POINTER#'        : CODE_POINTER,
                        '#EXTRA_LOADING_CODE#'  : EXTRA_LOADING_CODE,
                        '#POINTER_SIZE_NAME#'   : CODE_POINTER_SIZE_NAME })

        jumps = []
        jumps.append( '\n\nTABLE_ID_%04X:' % tableId )
        nodeStr = ''
        for i in xrange(0x100):
            effect = table[i]
            if str == type(effect):
                # Check that we do not generate the same code twice
                if 'CONTINUE' == effect:
                    jumpTo = 'NEXT_BYTE_ACCORDING_TO_TABLE_%04X' % (tableId)
                elif 'SYSENTER' == effect:
                    jumpTo = 'WRITE_LOG_POS_AND_RET'
                elif effect not in self.allKindsOfEffects:
                    newCode, jumpTo = self.genCodeForEffect(effect, is64)
                    code += newCode
                else:
                    jumpTo = effect + '_LOG'
                if is64:
                    jumps.append( 'DQ\t%s\t; %s' % (jumpTo, (opcode + chr(i)).encode('hex')) )
                else:
                    jumps.append( 'DD\t%s\t; %s' % (jumpTo, (opcode + chr(i)).encode('hex')) )
                nodeStr += jumpTo
            elif None == effect:
                if is64:
                    jumps.append( 'DQ\tFINISH_LOG_CYCLE\t; %s' % (opcode + chr(i)).encode('hex') )
                else:
                    jumps.append( 'DD\tFINISH_LOG_CYCLE\t; %s' % (opcode + chr(i)).encode('hex') )
                nodeStr += 'FINISH_LOG_CYCLE'
            elif list == type(effect):
                c, newTableId = self.genJumpTable(effect, opcode + chr(i), is64)
                code += c
                if is64:
                    jumps.append( 'DQ\tNEXT_BYTE_ACCORDING_TO_TABLE_%04X\t; %s' % (newTableId, (opcode + chr(i)).encode('hex')) )
                else:
                    jumps.append( 'DD\tNEXT_BYTE_ACCORDING_TO_TABLE_%04X\t; %s' % (newTableId, (opcode + chr(i)).encode('hex')) )
                nodeStr += 'ACCORDING_TO_TABLE_%04X' % newTableId
            else:
                raise Exception('Unsupported effect')
        if len(jumps) != 0x101:
            raise Exception("Missing jumps in jumps table (0x%x)" % len(jumps))

        if nodeStr in self.uniqueChecker:
            # We already got this node
            tableId, cloneOpcode = self.uniqueChecker[nodeStr]
            self.opcodesWithSameEffect.append( (cloneOpcode.encode('hex'), opcode.encode('hex')) )
            return '', tableId
        self.uniqueChecker[nodeStr] = (tableId, opcode)
        self.jumpTables.append(jumps)
        return code, tableId


OreganoCodeGenerator()
endTime = time.time()
print 'DONE all', (endTime - startTime)

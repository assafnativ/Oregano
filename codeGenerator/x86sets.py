#
# x86sets.py
#
# Copyright (C) 2007 Gil Dabah, http://ragestorm.net/disops/
# This library is licensed under the BSD license. See the file COPYING.
#

#from x86header import *
execfile("x86header.py")

class Instructions:
	""" Initializes all instruction of the 80x86 CPU (includes AMD64). """

	def init_INTEGER(self):
		SetInstruction = lambda *args: self.SetInstructionCallback(ISetClass.INTEGER, *args)

		# V 1.5.13 - Pushes can be affected by operand size prefix. Segment is encoded in flags.

		# SAL is exactly like SHL, so I prefer to use the mnemonic "SHL" (below).

		SetInstruction(OpcodeLength.OL_1, [0x00], ["ADD"], [OperandType.RM8, OperandType.REG8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_1, [0x01], ["ADD"], [OperandType.RM_FULL, OperandType.REG_FULL], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_1, [0x02], ["ADD"], [OperandType.REG8, OperandType.RM8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_1, [0x03], ["ADD"], [OperandType.REG_FULL, OperandType.RM_FULL], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_1, [0x04], ["ADD"], [OperandType.ACC8, OperandType.IMM8], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x05], ["ADD"], [OperandType.ACC_FULL, OperandType.IMM_FULL], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x06], ["PUSH"], [OperandType.SEG], InstFlag.PRE_ES | InstFlag.INVALID_64BITS);
		SetInstruction(OpcodeLength.OL_1, [0x07], ["POP"], [OperandType.SEG], InstFlag.PRE_ES | InstFlag.INVALID_64BITS);
		SetInstruction(OpcodeLength.OL_1, [0x08], ["OR"], [OperandType.RM8, OperandType.REG8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_1, [0x09], ["OR"], [OperandType.RM_FULL, OperandType.REG_FULL], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_1, [0x0a], ["OR"], [OperandType.REG8, OperandType.RM8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_1, [0x0b], ["OR"], [OperandType.REG_FULL, OperandType.RM_FULL], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_1, [0x0c], ["OR"], [OperandType.ACC8, OperandType.IMM8], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x0d], ["OR"], [OperandType.ACC_FULL, OperandType.IMM_FULL], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x0e], ["PUSH"], [OperandType.SEG], InstFlag.PRE_CS | InstFlag.INVALID_64BITS);
		#SetInstruction(OpcodeLength.OL_23, [0x0f, 0x00, 0x00], ["SLDT"], [OperandType.RM_FULL], InstFlag.INCLUDE_MODRM);
		#SetInstruction(OpcodeLength.OL_23, [0x0f, 0x00, 0x01], ["STR"], [OperandType.RM16], InstFlag.INCLUDE_MODRM);
		#SetInstruction(OpcodeLength.OL_23, [0x0f, 0x00, 0x02], ["LLDT"], [OperandType.RM16], InstFlag.INCLUDE_MODRM);
		#SetInstruction(OpcodeLength.OL_23, [0x0f, 0x00, 0x03], ["LTR"], [OperandType.RM16], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		#SetInstruction(OpcodeLength.OL_23, [0x0f, 0x00, 0x04], ["VERR"], [OperandType.RM16], InstFlag.INCLUDE_MODRM);
		#SetInstruction(OpcodeLength.OL_23, [0x0f, 0x00, 0x05], ["VERW"], [OperandType.RM16], InstFlag.INCLUDE_MODRM);
		#SetInstruction(OpcodeLength.OL_2d, [0x0f, 0x01, 0x00], ["SGDT"], [OperandType.MEM16_3264], InstFlag.INCLUDE_MODRM);
		#SetInstruction(OpcodeLength.OL_2d, [0x0f, 0x01, 0x01], ["SIDT"], [OperandType.MEM16_3264], InstFlag.INCLUDE_MODRM | InstFlag._64BITS);
		#SetInstruction(OpcodeLength.OL_2d, [0x0f, 0x01, 0x02], ["LGDT"], [OperandType.MEM16_3264], InstFlag.INCLUDE_MODRM | InstFlag._64BITS);
		#SetInstruction(OpcodeLength.OL_2d, [0x0f, 0x01, 0x03], ["LIDT"], [OperandType.MEM16_3264], InstFlag.INCLUDE_MODRM | InstFlag._64BITS);

		# These two instructions need the whole byte, means they use the whole third byte and are NOT divided.
		# We'll recognize them by their 3 REG bits in their third byte.
		#SetInstruction(OpcodeLength.OL_2d, [0x0f, 0x01, 0x04], ["SMSW"], [OperandType.RFULL_M16], InstFlag.INCLUDE_MODRM | InstFlag.NOT_DIVIDED);
		#SetInstruction(OpcodeLength.OL_2d, [0x0f, 0x01, 0x06], ["LMSW"], [OperandType.RM16], InstFlag.INCLUDE_MODRM | InstFlag.NOT_DIVIDED);

		#SetInstruction(OpcodeLength.OL_2d, [0x0f, 0x01, 0x07], ["INVLPG"], [OperandType.MEM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		#SetInstruction(OpcodeLength.OL_2d, [0x0f, 0x01, 0xc8], ["MONITOR"], [], InstFlag._32BITS);
		#SetInstruction(OpcodeLength.OL_2d, [0x0f, 0x01, 0xc9], ["MWAIT"], [], InstFlag._32BITS);
		#SetInstruction(OpcodeLength.OL_2d, [0x0f, 0x01, 0xf8], ["SWAPGS"], [], InstFlag._64BITS_FETCH);
		#SetInstruction(OpcodeLength.OL_2d, [0x0f, 0x01, 0xf9], ["RDTSCP"], [], InstFlag._64BITS_FETCH);
		#SetInstruction(OpcodeLength.OL_2, [0x0f, 0x02], ["LAR"], [OperandType.REG_FULL, OperandType.RM16], InstFlag.INCLUDE_MODRM);
		#SetInstruction(OpcodeLength.OL_2, [0x0f, 0x03], ["LSL"], [OperandType.REG_FULL, OperandType.RM16], InstFlag.INCLUDE_MODRM);
		#SetInstruction(OpcodeLength.OL_2, [0x0f, 0x06], ["CLTS"], [], InstFlag._32BITS);
		#SetInstruction(OpcodeLength.OL_2, [0x0f, 0x08], ["INVD"], [], InstFlag._32BITS);
		#SetInstruction(OpcodeLength.OL_2, [0x0f, 0x09], ["WBINVD"], [], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x0b], ["UD2"], [], InstFlag._32BITS);

		# MOV: In 64 bits decoding mode REG is 64 bits by default.
		#SetInstruction(OpcodeLength.OL_2, [0x0f, 0x20], ["MOV"], [OperandType.FREG32_64_RM, OperandType.CREG], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.MODRR | InstFlag._64BITS);
		#SetInstruction(OpcodeLength.OL_2, [0x0f, 0x21], ["MOV"], [OperandType.FREG32_64_RM, OperandType.DREG], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.MODRR | InstFlag._64BITS);
		#SetInstruction(OpcodeLength.OL_2, [0x0f, 0x22], ["MOV"], [OperandType.CREG, OperandType.FREG32_64_RM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.MODRR | InstFlag._64BITS);
		#SetInstruction(OpcodeLength.OL_2, [0x0f, 0x23], ["MOV"], [OperandType.DREG, OperandType.FREG32_64_RM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.MODRR | InstFlag._64BITS);
		#SetInstruction(OpcodeLength.OL_2, [0x0f, 0x30], ["WRMSR"], [], InstFlag._32BITS);
		#SetInstruction(OpcodeLength.OL_2, [0x0f, 0x31], ["RDTSC"], [], InstFlag._32BITS);
		#SetInstruction(OpcodeLength.OL_2, [0x0f, 0x32], ["RDMSR"], [], InstFlag._32BITS);
		#SetInstruction(OpcodeLength.OL_2, [0x0f, 0x33], ["RDPMC"], [], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x80], ["JO"], [OperandType.RELC_FULL], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x81], ["JNO"], [OperandType.RELC_FULL], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x82], ["JB"], [OperandType.RELC_FULL], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x83], ["JAE"], [OperandType.RELC_FULL], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x84], ["JZ"], [OperandType.RELC_FULL], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x85], ["JNZ"], [OperandType.RELC_FULL], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x86], ["JBE"], [OperandType.RELC_FULL], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x87], ["JA"], [OperandType.RELC_FULL], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x88], ["JS"], [OperandType.RELC_FULL], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x89], ["JNS"], [OperandType.RELC_FULL], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x8a], ["JP"], [OperandType.RELC_FULL], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x8b], ["JNP"], [OperandType.RELC_FULL], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x8c], ["JL"], [OperandType.RELC_FULL], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x8d], ["JGE"], [OperandType.RELC_FULL], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x8e], ["JLE"], [OperandType.RELC_FULL], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x8f], ["JG"], [OperandType.RELC_FULL], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x90], ["SETO"], [OperandType.RM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x91], ["SETNO"], [OperandType.RM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x92], ["SETB"], [OperandType.RM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x93], ["SETAE"], [OperandType.RM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x94], ["SETZ"], [OperandType.RM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x95], ["SETNZ"], [OperandType.RM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x96], ["SETBE"], [OperandType.RM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x97], ["SETA"], [OperandType.RM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x98], ["SETS"], [OperandType.RM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x99], ["SETNS"], [OperandType.RM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x9a], ["SETP"], [OperandType.RM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x9b], ["SETNP"], [OperandType.RM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x9c], ["SETL"], [OperandType.RM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x9d], ["SETGE"], [OperandType.RM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x9e], ["SETLE"], [OperandType.RM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x9f], ["SETG"], [OperandType.RM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xa0], ["PUSH"], [OperandType.SEG], InstFlag._32BITS | InstFlag.PRE_FS | InstFlag._64BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xa1], ["POP"], [OperandType.SEG], InstFlag._32BITS | InstFlag.PRE_FS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xa2], ["CPUID"], [], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xa3], ["BT"], [OperandType.RM_FULL, OperandType.REG_FULL], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xa4], ["SHLD"], [OperandType.RM_FULL, OperandType.REG_FULL, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.USE_OP3);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xa5], ["SHLD"], [OperandType.RM_FULL, OperandType.REG_FULL, OperandType.REGCL], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.USE_OP3);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xa8], ["PUSH"], [OperandType.SEG], InstFlag._32BITS | InstFlag.PRE_GS | InstFlag._64BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xa9], ["POP"], [OperandType.SEG], InstFlag._32BITS | InstFlag.PRE_GS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xaa], ["RSM"], [], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xab], ["BTS"], [OperandType.RM_FULL, OperandType.REG_FULL], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xac], ["SHRD"], [OperandType.RM_FULL, OperandType.REG_FULL, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.USE_OP3);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xad], ["SHRD"], [OperandType.RM_FULL, OperandType.REG_FULL, OperandType.REGCL], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.USE_OP3);
		SetInstruction(OpcodeLength.OL_2d, [0x0f, 0xae, 0x00], ["FXSAVE"], [OperandType.MEM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2d, [0x0f, 0xae, 0x01], ["FXRSTOR"], [OperandType.MEM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2d, [0x0f, 0xae, 0x02], ["LDMXCSR"], [OperandType.MEM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2d, [0x0f, 0xae, 0x03], ["STMXCSR"], [OperandType.MEM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2d, [0x0f, 0xae, 0x07], ["CLFLUSH"], [OperandType.MEM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2d, [0x0f, 0xae, 0xe8], ["LFENCE"], [], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2d, [0x0f, 0xae, 0xf0], ["MFENCE"], [], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2d, [0x0f, 0xae, 0xf8], ["SFENCE"], [], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xaf], ["IMUL"], [OperandType.REG_FULL, OperandType.RM_FULL], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xb0], ["CMPXCHG"], [OperandType.RM8, OperandType.REG8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xb1], ["CMPXCHG"], [OperandType.RM_FULL, OperandType.REG_FULL], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xb2], ["LSS"], [OperandType.REG_FULL, OperandType.MEM16_FULL], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._64BITS | InstFlag.PRE_REX);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xb3], ["BTR"], [OperandType.RM_FULL, OperandType.REG_FULL], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xb4], ["LFS"], [OperandType.REG_FULL, OperandType.MEM16_FULL], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._64BITS | InstFlag.PRE_REX);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xb5], ["LGS"], [OperandType.REG_FULL, OperandType.MEM16_FULL], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._64BITS | InstFlag.PRE_REX);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xb6], ["MOVZX"], [OperandType.REG_FULL, OperandType.RM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xb7], ["MOVZX"], [OperandType.REG_FULL, OperandType.RM16], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._64BITS | InstFlag.PRE_REX);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xb9], ["UD2"], [], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_23, [0x0f, 0xba, 0x04], ["BT"], [OperandType.RM_FULL, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_23, [0x0f, 0xba, 0x05], ["BTS"], [OperandType.RM_FULL, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_23, [0x0f, 0xba, 0x06], ["BTR"], [OperandType.RM_FULL, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_23, [0x0f, 0xba, 0x07], ["BTC"], [OperandType.RM_FULL, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xbb], ["BTC"], [OperandType.RM_FULL, OperandType.REG_FULL], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xbc], ["BSF"], [OperandType.REG_FULL, OperandType.RM_FULL], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xbd], ["BSR"], [OperandType.REG_FULL, OperandType.RM_FULL], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);

		# V 1.1.6 MOVSX/MOVZX now support 16bits regs.
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xbe], ["MOVSX"], [OperandType.REG_FULL, OperandType.RM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xbf], ["MOVSX"], [OperandType.REG_FULL, OperandType.RM16], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._64BITS | InstFlag.PRE_REX);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xc0], ["XADD"], [OperandType.RM8, OperandType.REG8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xc1], ["XADD"], [OperandType.RM_FULL, OperandType.REG_FULL], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_23, [0x0f, 0xc7, 0x01], ["CMPXCHG8B", "", "CMPXCHG16B"], [OperandType.MEM64_128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.PRE_LOCK | InstFlag._64BITS | InstFlag.PRE_REX | InstFlag.USE_EXMNEMONIC2);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xc8], ["BSWAP"], [OperandType.IB_R_DW_QW], InstFlag._32BITS | InstFlag._64BITS | InstFlag.PRE_REX | InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1, [0x10], ["ADC"], [OperandType.RM8, OperandType.REG8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_1, [0x11], ["ADC"], [OperandType.RM_FULL, OperandType.REG_FULL], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_1, [0x12], ["ADC"], [OperandType.REG8, OperandType.RM8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_1, [0x13], ["ADC"], [OperandType.REG_FULL, OperandType.RM_FULL], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_1, [0x14], ["ADC"], [OperandType.ACC8, OperandType.IMM8], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x15], ["ADC"], [OperandType.ACC_FULL, OperandType.IMM_FULL], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x16], ["PUSH"], [OperandType.SEG], InstFlag.PRE_SS | InstFlag.INVALID_64BITS);
		SetInstruction(OpcodeLength.OL_1, [0x17], ["POP"], [OperandType.SEG], InstFlag.PRE_SS | InstFlag.INVALID_64BITS);
		SetInstruction(OpcodeLength.OL_1, [0x18], ["SBB"], [OperandType.RM8, OperandType.REG8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_1, [0x19], ["SBB"], [OperandType.RM_FULL, OperandType.REG_FULL], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_1, [0x1a], ["SBB"], [OperandType.REG8, OperandType.RM8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_1, [0x1b], ["SBB"], [OperandType.REG_FULL, OperandType.RM_FULL], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_1, [0x1c], ["SBB"], [OperandType.ACC8, OperandType.IMM8], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x1d], ["SBB"], [OperandType.ACC_FULL, OperandType.IMM_FULL], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x1e], ["PUSH"], [OperandType.SEG], InstFlag.PRE_DS | InstFlag.INVALID_64BITS);
		SetInstruction(OpcodeLength.OL_1, [0x1f], ["POP"], [OperandType.SEG], InstFlag.PRE_DS | InstFlag.INVALID_64BITS);
		SetInstruction(OpcodeLength.OL_1, [0x20], ["AND"], [OperandType.RM8, OperandType.REG8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_1, [0x21], ["AND"], [OperandType.RM_FULL, OperandType.REG_FULL], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_1, [0x22], ["AND"], [OperandType.REG8, OperandType.RM8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_1, [0x23], ["AND"], [OperandType.REG_FULL, OperandType.RM_FULL], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_1, [0x24], ["AND"], [OperandType.ACC8, OperandType.IMM8], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x25], ["AND"], [OperandType.ACC_FULL, OperandType.IMM_FULL], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x27], ["DAA"], [], InstFlag.INVALID_64BITS);
		SetInstruction(OpcodeLength.OL_1, [0x28], ["SUB"], [OperandType.RM8, OperandType.REG8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_1, [0x29], ["SUB"], [OperandType.RM_FULL, OperandType.REG_FULL], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_1, [0x2a], ["SUB"], [OperandType.REG8, OperandType.RM8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_1, [0x2b], ["SUB"], [OperandType.REG_FULL, OperandType.RM_FULL], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_1, [0x2c], ["SUB"], [OperandType.ACC8, OperandType.IMM8], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x2d], ["SUB"], [OperandType.ACC_FULL, OperandType.IMM_FULL], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x2f], ["DAS"], [], InstFlag.INVALID_64BITS);
		SetInstruction(OpcodeLength.OL_1, [0x30], ["XOR"], [OperandType.RM8, OperandType.REG8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_1, [0x31], ["XOR"], [OperandType.RM_FULL, OperandType.REG_FULL], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_1, [0x32], ["XOR"], [OperandType.REG8, OperandType.RM8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_1, [0x33], ["XOR"], [OperandType.REG_FULL, OperandType.RM_FULL], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_1, [0x34], ["XOR"], [OperandType.ACC8, OperandType.IMM8], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x35], ["XOR"], [OperandType.ACC_FULL, OperandType.IMM_FULL], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x37], ["AAA"], [], InstFlag.INVALID_64BITS);
		SetInstruction(OpcodeLength.OL_1, [0x38], ["CMP"], [OperandType.RM8, OperandType.REG8], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x39], ["CMP"], [OperandType.RM_FULL, OperandType.REG_FULL], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x3a], ["CMP"], [OperandType.REG8, OperandType.RM8], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x3b], ["CMP"], [OperandType.REG_FULL, OperandType.RM_FULL], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x3c], ["CMP"], [OperandType.ACC8, OperandType.IMM8], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x3d], ["CMP"], [OperandType.ACC_FULL, OperandType.IMM_FULL], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x3f], ["AAS"], [], InstFlag.INVALID_64BITS);
		SetInstruction(OpcodeLength.OL_1, [0x40], ["INC"], [OperandType.IB_R_FULL], InstFlag.INVALID_64BITS | InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1, [0x48], ["DEC"], [OperandType.IB_R_FULL], InstFlag.INVALID_64BITS | InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1, [0x50], ["PUSH"], [OperandType.IB_R_FULL], InstFlag._64BITS | InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1, [0x58], ["POP"], [OperandType.IB_R_FULL], InstFlag._64BITS | InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1, [0x60], ["PUSHA"], [], InstFlag.NATIVE | InstFlag.INVALID_64BITS);
		SetInstruction(OpcodeLength.OL_1, [0x61], ["POPA"], [], InstFlag.NATIVE | InstFlag.INVALID_64BITS);
		SetInstruction(OpcodeLength.OL_1, [0x62], ["BOUND"], [OperandType.REG_FULL, OperandType.MEM], InstFlag.INCLUDE_MODRM | InstFlag.INVALID_64BITS);

		# Notes for diStorm:
		# 63 /R
		# 16/32: ARPL reg/mem16, reg16
		# 64: MOVSXD reg64, reg/mem32 OT_REG64, OT_RM32
		# Damn processor, my DB won't support mixing of operands types.
		# Therefore this instruction will be defined in x86defs and returned in the locate_inst according to the decoding type.
		# This is because I must not change the DB, otherwise the code isn't multi-threaded compliant!
		# I combine DB with Code in Waitable instructions also...
		# This InstInfo is unused! x86defs.c uses its own. We just allocate it here so it exists in DB.

		SetInstruction(OpcodeLength.OL_1, [0x63], ["ARPL"], [OperandType.RM16, OperandType.REG16], InstFlag.INCLUDE_MODRM | InstFlag._64BITS);
		SetInstruction(OpcodeLength.OL_1, [0x68], ["PUSH"], [OperandType.IMM_FULL], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x69], ["IMUL"], [OperandType.REG_FULL, OperandType.RM_FULL, OperandType.IMM_FULL], InstFlag.INCLUDE_MODRM | InstFlag.USE_OP3);
		SetInstruction(OpcodeLength.OL_1, [0x6a], ["PUSH"], [OperandType.SEIMM8], InstFlag.PRE_OP_SIZE);
		SetInstruction(OpcodeLength.OL_1, [0x6b], ["IMUL"], [OperandType.REG_FULL, OperandType.RM_FULL, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag.USE_OP3);
		# V 1.5.14 - String instructions aren't supposed to be promoted automatically in 64bits, only with a REX prefix.
		# In 64 bits INS/OUTS still supports only 8/16/32 bits.
		SetInstruction(OpcodeLength.OL_1, [0x6c], ["INS"], [OperandType.REGI_EDI, OperandType.REGDX], InstFlag.PRE_REPNZ | InstFlag.PRE_REP | InstFlag.PRE_ES);
		SetInstruction(OpcodeLength.OL_1, [0x6d], ["INS"], [OperandType.REGI_EDI, OperandType.REGDX], InstFlag._16BITS | InstFlag.PRE_REPNZ | InstFlag.PRE_REP | InstFlag.PRE_ES);
		SetInstruction(OpcodeLength.OL_1, [0x6e], ["OUTS"], [OperandType.REGDX, OperandType.REGI_ESI], InstFlag.PRE_REPNZ | InstFlag.PRE_REP | InstFlag.PRE_DS);
		SetInstruction(OpcodeLength.OL_1, [0x6f], ["OUTS"], [OperandType.REGDX, OperandType.REGI_ESI], InstFlag._16BITS | InstFlag.PRE_REPNZ | InstFlag.PRE_REP | InstFlag.PRE_DS);
		SetInstruction(OpcodeLength.OL_1, [0x70], ["JO"], [OperandType.RELCB], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x71], ["JNO"], [OperandType.RELCB], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x72], ["JB"], [OperandType.RELCB], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x73], ["JAE"], [OperandType.RELCB], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x74], ["JZ"], [OperandType.RELCB], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x75], ["JNZ"], [OperandType.RELCB], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x76], ["JBE"], [OperandType.RELCB], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x77], ["JA"], [OperandType.RELCB], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x78], ["JS"], [OperandType.RELCB], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x79], ["JNS"], [OperandType.RELCB], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x7a], ["JP"], [OperandType.RELCB], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x7b], ["JNP"], [OperandType.RELCB], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x7c], ["JL"], [OperandType.RELCB], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x7d], ["JGE"], [OperandType.RELCB], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x7e], ["JLE"], [OperandType.RELCB], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x7f], ["JG"], [OperandType.RELCB], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0x80, 0x00], ["ADD"], [OperandType.RM8, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_13, [0x80, 0x01], ["OR"], [OperandType.RM8, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_13, [0x80, 0x02], ["ADC"], [OperandType.RM8, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_13, [0x80, 0x03], ["SBB"], [OperandType.RM8, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_13, [0x80, 0x04], ["AND"], [OperandType.RM8, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_13, [0x80, 0x05], ["SUB"], [OperandType.RM8, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_13, [0x80, 0x06], ["XOR"], [OperandType.RM8, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_13, [0x80, 0x07], ["CMP"], [OperandType.RM8, OperandType.IMM8], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0x81, 0x00], ["ADD"], [OperandType.RM_FULL, OperandType.IMM_FULL], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_13, [0x81, 0x01], ["OR"], [OperandType.RM_FULL, OperandType.IMM_FULL], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_13, [0x81, 0x02], ["ADC"], [OperandType.RM_FULL, OperandType.IMM_FULL], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_13, [0x81, 0x03], ["SBB"], [OperandType.RM_FULL, OperandType.IMM_FULL], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_13, [0x81, 0x04], ["AND"], [OperandType.RM_FULL, OperandType.IMM_FULL], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_13, [0x81, 0x05], ["SUB"], [OperandType.RM_FULL, OperandType.IMM_FULL], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_13, [0x81, 0x06], ["XOR"], [OperandType.RM_FULL, OperandType.IMM_FULL], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_13, [0x81, 0x07], ["CMP"], [OperandType.RM_FULL, OperandType.IMM_FULL], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0x82, 0x00], ["ADD"], [OperandType.RM8, OperandType.SEIMM8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK | InstFlag.INVALID_64BITS);
		SetInstruction(OpcodeLength.OL_13, [0x82, 0x01], ["OR"], [OperandType.RM8, OperandType.SEIMM8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK | InstFlag.INVALID_64BITS);
		SetInstruction(OpcodeLength.OL_13, [0x82, 0x02], ["ADC"], [OperandType.RM8, OperandType.SEIMM8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK | InstFlag.INVALID_64BITS);
		SetInstruction(OpcodeLength.OL_13, [0x82, 0x03], ["SBB"], [OperandType.RM8, OperandType.SEIMM8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK | InstFlag.INVALID_64BITS);
		SetInstruction(OpcodeLength.OL_13, [0x82, 0x04], ["AND"], [OperandType.RM8, OperandType.SEIMM8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK | InstFlag.INVALID_64BITS);
		SetInstruction(OpcodeLength.OL_13, [0x82, 0x05], ["SUB"], [OperandType.RM8, OperandType.SEIMM8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK | InstFlag.INVALID_64BITS);
		SetInstruction(OpcodeLength.OL_13, [0x82, 0x06], ["XOR"], [OperandType.RM8, OperandType.SEIMM8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK | InstFlag.INVALID_64BITS);
		SetInstruction(OpcodeLength.OL_13, [0x82, 0x07], ["CMP"], [OperandType.RM8, OperandType.SEIMM8], InstFlag.INCLUDE_MODRM | InstFlag.INVALID_64BITS);
		SetInstruction(OpcodeLength.OL_13, [0x83, 0x00], ["ADD"], [OperandType.RM_FULL, OperandType.SEIMM8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_13, [0x83, 0x01], ["OR"], [OperandType.RM_FULL, OperandType.SEIMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_13, [0x83, 0x02], ["ADC"], [OperandType.RM_FULL, OperandType.SEIMM8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_13, [0x83, 0x03], ["SBB"], [OperandType.RM_FULL, OperandType.SEIMM8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_13, [0x83, 0x04], ["AND"], [OperandType.RM_FULL, OperandType.SEIMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_13, [0x83, 0x05], ["SUB"], [OperandType.RM_FULL, OperandType.SEIMM8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_13, [0x83, 0x06], ["XOR"], [OperandType.RM_FULL, OperandType.SEIMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_13, [0x83, 0x07], ["CMP"], [OperandType.RM_FULL, OperandType.SEIMM8], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x84], ["TEST"], [OperandType.RM8, OperandType.REG8], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x85], ["TEST"], [OperandType.RM_FULL, OperandType.REG_FULL], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x86], ["XCHG"], [OperandType.RM8, OperandType.REG8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_1, [0x87], ["XCHG"], [OperandType.RM_FULL, OperandType.REG_FULL], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_1, [0x88], ["MOV"], [OperandType.RM8, OperandType.REG8], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x89], ["MOV"], [OperandType.RM_FULL, OperandType.REG_FULL], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x8a], ["MOV"], [OperandType.REG8, OperandType.RM8], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x8b], ["MOV"], [OperandType.REG_FULL, OperandType.RM_FULL], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x8c], ["MOV"], [OperandType.RFULL_M16, OperandType.SREG], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x8d], ["LEA"], [OperandType.REG_FULL, OperandType.MEM], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x8e], ["MOV"], [OperandType.SREG, OperandType.RM16], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0x8f, 0x00], ["POP"], [OperandType.RM_FULL], InstFlag.INCLUDE_MODRM | InstFlag._64BITS);
		SetInstruction(OpcodeLength.OL_1, [0x90], ["NOP"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x91], ["XCHG"], [OperandType.IB_R_FULL, OperandType.ACC_FULL], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x92], ["XCHG"], [OperandType.IB_R_FULL, OperandType.ACC_FULL], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x93], ["XCHG"], [OperandType.IB_R_FULL, OperandType.ACC_FULL], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x94], ["XCHG"], [OperandType.IB_R_FULL, OperandType.ACC_FULL], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x95], ["XCHG"], [OperandType.IB_R_FULL, OperandType.ACC_FULL], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x96], ["XCHG"], [OperandType.IB_R_FULL, OperandType.ACC_FULL], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x97], ["XCHG"], [OperandType.IB_R_FULL, OperandType.ACC_FULL], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x98], ["CBW", "CWDE", "CDQE"], [], InstFlag.USE_EXMNEMONIC | InstFlag.USE_EXMNEMONIC2);
		SetInstruction(OpcodeLength.OL_1, [0x99], ["CWD", "CDQ", "CQO"], [], InstFlag.USE_EXMNEMONIC | InstFlag.USE_EXMNEMONIC2);
		SetInstruction(OpcodeLength.OL_1, [0x9a], ["CALL FAR"], [OperandType.PTR16_FULL], InstFlag.INVALID_64BITS);

		# V 1.4.a PUSHF/POPF are supposed to be promoted to 64 bits, without a REX.
		SetInstruction(OpcodeLength.OL_1, [0x9c], ["PUSHF"], [], InstFlag.NATIVE | InstFlag._64BITS);
		SetInstruction(OpcodeLength.OL_1, [0x9d], ["POPF"], [], InstFlag.NATIVE | InstFlag._64BITS);
		SetInstruction(OpcodeLength.OL_1, [0x9e], ["SAHF"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0x9f], ["LAHF"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0xa0], ["MOV"], [OperandType.ACC8, OperandType.MOFFS], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0xa1], ["MOV"], [OperandType.ACC_FULL, OperandType.MOFFS], InstFlag._16BITS | InstFlag._32BITS | InstFlag._64BITS);
		SetInstruction(OpcodeLength.OL_1, [0xa2], ["MOV"], [OperandType.MOFFS, OperandType.ACC8], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0xa3], ["MOV"], [OperandType.MOFFS, OperandType.ACC_FULL], InstFlag._16BITS | InstFlag._32BITS | InstFlag._64BITS);
		SetInstruction(OpcodeLength.OL_1, [0xa4], ["MOVS"], [OperandType.REGI_EDI], InstFlag.PRE_REPNZ | InstFlag.PRE_REP | InstFlag.PRE_ES);
		SetInstruction(OpcodeLength.OL_1, [0xa5], ["MOVS"], [OperandType.REGI_EDI], InstFlag._16BITS | InstFlag.PRE_REPNZ | InstFlag.PRE_REP | InstFlag.PRE_ES | InstFlag._64BITS | InstFlag.PRE_REX);
		SetInstruction(OpcodeLength.OL_1, [0xa6], ["CMPS"], [OperandType.REGI_ESI], InstFlag.PRE_REPNZ | InstFlag.PRE_REP | InstFlag.PRE_ES);
		SetInstruction(OpcodeLength.OL_1, [0xa7], ["CMPS"], [OperandType.REGI_ESI], InstFlag._16BITS | InstFlag.PRE_REPNZ | InstFlag.PRE_REP | InstFlag.PRE_ES | InstFlag._64BITS | InstFlag.PRE_REX);
		SetInstruction(OpcodeLength.OL_1, [0xa8], ["TEST"], [OperandType.ACC8, OperandType.IMM8], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0xa9], ["TEST"], [OperandType.ACC_FULL, OperandType.IMM_FULL], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0xaa], ["STOS"], [OperandType.REGI_EDI], InstFlag.PRE_REPNZ | InstFlag.PRE_REP | InstFlag.PRE_ES);
		SetInstruction(OpcodeLength.OL_1, [0xab], ["STOS"], [OperandType.REGI_EDI], InstFlag._16BITS | InstFlag.PRE_REPNZ | InstFlag.PRE_REP | InstFlag.PRE_ES | InstFlag._64BITS | InstFlag.PRE_REX);
		SetInstruction(OpcodeLength.OL_1, [0xac], ["LODS"], [OperandType.REGI_ESI], InstFlag.PRE_REPNZ | InstFlag.PRE_REP | InstFlag.PRE_DS);
		SetInstruction(OpcodeLength.OL_1, [0xad], ["LODS"], [OperandType.REGI_ESI], InstFlag._16BITS | InstFlag.PRE_REPNZ | InstFlag.PRE_REP | InstFlag.PRE_DS | InstFlag._64BITS | InstFlag.PRE_REX);
		SetInstruction(OpcodeLength.OL_1, [0xae], ["SCAS"], [OperandType.REGI_EDI], InstFlag.PRE_REPNZ | InstFlag.PRE_REP | InstFlag.PRE_ES);
		SetInstruction(OpcodeLength.OL_1, [0xaf], ["SCAS"], [OperandType.REGI_EDI], InstFlag._16BITS | InstFlag.PRE_REPNZ | InstFlag.PRE_REP | InstFlag.PRE_ES | InstFlag._64BITS | InstFlag.PRE_REX);
		SetInstruction(OpcodeLength.OL_1, [0xb0], ["MOV"], [OperandType.IB_RB, OperandType.IMM8], InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1, [0xb8], ["MOV"], [OperandType.IB_R_FULL, OperandType.IMM_FULL], InstFlag._64BITS | InstFlag.PRE_REX | InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_13, [0xc0, 0x00], ["ROL"], [OperandType.RM8, OperandType.IMM8], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xc0, 0x01], ["ROR"], [OperandType.RM8, OperandType.IMM8], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xc0, 0x02], ["RCL"], [OperandType.RM8, OperandType.IMM8], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xc0, 0x03], ["RCR"], [OperandType.RM8, OperandType.IMM8], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xc0, 0x04], ["SHL"], [OperandType.RM8, OperandType.IMM8], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xc0, 0x05], ["SHR"], [OperandType.RM8, OperandType.IMM8], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xc0, 0x06], ["SAL"], [OperandType.RM8, OperandType.IMM8], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xc0, 0x07], ["SAR"], [OperandType.RM8, OperandType.IMM8], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xc1, 0x00], ["ROL"], [OperandType.RM_FULL, OperandType.IMM8], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xc1, 0x01], ["ROR"], [OperandType.RM_FULL, OperandType.IMM8], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xc1, 0x02], ["RCL"], [OperandType.RM_FULL, OperandType.IMM8], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xc1, 0x03], ["RCR"], [OperandType.RM_FULL, OperandType.IMM8], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xc1, 0x04], ["SHL"], [OperandType.RM_FULL, OperandType.IMM8], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xc1, 0x05], ["SHR"], [OperandType.RM_FULL, OperandType.IMM8], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xc1, 0x06], ["SAL"], [OperandType.RM_FULL, OperandType.IMM8], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xc1, 0x07], ["SAR"], [OperandType.RM_FULL, OperandType.IMM8], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0xc2], ["RET"], [OperandType.IMM16], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0xc3], ["RET"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0xc4], ["LES"], [OperandType.REG_FULL, OperandType.MEM16_FULL], InstFlag.INCLUDE_MODRM | InstFlag.INVALID_64BITS);
		SetInstruction(OpcodeLength.OL_1, [0xc5], ["LDS"], [OperandType.REG_FULL, OperandType.MEM16_FULL], InstFlag.INCLUDE_MODRM | InstFlag.INVALID_64BITS);
		SetInstruction(OpcodeLength.OL_13, [0xc6, 0x00], ["MOV"], [OperandType.RM8, OperandType.IMM8], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xc7, 0x00], ["MOV"], [OperandType.RM_FULL, OperandType.IMM_FULL], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0xc8], ["ENTER"], [OperandType.IMM16, OperandType.IMM8], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0xc9], ["LEAVE"], [], InstFlag.EXCLUDE_MODRM);

		# V 1.1.6 RETF is NOT promoted automatically in 64bits. So with REX it should be RETFQ.
		SetInstruction(OpcodeLength.OL_1, [0xca], ["RETF"], [OperandType.IMM16], InstFlag.NATIVE | InstFlag._64BITS | InstFlag.PRE_REX);
		SetInstruction(OpcodeLength.OL_1, [0xcb], ["RETF"], [], InstFlag.NATIVE | InstFlag._64BITS | InstFlag.PRE_REX);
		SetInstruction(OpcodeLength.OL_1, [0xcc], ["INT 3"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0xcd], ["INT"], [OperandType.IMM8], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0xce], ["INTO"], [], InstFlag.INVALID_64BITS);
		SetInstruction(OpcodeLength.OL_1, [0xcf], ["IRET"], [], InstFlag.NATIVE | InstFlag._64BITS | InstFlag.PRE_REX);
		SetInstruction(OpcodeLength.OL_13, [0xd0, 0x00], ["ROL"], [OperandType.RM8, OperandType.CONST1], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xd0, 0x01], ["ROR"], [OperandType.RM8, OperandType.CONST1], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xd0, 0x02], ["RCL"], [OperandType.RM8, OperandType.CONST1], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xd0, 0x03], ["RCR"], [OperandType.RM8, OperandType.CONST1], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xd0, 0x04], ["SHL"], [OperandType.RM8, OperandType.CONST1], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xd0, 0x05], ["SHR"], [OperandType.RM8, OperandType.CONST1], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xd0, 0x06], ["SAL"], [OperandType.RM8, OperandType.CONST1], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xd0, 0x07], ["SAR"], [OperandType.RM8, OperandType.CONST1], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xd1, 0x00], ["ROL"], [OperandType.RM_FULL, OperandType.CONST1], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xd1, 0x01], ["ROR"], [OperandType.RM_FULL, OperandType.CONST1], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xd1, 0x02], ["RCL"], [OperandType.RM_FULL, OperandType.CONST1], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xd1, 0x03], ["RCR"], [OperandType.RM_FULL, OperandType.CONST1], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xd1, 0x04], ["SHL"], [OperandType.RM_FULL, OperandType.CONST1], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xd1, 0x05], ["SHR"], [OperandType.RM_FULL, OperandType.CONST1], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xd1, 0x06], ["SAL"], [OperandType.RM_FULL, OperandType.CONST1], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xd1, 0x07], ["SAR"], [OperandType.RM_FULL, OperandType.CONST1], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xd2, 0x00], ["ROL"], [OperandType.RM8, OperandType.REGCL], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xd2, 0x01], ["ROR"], [OperandType.RM8, OperandType.REGCL], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xd2, 0x02], ["RCL"], [OperandType.RM8, OperandType.REGCL], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xd2, 0x03], ["RCR"], [OperandType.RM8, OperandType.REGCL], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xd2, 0x04], ["SHL"], [OperandType.RM8, OperandType.REGCL], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xd2, 0x05], ["SHR"], [OperandType.RM8, OperandType.REGCL], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xd2, 0x06], ["SAL"], [OperandType.RM8, OperandType.REGCL], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xd2, 0x07], ["SAR"], [OperandType.RM8, OperandType.REGCL], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xd3, 0x00], ["ROL"], [OperandType.RM_FULL, OperandType.REGCL], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xd3, 0x01], ["ROR"], [OperandType.RM_FULL, OperandType.REGCL], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xd3, 0x02], ["RCL"], [OperandType.RM_FULL, OperandType.REGCL], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xd3, 0x03], ["RCR"], [OperandType.RM_FULL, OperandType.REGCL], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xd3, 0x04], ["SHL"], [OperandType.RM_FULL, OperandType.REGCL], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xd3, 0x05], ["SHR"], [OperandType.RM_FULL, OperandType.REGCL], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xd3, 0x06], ["SAL"], [OperandType.RM_FULL, OperandType.REGCL], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xd3, 0x07], ["SAR"], [OperandType.RM_FULL, OperandType.REGCL], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0xd4], ["AAM"], [OperandType.IMM_AADM], InstFlag.INVALID_64BITS);
		SetInstruction(OpcodeLength.OL_1, [0xd5], ["AAD"], [OperandType.IMM_AADM], InstFlag.INVALID_64BITS);
		SetInstruction(OpcodeLength.OL_1, [0xd6], ["SALC"], [], InstFlag.INVALID_64BITS);

		# XLATB / XLAT BYTE PTR DS:[EBX + AL]
		SetInstruction(OpcodeLength.OL_1, [0xd7], ["XLAT"], [OperandType.REGI_EBXAL], InstFlag.PRE_DS);

		# LOOPxx are also affected by the ADDRESS-SIZE prefix!
		# But they require a suffix letter indicating their size.
		# LOOPxx are promoted to 64bits.
		SetInstruction(OpcodeLength.OL_1, [0xe0], ["LOOPNZ"], [OperandType.RELCB], InstFlag.PRE_ADDR_SIZE | InstFlag.NATIVE);
		SetInstruction(OpcodeLength.OL_1, [0xe1], ["LOOPZ"], [OperandType.RELCB], InstFlag.PRE_ADDR_SIZE | InstFlag.NATIVE);
		SetInstruction(OpcodeLength.OL_1, [0xe2], ["LOOP"], [OperandType.RELCB], InstFlag.PRE_ADDR_SIZE | InstFlag.NATIVE);

		# JMP CX:
		# This is a special instruction, because the ADDRESS-SIZE prefix affects its register size!!!
		# INST_PRE_ADDR_SIZE isn't supposed to really be a flag of a static instruction, it's quite a hack to distinguish this instruction.
		# J(r/e)CXZ are promoted to 64bits.
		SetInstruction(OpcodeLength.OL_1, [0xe3], ["JCXZ", "JECXZ", "JRCXZ"], [OperandType.RELCB], InstFlag.PRE_ADDR_SIZE | InstFlag.USE_EXMNEMONIC | InstFlag.USE_EXMNEMONIC2);
		SetInstruction(OpcodeLength.OL_1, [0xe4], ["IN"], [OperandType.ACC8, OperandType.IMM8], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0xe5], ["IN"], [OperandType.ACC_FULL_NOT64, OperandType.IMM8], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0xe6], ["OUT"], [OperandType.IMM8, OperandType.ACC8], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0xe7], ["OUT"], [OperandType.IMM8, OperandType.ACC_FULL_NOT64], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0xe8], ["CALL"], [OperandType.RELC_FULL], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0xe9], ["JMP"], [OperandType.RELC_FULL], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0xea], ["JMP FAR"], [OperandType.PTR16_FULL], InstFlag.INVALID_64BITS);
		SetInstruction(OpcodeLength.OL_1, [0xeb], ["JMP"], [OperandType.RELCB], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0xec], ["IN AL, DX"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0xed], ["IN"], [OperandType.ACC_FULL_NOT64, OperandType.REGDX], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0xee], ["OUT DX, AL"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0xef], ["OUT"], [OperandType.REGDX, OperandType.ACC_FULL_NOT64], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0xf1], ["INT1"], [], InstFlag.EXCLUDE_MODRM);
		#SetInstruction(OpcodeLength.OL_1, [0xf4], ["HLT"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0xf5], ["CMC"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xf6, 0x00], ["TEST"], [OperandType.RM8, OperandType.IMM8], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xf6, 0x02], ["NOT"], [OperandType.RM8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_13, [0xf6, 0x03], ["NEG"], [OperandType.RM8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_13, [0xf6, 0x04], ["MUL"], [OperandType.RM8], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xf6, 0x05], ["IMUL"], [OperandType.RM8], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xf6, 0x06], ["DIV"], [OperandType.RM8], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xf6, 0x07], ["IDIV"], [OperandType.RM8], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xf7, 0x00], ["TEST"], [OperandType.RM_FULL, OperandType.IMM_FULL], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xf7, 0x02], ["NOT"], [OperandType.RM_FULL], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_13, [0xf7, 0x03], ["NEG"], [OperandType.RM_FULL], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_13, [0xf7, 0x04], ["MUL"], [OperandType.RM_FULL], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xf7, 0x05], ["IMUL"], [OperandType.RM_FULL], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xf7, 0x06], ["DIV"], [OperandType.RM_FULL], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xf7, 0x07], ["IDIV"], [OperandType.RM_FULL], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0xf8], ["CLC"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0xf9], ["STC"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0xfa], ["CLI"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0xfb], ["STI"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0xfc], ["CLD"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1, [0xfd], ["STD"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_13, [0xfe, 0x00], ["INC"], [OperandType.RM8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_13, [0xfe, 0x01], ["DEC"], [OperandType.RM8], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_13, [0xff, 0x00], ["INC"], [OperandType.RM_FULL], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_13, [0xff, 0x01], ["DEC"], [OperandType.RM_FULL], InstFlag.INCLUDE_MODRM | InstFlag.PRE_LOCK);
		SetInstruction(OpcodeLength.OL_13, [0xff, 0x02], ["CALL"], [OperandType.RM_FULL, OperandType.DUMMY], InstFlag.INCLUDE_MODRM | InstFlag._64BITS);
		SetInstruction(OpcodeLength.OL_13, [0xff, 0x03], ["CALL FAR"], [OperandType.MEM16_FULL], InstFlag.INCLUDE_MODRM | InstFlag._64BITS | InstFlag.PRE_REX);
		SetInstruction(OpcodeLength.OL_13, [0xff, 0x04], ["JMP"], [OperandType.RM_FULL, OperandType.DUMMY], InstFlag.INCLUDE_MODRM | InstFlag._64BITS);
		SetInstruction(OpcodeLength.OL_13, [0xff, 0x05], ["JMP FAR"], [OperandType.MEM16_FULL], InstFlag.INCLUDE_MODRM | InstFlag._64BITS | InstFlag.PRE_REX);
		SetInstruction(OpcodeLength.OL_13, [0xff, 0x06], ["PUSH"], [OperandType.RM_FULL], InstFlag.INCLUDE_MODRM | InstFlag._64BITS);

	def init_FPU(self):
		SetInstruction = lambda *args: self.SetInstructionCallback(ISetClass.FPU, *args)


		# The WAIT instruction is tricky, it starts a 3 bytes instruction series.
		# If you find a 3 bytes long instruction you are on your own.
		# But the problem is that if you don't find a 3 bytes long instruction and the first byte that is going to be DB'ed
		# is this 0x9b byte, which represents the WAIT instruction, thus you'll have to output it as a standalone instruction.
		# Example:
		# 9B DB E3 ~ FINIT
		# 9B DB E4 ~ WAIT; DB 0xDB; ...
		# Get the idea?
		# It might be a part of a long instruction (3 bytes), else it just a simple one byte instruction by its own.
		# This way is a simple rule which is broken easily when dealing with Trie DB, the whole point is that the byte says
		# "read another byte" or "I'm your one", but here both happens.
		# That's why I will have to hardcode the WAIT instruction in the decode function which DB'es unknown bytes.
		# SetInstruction(0x9b, "WAIT") ....

		SetInstruction(OpcodeLength.OL_23, [0x9b, 0xd9, 0x06], ["FSTENV"], [OperandType.MEM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_23, [0x9b, 0xd9, 0x07], ["FSTCW"], [OperandType.MEM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x9b, 0xdb, 0xe2], ["FCLEX"], [], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x9b, 0xdb, 0xe3], ["FINIT"], [], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_23, [0x9b, 0xdd, 0x06], ["FSAVE"], [OperandType.MEM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_23, [0x9b, 0xdd, 0x07], ["FSTSW"], [OperandType.MEM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x9b, 0xdf, 0xe0], ["FSTSW AX"], [], InstFlag._32BITS);


		SetInstruction(OpcodeLength.OL_1d, [0xd8, 0x00], ["FADD"], [OperandType.FPUM32], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd8, 0x01], ["FMUL"], [OperandType.FPUM32], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd8, 0x02], ["FCOM"], [OperandType.FPUM32], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd8, 0x03], ["FCOMP"], [OperandType.FPUM32], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd8, 0x04], ["FSUB"], [OperandType.FPUM32], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd8, 0x05], ["FSUBR"], [OperandType.FPUM32], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd8, 0x06], ["FDIV"], [OperandType.FPUM32], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd8, 0x07], ["FDIVR"], [OperandType.FPUM32], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd8, 0xc0], ["FADD"], [OperandType.FPU_SSI], InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xd8, 0xc8], ["FMUL"], [OperandType.FPU_SSI], InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xd8, 0xd0], ["FCOM"], [OperandType.FPU_SI], InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xd8, 0xd8], ["FCOMP"], [OperandType.FPU_SI], InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xd8, 0xd9], ["FCOMP"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd8, 0xe0], ["FSUB"], [OperandType.FPU_SSI], InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xd8, 0xe8], ["FSUBR"], [OperandType.FPU_SSI], InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xd8, 0xf0], ["FDIV"], [OperandType.FPU_SSI], InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xd8, 0xf8], ["FDIVR"], [OperandType.FPU_SSI], InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0x00], ["FLD"], [OperandType.FPUM32], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0x02], ["FST"], [OperandType.FPUM32], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0x03], ["FSTP"], [OperandType.FPUM32], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0x04], ["FLDENV"], [OperandType.MEM], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0x05], ["FLDCW"], [OperandType.MEM], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0x06], ["FNSTENV"], [OperandType.MEM], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0x07], ["FNSTCW"], [OperandType.MEM], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0xc0], ["FLD"], [OperandType.FPU_SI], InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0xc8], ["FXCH"], [OperandType.FPU_SI], InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0xc9], ["FXCH"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0xd0], ["FNOP"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0xe0], ["FCHS"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0xe1], ["FABS"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0xe4], ["FTST"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0xe5], ["FXAM"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0xe8], ["FLD1"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0xe9], ["FLDL2T"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0xea], ["FLDL2E"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0xeb], ["FLDPI"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0xec], ["FLDLG2"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0xed], ["FLDLN2"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0xee], ["FLDZ"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0xf0], ["F2XM1"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0xf1], ["FYL2X"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0xf2], ["FPTAN"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0xf3], ["FPATAN"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0xf4], ["FXTRACT"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0xf5], ["FPREM1"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0xf6], ["FDECSTP"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0xf7], ["FINCSTP"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0xf8], ["FPREM"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0xf9], ["FYL2XP1"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0xfa], ["FSQRT"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0xfb], ["FSINCOS"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0xfc], ["FRNDINT"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0xfd], ["FSCALE"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0xfe], ["FSIN"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xd9, 0xff], ["FCOS"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xda, 0x00], ["FIADD"], [OperandType.FPUM32], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xda, 0x01], ["FIMUL"], [OperandType.FPUM32], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xda, 0x02], ["FICOM"], [OperandType.FPUM32], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xda, 0x03], ["FICOMP"], [OperandType.FPUM32], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xda, 0x04], ["FISUB"], [OperandType.FPUM32], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xda, 0x05], ["FISUBR"], [OperandType.FPUM32], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xda, 0x06], ["FIDIV"], [OperandType.FPUM32], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xda, 0x07], ["FIDIVR"], [OperandType.FPUM32], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xda, 0xe9], ["FUCOMPP"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xdb, 0x00], ["FILD"], [OperandType.FPUM32], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xdb, 0x02], ["FIST"], [OperandType.FPUM32], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xdb, 0x03], ["FISTP"], [OperandType.FPUM32], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xdb, 0x05], ["FLD"], [OperandType.FPUM80], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xdb, 0x07], ["FSTP"], [OperandType.FPUM80], InstFlag.INCLUDE_MODRM);

		# Obsolete.
		SetInstruction(OpcodeLength.OL_1d, [0xdb, 0xe0], ["FENI"], [], InstFlag.EXCLUDE_MODRM);

		# Obsolete.
		SetInstruction(OpcodeLength.OL_1d, [0xdb, 0xe1], ["FEDISI"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xdb, 0xe2], ["FNCLEX"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xdb, 0xe3], ["FNINIT"], [], InstFlag.EXCLUDE_MODRM);

		# Obsolete.
		SetInstruction(OpcodeLength.OL_1d, [0xdb, 0xe4], ["FSETPM"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xdb, 0xe8], ["FUCOMI"], [OperandType.FPU_SSI], InstFlag._32BITS | InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xdc, 0x00], ["FADD"], [OperandType.FPUM64], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xdc, 0x01], ["FMUL"], [OperandType.FPUM64], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xdc, 0x02], ["FCOM"], [OperandType.FPUM64], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xdc, 0x03], ["FCOMP"], [OperandType.FPUM64], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xdc, 0x04], ["FSUB"], [OperandType.FPUM64], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xdc, 0x05], ["FSUBR"], [OperandType.FPUM64], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xdc, 0x06], ["FDIV"], [OperandType.FPUM64], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xdc, 0x07], ["FDIVR"], [OperandType.FPUM64], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xdc, 0xc0], ["FADD"], [OperandType.FPU_SIS], InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xdc, 0xc8], ["FMUL"], [OperandType.FPU_SIS], InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xdc, 0xe0], ["FSUBR"], [OperandType.FPU_SIS], InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xdc, 0xe8], ["FSUB"], [OperandType.FPU_SIS], InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xdc, 0xf0], ["FDIVR"], [OperandType.FPU_SIS], InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xdc, 0xf8], ["FDIV"], [OperandType.FPU_SIS], InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xdd, 0x00], ["FLD"], [OperandType.FPUM64], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xdd, 0x02], ["FST"], [OperandType.FPUM64], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xdd, 0x03], ["FSTP"], [OperandType.FPUM64], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xdd, 0x04], ["FRSTOR"], [OperandType.MEM], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xdd, 0x06], ["FNSAVE"], [OperandType.MEM], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xdd, 0x07], ["FNSTSW"], [OperandType.MEM], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xdd, 0xc0], ["FFREE"], [OperandType.FPU_SI], InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xdd, 0xd0], ["FST"], [OperandType.FPU_SI], InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xdd, 0xd8], ["FSTP"], [OperandType.FPU_SI], InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xdd, 0xe0], ["FUCOM"], [OperandType.FPU_SIS], InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xdd, 0xe1], ["FUCOM"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xdd, 0xe8], ["FUCOMP"], [OperandType.FPU_SI], InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xdd, 0xe9], ["FUCOMP"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xde, 0x00], ["FIADD"], [OperandType.FPUM16], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xde, 0x01], ["FIMUL"], [OperandType.FPUM16], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xde, 0x02], ["FICOM"], [OperandType.FPUM16], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xde, 0x03], ["FICOMP"], [OperandType.FPUM16], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xde, 0x04], ["FISUB"], [OperandType.FPUM16], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xde, 0x05], ["FISUBR"], [OperandType.FPUM16], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xde, 0x06], ["FIDIV"], [OperandType.FPUM16], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xde, 0x07], ["FIDIVR"], [OperandType.FPUM16], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xde, 0xc0], ["FADDP"], [OperandType.FPU_SIS], InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xde, 0xc1], ["FADDP"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xde, 0xc8], ["FMULP"], [OperandType.FPU_SIS], InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xde, 0xc9], ["FMULP"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xde, 0xd9], ["FCOMPP"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xde, 0xe0], ["FSUBRP"], [OperandType.FPU_SIS], InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xde, 0xe1], ["FSUBRP"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xde, 0xe8], ["FSUBP"], [OperandType.FPU_SIS], InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xde, 0xe9], ["FSUBP"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xde, 0xf0], ["FDIVRP"], [OperandType.FPU_SIS], InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xde, 0xf1], ["FDIVRP"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xde, 0xf8], ["FDIVP"], [OperandType.FPU_SIS], InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xde, 0xf9], ["FDIVP"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xdf, 0x00], ["FILD"], [OperandType.FPUM16], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xdf, 0x02], ["FIST"], [OperandType.FPUM16], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xdf, 0x03], ["FISTP"], [OperandType.FPUM16], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xdf, 0x04], ["FBLD"], [OperandType.FPUM80], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xdf, 0x05], ["FILD"], [OperandType.FPUM64], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xdf, 0x06], ["FBSTP"], [OperandType.FPUM80], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xdf, 0x07], ["FISTP"], [OperandType.FPUM64], InstFlag.INCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xdf, 0xe0], ["FNSTSW AX"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_1d, [0xdf, 0xe8], ["FUCOMIP"], [OperandType.FPU_SSI], InstFlag._32BITS | InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xdf, 0xf0], ["FCOMIP"], [OperandType.FPU_SSI], InstFlag._32BITS | InstFlag.GEN_BLOCK);

	def init_P6(self):
		SetInstruction = lambda *args: self.SetInstructionCallback(ISetClass.P6, *args)
		#SetInstruction(OpcodeLength.OL_2, [0x0f, 0x05], ["SYSCALL"], [], InstFlag._32BITS);
		#SetInstruction(OpcodeLength.OL_2, [0x0f, 0x07], ["SYSRET"], [], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x34], ["SYSENTER"], [], InstFlag._32BITS | InstFlag.INVALID_64BITS);
		#SetInstruction(OpcodeLength.OL_2, [0x0f, 0x35], ["SYSEXIT"], [], InstFlag._32BITS | InstFlag.INVALID_64BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x40], ["CMOVO"], [OperandType.REG_FULL, OperandType.RM_FULL], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x41], ["CMOVNO"], [OperandType.REG_FULL, OperandType.RM_FULL], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x42], ["CMOVB"], [OperandType.REG_FULL, OperandType.RM_FULL], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x43], ["CMOVAE"], [OperandType.REG_FULL, OperandType.RM_FULL], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x44], ["CMOVZ"], [OperandType.REG_FULL, OperandType.RM_FULL], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x45], ["CMOVNZ"], [OperandType.REG_FULL, OperandType.RM_FULL], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x46], ["CMOVBE"], [OperandType.REG_FULL, OperandType.RM_FULL], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x47], ["CMOVA"], [OperandType.REG_FULL, OperandType.RM_FULL], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x48], ["CMOVS"], [OperandType.REG_FULL, OperandType.RM_FULL], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x49], ["CMOVNS"], [OperandType.REG_FULL, OperandType.RM_FULL], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x4a], ["CMOVP"], [OperandType.REG_FULL, OperandType.RM_FULL], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x4b], ["CMOVNP"], [OperandType.REG_FULL, OperandType.RM_FULL], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x4c], ["CMOVL"], [OperandType.REG_FULL, OperandType.RM_FULL], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x4d], ["CMOVGE"], [OperandType.REG_FULL, OperandType.RM_FULL], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x4e], ["CMOVLE"], [OperandType.REG_FULL, OperandType.RM_FULL], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x4f], ["CMOVG"], [OperandType.REG_FULL, OperandType.RM_FULL], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_1d, [0xda, 0xc0], ["FCMOVB"], [OperandType.FPU_SSI], InstFlag._32BITS | InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xda, 0xc8], ["FCMOVE"], [OperandType.FPU_SSI], InstFlag._32BITS | InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xda, 0xd0], ["FCMOVBE"], [OperandType.FPU_SSI], InstFlag._32BITS | InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xda, 0xd8], ["FCMOVU"], [OperandType.FPU_SSI], InstFlag._32BITS | InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xdb, 0xc0], ["FCMOVNB"], [OperandType.FPU_SSI], InstFlag._32BITS | InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xdb, 0xc8], ["FCMOVNE"], [OperandType.FPU_SSI], InstFlag._32BITS | InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xdb, 0xd0], ["FCMOVNBE"], [OperandType.FPU_SSI], InstFlag._32BITS | InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xdb, 0xd8], ["FCMOVNU"], [OperandType.FPU_SSI], InstFlag._32BITS | InstFlag.GEN_BLOCK);
		SetInstruction(OpcodeLength.OL_1d, [0xdb, 0xf0], ["FCOMI"], [OperandType.FPU_SSI], InstFlag._32BITS | InstFlag.GEN_BLOCK);

	def init_MMX(self):
		SetInstruction = lambda *args: self.SetInstructionCallback(ISetClass.MMX, *args)

		# Pseudo Opcodes, the second mnemonic is concatenated to the first mnemonic.

		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x60], ["PUNPCKLBW"], [OperandType.MM, OperandType.MM32], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x61], ["PUNPCKLWD"], [OperandType.MM, OperandType.MM32], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x62], ["PUNPCKLDQ"], [OperandType.MM, OperandType.MM32], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x63], ["PACKSSWB"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x64], ["PCMPGTB"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x65], ["PCMPGTW"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x66], ["PCMPGTD"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x67], ["PACKUSWB"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x68], ["PUNPCKHBW"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x69], ["PUNPCKHWD"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x6a], ["PUNPCKHDQ"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x6b], ["PACKSSDW"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x6e], ["MOVD"], [OperandType.MM, OperandType.RM32_64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._64BITS | InstFlag.PRE_REX);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x6f], ["MOVQ"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_23, [0x0f, 0x71, 0x02], ["PSRLW"], [OperandType.MM_RM, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.MODRR);
		SetInstruction(OpcodeLength.OL_23, [0x0f, 0x71, 0x04], ["PSRAW"], [OperandType.MM_RM, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.MODRR);
		SetInstruction(OpcodeLength.OL_23, [0x0f, 0x71, 0x06], ["PSLLW"], [OperandType.MM_RM, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.MODRR);
		SetInstruction(OpcodeLength.OL_23, [0x0f, 0x72, 0x02], ["PSRLD"], [OperandType.MM_RM, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.MODRR);
		SetInstruction(OpcodeLength.OL_23, [0x0f, 0x72, 0x04], ["PSRAD"], [OperandType.MM_RM, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.MODRR);
		SetInstruction(OpcodeLength.OL_23, [0x0f, 0x72, 0x06], ["PSLLD"], [OperandType.MM_RM, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.MODRR);
		SetInstruction(OpcodeLength.OL_23, [0x0f, 0x73, 0x02], ["PSRLQ"], [OperandType.MM_RM, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.MODRR);
		SetInstruction(OpcodeLength.OL_23, [0x0f, 0x73, 0x06], ["PSLLQ"], [OperandType.MM_RM, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.MODRR);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x74], ["PCMPEQB"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x75], ["PCMPEQW"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x76], ["PCMPEQD"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x77], ["EMMS"], [], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x7e], ["MOVD"], [OperandType.RM32_64, OperandType.MM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._64BITS | InstFlag.PRE_REX);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x7f], ["MOVQ"], [OperandType.MM64, OperandType.MM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xd1], ["PSRLW"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xd2], ["PSRLD"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xd3], ["PSRLQ"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xd5], ["PMULLW"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xd8], ["PSUBUSB"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xd9], ["PSUBUSW"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xdb], ["PAND"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xdc], ["PADDUSB"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xdd], ["PADDUSW"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xdf], ["PANDN"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xe1], ["PSRAW"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xe2], ["PSRAD"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xe5], ["PMULHW"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xe8], ["PSUBSB"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xe9], ["PSUBSW"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xeb], ["POR"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xec], ["PADDSB"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xed], ["PADDSW"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xef], ["PXOR"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xf1], ["PSLLW"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xf2], ["PSLLD"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xf3], ["PSLLQ"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xf5], ["PMADDWD"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xf8], ["PSUBB"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xf9], ["PSUBW"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xfa], ["PSUBD"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xfc], ["PADDB"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xfd], ["PADDW"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xfe], ["PADDD"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);

	def init_SSE(self):
		SetInstruction = lambda *args: self.SetInstructionCallback(ISetClass.SSE, *args)
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x10], ["MOVUPS"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x11], ["MOVUPS"], [OperandType.XMM128, OperandType.XMM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);

		# The problem with these instructions (MOVHLPS/MOVLHPS) is that both kinds need partialy the ModR/M byte.
		# mod=11 for first mnemonic.

		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x12], ["MOVHLPS", "MOVLPS"], [OperandType.XMM, OperandType.XMM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.USE_EXMNEMONIC | InstFlag.MODRM_BASED);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x13], ["MOVLPS"], [OperandType.MEM64, OperandType.XMM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x14], ["UNPCKLPS"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x15], ["UNPCKHPS"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x16], ["MOVLHPS", "MOVHPS"], [OperandType.XMM, OperandType.XMM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.USE_EXMNEMONIC | InstFlag.MODRM_BASED);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x17], ["MOVHPS"], [OperandType.MEM64, OperandType.XMM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_23, [0x0f, 0x18, 0x00], ["PREFETCHNTA"], [OperandType.MEM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_23, [0x0f, 0x18, 0x01], ["PREFETCHT0"], [OperandType.MEM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_23, [0x0f, 0x18, 0x02], ["PREFETCHT1"], [OperandType.MEM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_23, [0x0f, 0x18, 0x03], ["PREFETCHT2"], [OperandType.MEM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x28], ["MOVAPS"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x29], ["MOVAPS"], [OperandType.XMM128, OperandType.XMM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x2a], ["CVTPI2PS"], [OperandType.XMM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x2b], ["MOVNTPS"], [OperandType.MEM128, OperandType.XMM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x2c], ["CVTTPS2PI"], [OperandType.MM, OperandType.XMM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x2d], ["CVTPS2PI"], [OperandType.MM, OperandType.XMM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x2e], ["UCOMISS"], [OperandType.XMM, OperandType.XMM32], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x2f], ["COMISS"], [OperandType.XMM, OperandType.XMM32], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x50], ["MOVMSKPS"], [OperandType.REG32, OperandType.XMM_RM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.MODRR);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x51], ["SQRTPS"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x52], ["RSQRTPS"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x53], ["RCPPS"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x54], ["ANDPS"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x55], ["ANDNPS"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x56], ["ORPS"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x57], ["XORPS"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x58], ["ADDPS"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x59], ["MULPS"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x5c], ["SUBPS"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x5d], ["MINPS"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x5e], ["DIVPS"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x5f], ["MAXPS"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x70], ["PSHUFW"], [OperandType.MM, OperandType.MM64, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.USE_OP3);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xc2], ["CMP", "PS"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.USE_EXMNEMONIC | InstFlag.PSEUDO_OPCODE);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xc4], ["PINSRW"], [OperandType.MM, OperandType.R32M16, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.USE_OP3);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xc5], ["PEXTRW"], [OperandType.REG32, OperandType.MM_RM, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.USE_OP3 | InstFlag.MODRR);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xc6], ["SHUFPS"], [OperandType.XMM, OperandType.XMM128, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.USE_OP3);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xd7], ["PMOVMSKB"], [OperandType.REG32, OperandType.MM_RM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.MODRR);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xda], ["PMINUB"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xde], ["PMAXUB"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xe0], ["PAVGB"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xe3], ["PAVGW"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xe4], ["PMULHUW"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xe7], ["MOVNTQ"], [OperandType.MEM64, OperandType.MM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xea], ["PMINSW"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xee], ["PMAXSW"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xf6], ["PSADBW"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xf7], ["MASKMOVQ"], [OperandType.MM, OperandType.MM_RM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.MODRR);
		SetInstruction(OpcodeLength.OL_3, [0xf3, 0x0f, 0x10], ["MOVSS"], [OperandType.XMM, OperandType.XMM32], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf3, 0x0f, 0x11], ["MOVSS"], [OperandType.XMM32, OperandType.XMM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf3, 0x0f, 0x2a], ["CVTSI2SS"], [OperandType.XMM, OperandType.RM32_64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._64BITS | InstFlag.PRE_REX);
		SetInstruction(OpcodeLength.OL_3, [0xf3, 0x0f, 0x2c], ["CVTTSS2SI"], [OperandType.REG32_64, OperandType.XMM32], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._64BITS | InstFlag.PRE_REX);
		SetInstruction(OpcodeLength.OL_3, [0xf3, 0x0f, 0x2d], ["CVTSS2SI"], [OperandType.REG32_64, OperandType.XMM32], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._64BITS | InstFlag.PRE_REX);
		SetInstruction(OpcodeLength.OL_3, [0xf3, 0x0f, 0x51], ["SQRTSS"], [OperandType.XMM, OperandType.XMM32], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf3, 0x0f, 0x52], ["RSQRTSS"], [OperandType.XMM, OperandType.XMM32], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf3, 0x0f, 0x53], ["RCPSS"], [OperandType.XMM, OperandType.XMM32], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf3, 0x0f, 0x58], ["ADDSS"], [OperandType.XMM, OperandType.XMM32], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf3, 0x0f, 0x59], ["MULSS"], [OperandType.XMM, OperandType.XMM32], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf3, 0x0f, 0x5c], ["SUBSS"], [OperandType.XMM, OperandType.XMM32], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf3, 0x0f, 0x5d], ["MINSS"], [OperandType.XMM, OperandType.XMM32], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf3, 0x0f, 0x5e], ["DIVSS"], [OperandType.XMM, OperandType.XMM32], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf3, 0x0f, 0x5f], ["MAXSS"], [OperandType.XMM, OperandType.XMM32], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf3, 0x0f, 0xc2], ["CMP", "SS"], [OperandType.XMM, OperandType.XMM32], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.USE_EXMNEMONIC | InstFlag.PSEUDO_OPCODE);

	def init_SSE2(self):
		SetInstruction = lambda *args: self.SetInstructionCallback(ISetClass.SSE2, *args)
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x5a], ["CVTPS2PD"], [OperandType.XMM, OperandType.XMM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x5b], ["CVTDQ2PS"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xc3], ["MOVNTI"], [OperandType.RM32_64, OperandType.REG32_64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._64BITS | InstFlag.PRE_REX);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xd4], ["PADDQ"], [OperandType.XMM, OperandType.XMM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xf4], ["PMULUDQ"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0xfb], ["PSUBQ"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x10], ["MOVUPD"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x11], ["MOVUPD"], [OperandType.XMM128, OperandType.XMM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x12], ["MOVLPD"], [OperandType.XMM, OperandType.MEM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x13], ["MOVLPD"], [OperandType.MEM64, OperandType.XMM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x14], ["UNPCKLPD"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x15], ["UNPCKHPD"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x16], ["MOVHPD"], [OperandType.XMM, OperandType.MEM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x17], ["MOVHPD"], [OperandType.MEM64, OperandType.XMM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x28], ["MOVAPD"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x29], ["MOVAPD"], [OperandType.XMM128, OperandType.XMM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x2a], ["CVTPI2PD"], [OperandType.XMM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x2b], ["MOVNTPD"], [OperandType.MEM128, OperandType.XMM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.MODRR);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x2c], ["CVTTPD2PI"], [OperandType.MM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x2d], ["CVTPD2PI"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x2e], ["UCOMISD"], [OperandType.XMM, OperandType.XMM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x2f], ["COMISD"], [OperandType.XMM, OperandType.XMM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x50], ["MOVMSKPD"], [OperandType.REG32, OperandType.XMM_RM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.MODRR);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x51], ["SQRTPD"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x54], ["ANDPD"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x55], ["ANDNPD"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x56], ["ORPD"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x57], ["XORPD"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x58], ["ADDPD"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x59], ["MULPD"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x5a], ["CVTPD2PS"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x5b], ["CVTPS2DQ"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x5c], ["SUBPD"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x5d], ["MINPD"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x5e], ["DIVPD"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x5f], ["MAXPD"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x60], ["PUNPCKLBW"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x61], ["PUNPCKLWD"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x62], ["PUNPCKLDQ"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x63], ["PACKSSWB"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x64], ["PCMPGTB"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x65], ["PCMPGTW"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x66], ["PCMPGTD"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x67], ["PACKUSWB"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x68], ["PUNPCKHBW"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x69], ["PUNPCKHWD"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x6a], ["PUNPCKHDQ"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x6b], ["PACKSSDW"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x6c], ["PUNPCKLQDQ"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x6d], ["PUNPCKHQDQ"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x6e], ["MOVD"], [OperandType.XMM, OperandType.RM32_64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._64BITS | InstFlag.PRE_REX);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x6f], ["MOVDQA"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x70], ["PSHUFD"], [OperandType.XMM, OperandType.XMM128, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.USE_OP3);
		SetInstruction(OpcodeLength.OL_33, [0x66, 0x0f, 0x71, 0x02], ["PSRLW"], [OperandType.XMM_RM, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_33, [0x66, 0x0f, 0x71, 0x04], ["PSRAW"], [OperandType.XMM_RM, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_33, [0x66, 0x0f, 0x71, 0x06], ["PSLLW"], [OperandType.XMM_RM, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_33, [0x66, 0x0f, 0x72, 0x02], ["PSRLD"], [OperandType.XMM_RM, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_33, [0x66, 0x0f, 0x72, 0x04], ["PSRAD"], [OperandType.XMM_RM, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_33, [0x66, 0x0f, 0x72, 0x06], ["PSLLD"], [OperandType.XMM_RM, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_33, [0x66, 0x0f, 0x73, 0x02], ["PSRLQ"], [OperandType.XMM_RM, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_33, [0x66, 0x0f, 0x73, 0x03], ["PSRLDQ"], [OperandType.XMM_RM, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_33, [0x66, 0x0f, 0x73, 0x06], ["PSLLQ"], [OperandType.XMM_RM, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_33, [0x66, 0x0f, 0x73, 0x07], ["PSLLDQ"], [OperandType.XMM_RM, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x74], ["PCMPEQB"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x75], ["PCMPEQW"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x76], ["PCMPEQD"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x7e], ["MOVD"], [OperandType.RM32_64, OperandType.XMM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._64BITS | InstFlag.PRE_REX);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x7f], ["MOVDQA"], [OperandType.XMM128, OperandType.XMM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xc2], ["CMP", "PD"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.USE_EXMNEMONIC | InstFlag.PSEUDO_OPCODE);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xc4], ["PINSRW"], [OperandType.XMM, OperandType.R32M16, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.USE_OP3 | InstFlag.MODRR);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xc5], ["PEXTRW"], [OperandType.REG32, OperandType.XMM_RM, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.USE_OP3 | InstFlag.MODRR);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xc6], ["SHUFPD"], [OperandType.XMM, OperandType.XMM128, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.USE_OP3);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xd1], ["PSRLW"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xd2], ["PSRLD"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xd3], ["PSRLQ"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xd4], ["PADDQ"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xd5], ["PMULLW"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xd6], ["MOVQ"], [OperandType.XMM64, OperandType.XMM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xd7], ["PMOVMSKB"], [OperandType.REG32, OperandType.XMM_RM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.MODRR);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xd8], ["PSUBUSB"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xd9], ["PSUBUSW"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xda], ["PMINUB"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xdb], ["PAND"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xdc], ["PADDUSB"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xdd], ["PADDUSW"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xde], ["PMAXUB"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xdf], ["PANDN"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xe0], ["PAVGB"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xe1], ["PSRAW"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xe2], ["PSRAD"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xe3], ["PAVGW"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xe4], ["PMULHUW"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xe5], ["PMULHW"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xe6], ["CVTTPD2DQ"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xe7], ["MOVNTDQ"], [OperandType.MEM128, OperandType.XMM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.MODRR);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xe8], ["PSUBSB"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xe9], ["PSUBSW"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xea], ["PMINSW"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xeb], ["POR"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xec], ["PADDSB"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xed], ["PADDSW"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xee], ["PMAXSW"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xef], ["PXOR"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xf1], ["PSLLW"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xf2], ["PSLLD"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xf3], ["PSLLQ"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xf4], ["PMULUDQ"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xf5], ["PMADDWD"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xf6], ["PSADBW"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xf7], ["MASKMOVDQU"], [OperandType.XMM, OperandType.XMM_RM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.MODRR);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xf8], ["PSUBB"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xf9], ["PSUBW"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xfa], ["PSUBD"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xfb], ["PSUBQ"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xfc], ["PADDB"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xfd], ["PADDW"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xfe], ["PADDD"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf2, 0x0f, 0x10], ["MOVSD"], [OperandType.XMM, OperandType.XMM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf2, 0x0f, 0x11], ["MOVSD"], [OperandType.XMM64, OperandType.XMM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf2, 0x0f, 0x2a], ["CVTSI2SD"], [OperandType.XMM, OperandType.RM32_64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._64BITS | InstFlag.PRE_REX);
		SetInstruction(OpcodeLength.OL_3, [0xf2, 0x0f, 0x2c], ["CVTTSD2SI"], [OperandType.REG32_64, OperandType.XMM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._64BITS | InstFlag.PRE_REX);
		SetInstruction(OpcodeLength.OL_3, [0xf2, 0x0f, 0x2d], ["CVTSD2SI"], [OperandType.REG32_64, OperandType.XMM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._64BITS | InstFlag.PRE_REX);
		SetInstruction(OpcodeLength.OL_3, [0xf2, 0x0f, 0x51], ["SQRTSD"], [OperandType.XMM, OperandType.XMM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf2, 0x0f, 0x58], ["ADDSD"], [OperandType.XMM, OperandType.XMM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf2, 0x0f, 0x59], ["MULSD"], [OperandType.XMM, OperandType.XMM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf2, 0x0f, 0x5a], ["CVTSD2SS"], [OperandType.XMM, OperandType.XMM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf2, 0x0f, 0x5c], ["SUBSD"], [OperandType.XMM, OperandType.XMM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf2, 0x0f, 0x5d], ["MINSD"], [OperandType.XMM, OperandType.XMM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf2, 0x0f, 0x5e], ["DIVSD"], [OperandType.XMM, OperandType.XMM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf2, 0x0f, 0x5f], ["MAXSD"], [OperandType.XMM, OperandType.XMM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf2, 0x0f, 0x70], ["PSHUFLW"], [OperandType.XMM, OperandType.XMM128, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.USE_OP3);
		SetInstruction(OpcodeLength.OL_3, [0xf2, 0x0f, 0xc2], ["CMP", "SD"], [OperandType.XMM, OperandType.XMM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.USE_EXMNEMONIC | InstFlag.PSEUDO_OPCODE);
		SetInstruction(OpcodeLength.OL_3, [0xf2, 0x0f, 0xd6], ["MOVDQ2Q"], [OperandType.MM, OperandType.XMM_RM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.MODRR);
		SetInstruction(OpcodeLength.OL_3, [0xf2, 0x0f, 0xe6], ["CVTPD2DQ"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf3, 0x0f, 0x5a], ["CVTSS2SD"], [OperandType.XMM, OperandType.XMM32], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf3, 0x0f, 0x5b], ["CVTTPS2DQ"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf3, 0x0f, 0x6f], ["MOVDQU"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf3, 0x0f, 0x70], ["PSHUFHW"], [OperandType.XMM, OperandType.XMM128, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.USE_OP3);
		SetInstruction(OpcodeLength.OL_3, [0xf3, 0x0f, 0x7e], ["MOVQ"], [OperandType.XMM, OperandType.XMM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf3, 0x0f, 0x7f], ["MOVDQU"], [OperandType.XMM128, OperandType.XMM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf3, 0x0f, 0xd6], ["MOVQ2DQ"], [OperandType.XMM, OperandType.MM_RM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.MODRR);
		SetInstruction(OpcodeLength.OL_3, [0xf3, 0x0f, 0xe6], ["CVTDQ2PD"], [OperandType.XMM, OperandType.XMM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0xf3, 0x90], ["PAUSE"], [], InstFlag._32BITS);

	def init_SSE3(self):
		SetInstruction = lambda *args: self.SetInstructionCallback(ISetClass.SSE3, *args)
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x7c], ["HADDPD"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0x7d], ["HSUBPD"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x66, 0x0f, 0xd0], ["ADDSUBPD"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_1d, [0xdb, 0x01], ["FISTTP"], [OperandType.FPUM32], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_1d, [0xdd, 0x01], ["FISTTP"], [OperandType.FPUM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_1d, [0xdf, 0x01], ["FISTTP"], [OperandType.FPUM16], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf2, 0x0f, 0x12], ["MOVDDUP"], [OperandType.XMM, OperandType.XMM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf2, 0x0f, 0x7c], ["HADDPS"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf2, 0x0f, 0x7d], ["HSUBPS"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf2, 0x0f, 0xd0], ["ADDSUBPS"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf2, 0x0f, 0xf0], ["LDDQU"], [OperandType.XMM, OperandType.MEM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0xf3, 0x0f, 0x16], ["MOVSHDUP"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);

	def init_SSSE3(self):
		SetInstruction = lambda *args: self.SetInstructionCallback(ISetClass.SSSE3, *args)
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x38, 0x00], ["PSHUFB"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x38, 0x01], ["PHADDW"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x38, 0x02], ["PHADDD"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x38, 0x03], ["PHADDSW"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x38, 0x04], ["PMADDUBSW"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x38, 0x05], ["PHSUBW"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x38, 0x06], ["PHSUBD"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x38, 0x07], ["PHSUBSW"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x38, 0x08], ["PSIGNB"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x38, 0x09], ["PSIGNW"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x38, 0x0a], ["PSIGND"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x38, 0x0b], ["PMULHRSW"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x38, 0x1c], ["PABSB"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x38, 0x1d], ["PABSW"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x38, 0x1e], ["PABSD"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x3a, 0x0f], ["PALIGNR"], [OperandType.MM, OperandType.MM64, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.USE_OP3);
		SetInstruction(OpcodeLength.OL_4, [0x66, 0x0f, 0x38, 0x00], ["PSHUFB"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_4, [0x66, 0x0f, 0x38, 0x01], ["PHADDW"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_4, [0x66, 0x0f, 0x38, 0x02], ["PHADDD"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_4, [0x66, 0x0f, 0x38, 0x03], ["PHADDSW"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_4, [0x66, 0x0f, 0x38, 0x04], ["PMADDUBSW"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_4, [0x66, 0x0f, 0x38, 0x05], ["PHSUBW"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_4, [0x66, 0x0f, 0x38, 0x06], ["PHSUBD"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_4, [0x66, 0x0f, 0x38, 0x07], ["PHSUBSW"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_4, [0x66, 0x0f, 0x38, 0x08], ["PSIGNB"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_4, [0x66, 0x0f, 0x38, 0x09], ["PSIGNW"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_4, [0x66, 0x0f, 0x38, 0x0a], ["PSIGND"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_4, [0x66, 0x0f, 0x38, 0x0b], ["PMULHRSW"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_4, [0x66, 0x0f, 0x38, 0x1c], ["PABSB"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_4, [0x66, 0x0f, 0x38, 0x1d], ["PABSW"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_4, [0x66, 0x0f, 0x38, 0x1e], ["PABSD"], [OperandType.XMM, OperandType.XMM128], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_4, [0x66, 0x0f, 0x3a, 0x0f], ["PALIGNR"], [OperandType.XMM, OperandType.XMM128, OperandType.IMM8], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag.USE_OP3);

	def init_3DNOW(self):
		SetInstruction = lambda *args: self.SetInstructionCallback(ISetClass._3DNOW, *args)
		SetInstruction(OpcodeLength.OL_23, [0x0f, 0x0d, 0x00], ["PREFETCH"], [OperandType.MEM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_23, [0x0f, 0x0d, 0x01], ["PREFETCHW"], [OperandType.MEM], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x0e], ["FEMMS"], [], InstFlag.EXCLUDE_MODRM);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x0f, 0x0d], ["PI2FD"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._3DNOW_FETCH);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x0f, 0x1d], ["PF2ID"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._3DNOW_FETCH);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x0f, 0x90], ["PFCMPGE"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._3DNOW_FETCH);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x0f, 0x94], ["PFMIN"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._3DNOW_FETCH);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x0f, 0x96], ["PFRCP"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._3DNOW_FETCH);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x0f, 0x97], ["PFRSQRT"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._3DNOW_FETCH);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x0f, 0x9a], ["PFSUB"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._3DNOW_FETCH);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x0f, 0x9e], ["PFADD"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._3DNOW_FETCH);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x0f, 0xa0], ["PFCMPGT"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._3DNOW_FETCH);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x0f, 0xa4], ["PFMAX"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._3DNOW_FETCH);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x0f, 0xa6], ["PFRCPIT1"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._3DNOW_FETCH);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x0f, 0xa7], ["PFRSQIT1"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._3DNOW_FETCH);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x0f, 0xaa], ["PFSUBR"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._3DNOW_FETCH);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x0f, 0xae], ["PFACC"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._3DNOW_FETCH);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x0f, 0xb0], ["PFCMPEQ"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._3DNOW_FETCH);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x0f, 0xb4], ["PFMUL"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._3DNOW_FETCH);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x0f, 0xb6], ["PFRCPIT2"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._3DNOW_FETCH);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x0f, 0xb7], ["PMULHRW"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._3DNOW_FETCH);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x0f, 0xbf], ["PAVGUSB"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._3DNOW_FETCH);

	def init_3DNOWEXT(self):
		SetInstruction = lambda *args: self.SetInstructionCallback(ISetClass._3DNOWEXT, *args)
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x0f, 0x0c], ["PI2FW"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._3DNOW_FETCH);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x0f, 0x1c], ["PF2IW"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._3DNOW_FETCH);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x0f, 0x8a], ["PFNACC"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._3DNOW_FETCH);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x0f, 0x8e], ["PFPNACC"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._3DNOW_FETCH);
		SetInstruction(OpcodeLength.OL_3, [0x0f, 0x0f, 0xbb], ["PSWAPD"], [OperandType.MM, OperandType.MM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._3DNOW_FETCH);

	def init_VMX(self):
		SetInstruction = lambda *args: self.SetInstructionCallback(ISetClass.VMX, *args)
		SetInstruction(OpcodeLength.OL_2d, [0x0f, 0x01, 0xc1], ["VMCALL"], [], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2d, [0x0f, 0x01, 0xc2], ["VMLAUNCH"], [], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2d, [0x0f, 0x01, 0xc3], ["VMRESUME"], [], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2d, [0x0f, 0x01, 0xc4], ["VMXOFF"], [], InstFlag._32BITS);

		# In 64bits the operands are promoted to 64bits automatically.
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x78], ["VMREAD"], [OperandType.RM32_64, OperandType.REG32_64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._64BITS);
		SetInstruction(OpcodeLength.OL_2, [0x0f, 0x79], ["VMWRITE"], [OperandType.REG32_64, OperandType.RM32_64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._64BITS);
		SetInstruction(OpcodeLength.OL_23, [0x0f, 0xc7, 0x06], ["VMPTRLD"], [OperandType.MEM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_23, [0x0f, 0xc7, 0x07], ["VMPTRST"], [OperandType.MEM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_33, [0x66, 0x0f, 0xc7, 0x06], ["VMCLEAR"], [OperandType.MEM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_33, [0xf3, 0x0f, 0xc7, 0x06], ["VMXON"], [OperandType.MEM64], InstFlag.INCLUDE_MODRM | InstFlag._32BITS);

	def init_SVM(self):
		SetInstruction = lambda *args: self.SetInstructionCallback(ISetClass.SVM, *args)
		SetInstruction(OpcodeLength.OL_2d, [0x0f, 0x01, 0xd8], ["VMRUN"], [OperandType.ACC_FULL], InstFlag.INCLUDE_MODRM | InstFlag._32BITS | InstFlag._64BITS);
		SetInstruction(OpcodeLength.OL_2d, [0x0f, 0x01, 0xd9], ["VMMCALL"], [], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2d, [0x0f, 0x01, 0xda], ["VMLOAD"], [], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2d, [0x0f, 0x01, 0xdb], ["VMSAVE"], [], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2d, [0x0f, 0x01, 0xdc], ["STGI"], [], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2d, [0x0f, 0x01, 0xdd], ["CLGI"], [], InstFlag._32BITS);
		SetInstruction(OpcodeLength.OL_2d, [0x0f, 0x01, 0xde], ["SKINIT EAX"], [], InstFlag._32BITS);

	def __init__(self, SetInstructionCallback):
		""" Initializes all instructions-sets using the given callback.
		The arguments of the callback are as follows:
		(iset-class, opcode-length, list of bytes of opcode, list of string of mnemonics, list of operands, flags) """
		self.SetInstructionCallback = SetInstructionCallback
		self.init_INTEGER()
		self.init_FPU()
		self.init_P6()
		self.init_MMX()
		self.init_SSE()
		self.init_SSE2()
		self.init_SSE3()
		self.init_SSSE3()
		self.init_3DNOW()
		self.init_3DNOWEXT()
		#self.init_VMX()
		#self.init_SVM()

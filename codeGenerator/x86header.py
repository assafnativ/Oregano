#
# x86header.py
#
# Copyright (C) 2007 Gil Dabah, http://ragestorm.net/disops/
# This library is licensed under the BSD license. See the file COPYING.
#

class OperandType:
	""" Types of possible operands in an opcode.
	Refer to the diStorm's documentation or diStorm's instructions.h
	for more explanation about every one of them. """
	(NONE,
	IMM8,
	IMM16,
	IMM_FULL,
	IMM32,
	IMM_AADM,
	SEIMM8,
	REG8,
	REG16,
	REG_FULL,
	REG32,
	REG64,
	REG32_64,
	REG32_RM,
	FREG32_64_RM,
	RM8,
	RM16,
	RM_FULL,
	RM32,
	RM32_64,
	RM16_32,
	FPUM16,
	FPUM32,
	FPUM64,
	FPUM80,
	R32M16,
	RFULL_M16,
	CREG,
	DREG,
	SREG,
	SEG,
	ACC8,
	ACC_FULL,
	ACC_FULL_NOT64,
	MEM16_FULL,
	PTR16_FULL,
	MEM16_3264,
	RELCB,
	RELC_FULL,
	MEM,
	MEM64,
	MEM128,
	MEM64_128,
	MOFFS,
	CONST1,
	REGCL,
	IB_RB,
	IB_R_DW_QW,
	IB_R_FULL,
	REGI_ESI,
	REGI_EDI,
	REGI_EBXAL,
	REGDX,
	FPU_SI,
	FPU_SSI,
	FPU_SIS,
	MM,
	MM_RM,
	MM32,
	MM64,
	XMM,
	XMM_RM,
	XMM32,
	XMM64,
	XMM128,
	DUMMY) = range(66)

class OpcodeLength:
	""" The length of the opcode in bytes.
	Where a suffix of '3' means we have to read the REG field of the ModR/M byte (REG size is 3 bits).
	Suffix of 'd' means it's a Divided instruction (see documentation),
	tells the disassembler to read the REG field or the whole next byte. """
	(OL_1,
	OL_13,
	OL_1d,
	OL_2,
	OL_23,
	OL_2d,
	OL_3,
	OL_33,
	OL_4) = range(9)

	""" Next-Opcode-Length dictionary is used in order to recursively build the instructions' tables dynamically.
	It is used in such a way that it indicates how many more nested tables
	we have to build and link starting from a given OL. """
	NextOL = {OL_13: OL_1, OL_1d: OL_1, OL_2: OL_1, OL_23: OL_13,
		  OL_2d: OL_1d, OL_3: OL_2, OL_33: OL_23, OL_4: OL_3}

class InstFlag:
	""" Instruction Flag contains all bit mask constants for describing an instruction.
	You can bitwise-or the flags. See diStorm's documentation for more explanation.
	
	The GEN_BLOCK is a special flag, it is used in the tables generator only;
	See GenBlock class inside x86db.py. """
	BITS_USED = 27
	EXCLUDE_MODRM = 0
	(INCLUDE_MODRM,
	NOT_DIVIDED,
	_16BITS,
	_32BITS,
	PRE_LOCK,
	PRE_REPNZ,
	PRE_REP,
	PRE_CS,
	PRE_SS,
	PRE_DS,
	PRE_ES,
	PRE_FS,
	PRE_GS,
	PRE_OP_SIZE,
	PRE_ADDR_SIZE,
	NATIVE,
	USE_EXMNEMONIC,
	USE_OP3,
	MODRM_BASED,
	MODRR,
	_3DNOW_FETCH,
	PSEUDO_OPCODE,
	INVALID_64BITS,
	_64BITS,
	PRE_REX,
	USE_EXMNEMONIC2,
	_64BITS_FETCH,
	GEN_BLOCK) = [1 << i for i in xrange(BITS_USED+1)]

class ISetClass:
	""" Instruction-Set-Class indicates to which set the instruction belongs.
	These types are taken from the documentation of Intel/AMD. """
	(INTEGER,
	FPU,
	P6,
	MMX,
	SSE,
	SSE2,
	SSE3,
	SSSE3,
	_3DNOW,
	_3DNOWEXT,
	VMX,
	SVM) = range(12)

class NodeType:
	""" A node can really an object holder for an instruction-info object or
	another table (list) with a different size.

	GROUP - 8 entries in the table
	FULL - 256 entries in the table.
	Divided - 72 entries in the table (ranges: 0x0-0x7, 0xc0-0xff). """
	(NOTEXISTS,
	NONE,
	INFO,
	LIST_GROUP,
	LIST_FULL,
	LIST_DIVIDED) = range(-1, 5)

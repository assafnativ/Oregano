
#pragma once

#include <windows.h>

#include "GlobalDefines.hpp"

/* Log depended */
static const BYTE EIP_CHANGE_TYPE(0);
static const BYTE RIP_CHANGE_TYPE(0);
static const DWORD THREAD_CHANGE(0xfe);
static const Cycle INVALID_CYCLE(0xffffffff);
static const Cycle MAX_CYCLE    (0xfffffffe);
static const BYTE UNKNOWN_SYMBOL('?');
static const BYTE UNKNOWN_BYTE(0x3f);
static const WORD UNKNOWN_WORD(0x3f3f);
static const DWORD UNKNOWN_DWORD(0x3f3f3f3f);

#ifdef X86
static const MACHINE_LONG UNKNOWN_MACHINE_LONG(0x3f3f3f3f);
static const DWORD REG_ID_EIP(0x00);
static const DWORD REG_ID_EDI(0x01);
static const DWORD REG_ID_ESI(0x02);
static const DWORD REG_ID_EBP(0x03);
static const DWORD REG_ID_EBX(0x04);
static const DWORD REG_ID_EDX(0x05);
static const DWORD REG_ID_ECX(0x06);
static const DWORD REG_ID_EAX(0x07);
static const DWORD REG_ID_ECS(0x08);
static const DWORD REG_ID_EFLAGS(0x09);
static const DWORD REG_ID_ESP(0x0a);
static const DWORD REG_ID_ESS(0x0b);
static const DWORD THREAD_ID(0x0c);
static const DWORD LAST_REG_ID_x86(THREAD_ID);
static const DWORD NUMBER_OF_REGS(LAST_REG_ID_x86+1);

#elif AMD64
static const MACHINE_LONG UNKNOWN_MACHINE_LONG(0x3f3f3f3f3f3f3f3f);
static const DWORD REG_ID_RIP(0x00);
static const DWORD REG_ID_RDI(0x01);
static const DWORD REG_ID_RSI(0x02);
static const DWORD REG_ID_RBP(0x03);
static const DWORD REG_ID_RBX(0x04);
static const DWORD REG_ID_RDX(0x05);
static const DWORD REG_ID_RCX(0x06);
static const DWORD REG_ID_RAX(0x07);
static const DWORD REG_ID_R8 (0x08);
static const DWORD REG_ID_R9 (0x09);
static const DWORD REG_ID_R10(0x0A);
static const DWORD REG_ID_R11(0x0B);
static const DWORD REG_ID_R12(0x0C);
static const DWORD REG_ID_R13(0x0D);
static const DWORD REG_ID_R14(0x0E);
static const DWORD REG_ID_R15(0x0F);
static const DWORD REG_ID_RCS(0x10);
static const DWORD REG_ID_RFLAGS(0x11);
static const DWORD REG_ID_RSP(0x12);
static const DWORD REG_ID_RSS(0x13);
static const DWORD THREAD_ID(0x14);
static const DWORD LAST_REG_ID_AMD64(THREAD_ID);
static const DWORD NUMBER_OF_REGS(LAST_REG_ID_AMD64+1);
#endif

static const DWORD BYTEPTR_ACCESS (0x1c);
static const DWORD WORDPTR_ACCESS (0x1d);
static const DWORD DWORDPTR_ACCESS(0x1e);
static const DWORD QWORDPTR_ACCESS(0x1f);

static const DWORD PROCESSOR_TYPE_x86  (0x00);
static const DWORD PROCESSOR_TYPE_AMD64(0x01);

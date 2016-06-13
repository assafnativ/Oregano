
; Defines
THREAD_ID_MASK              equ 0fffh
THREAD_CONTEXT_SIZE         equ 040h
THREAD_CONTEXT_SIZE_IN_BITS equ 06h
THREAD_CONTEXT_ARRAY_END    equ 03ffffh
SKIP_MEM_READ               equ 030h

; Exports
GLOBAL _orgStackFaultInterrupt
GLOBAL _orgGPFInterrupt
GLOBAL _orgPageFaultInterrupt

; Globals
EXTERN _target_process
EXTERN _lastContext
EXTERN _threads

SECTION .data

_orgStackFaultInterrupt DD 0
_orgGPFInterrupt        DD 0
_orgPageFaultInterrupt  DD 0

SECTION .text

; Exportes
GLOBAL _stackFaultInterrupt@0
GLOBAL _GPFInterrupt@0
GLOBAL _pageFaultInterrupt@0

%macro CHECK_PROCESS_AND_THREAD 1
    pushf
    push eax
    push ebx

    mov eax, cr3
    mov ebx, [_target_process]
    cmp eax, ebx
    je %%DONE_CHECKING

    mov eax, DWORD [_lastContext]
    cmp ebx, DWORD [ebx]
    je %%CONTEXT_FOUND

        ; Load context
        ; Should never fail to find thread context, we set the first thread context
        ; when we set the trap flag on.
        push ecx
        push edx
        mov edx, ebx
        ; Address is usually DWORD aligne, so for better hashing we shift 2 bits out
        shr edx, 2
        and edx, THREAD_ID_MASK
        ; Find item in hash table
        ; Every entry is 0x40 bytes long
        shl edx, THREAD_CONTEXT_SIZE_IN_BITS
        %%IS_THIS_THE_RIGHT_CONTEXT:
            lea eax, [edx + _threads]
            mov ecx, [eax]
            cmp ecx, ebx
            je %%CONTEXT_FOUND
            add edx, THREAD_CONTEXT_SIZE
            and edx, THREAD_CONTEXT_ARRAY_END
        jmp %%IS_THIS_THE_RIGHT_CONTEXT
        %%CONTEXT_FOUND:
        xor ebx, ebx
        inc ebx
        mov [eax + SKIP_MEM_READ], ebx

        pop edx
        pop ecx

%%DONE_CHECKING:
    pop eax
    pop ebx
    popf

    jmp DWORD [%1]
%endmacro

_stackFaultInterrupt@0:
CHECK_PROCESS_AND_THREAD _orgStackFaultInterrupt

_GPFInterrupt@0:
CHECK_PROCESS_AND_THREAD _orgGPFInterrupt

_pageFaultInterrupt@0:
CHECK_PROCESS_AND_THREAD _orgPageFaultInterrupt


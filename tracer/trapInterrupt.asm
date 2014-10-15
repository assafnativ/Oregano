
; Only in MASM
;	TITLE	trap_interrupt.asm
;	.586
;
;	.MODEL flat

; Exportes
GLOBAL	_orgTrapInterrupt
GLOBAL	_orgBreakpointInterrupt
GLOBAL	_targetProcessId
GLOBAL	_target_process
GLOBAL	_stopAddress
GLOBAL  _bottom_log_address
GLOBAL  _top_log_address
GLOBAL	_log_buffer
GLOBAL	_log_buffer_item
GLOBAL	_active_log_buffer
GLOBAL  _used_buffers
GLOBAL	_next_free_log_buffer
GLOBAL	_lastContext
GLOBAL  _lastLoggedContext
GLOBAL	_threads
GLOBAL  _loggingRanges
GLOBAL  _isTrapOnBranchSet

%ifdef DEBUG
GLOBAL	_DebugVar0
GLOBAL	_DebugVar1  ; DR6
GLOBAL	_DebugVar2
GLOBAL	_DebugVar3  ; Reason for calling original interrupt
GLOBAL	_DebugVar4
GLOBAL	_DebugVar5
GLOBAL	_DebugVar6
GLOBAL	_DebugVar7
%endif

; Defines
LOG_BUFFER_SIZE				equ 00004000h
SHIFTED_LOG_BUFFER_MAX_SIZE  equ 00000007h
BUFFER_MAX_SIZE_BIT_TO_SHIFT equ 0000000bh
MAX_BUFFER_OFFSET            equ 00003f40h
SIZE_OF_DWORD               equ 04h
SIZE_OF_QWORD               equ 08h
SIZE_OF_POINTER             equ 04h
NUMBER_OF_BUFFERS           equ 1000h
NUMBER_OF_BUFFERS_MASK      equ 0fffh	; I've got exactly 0x1000 buffers

END_BUFFER_SYMBOL			equ 0ffffffffh
THREAD_CHANGE_SYMBOL		equ 0feh
THREAD_ID_MASK              equ 03ffc0h
THREAD_CONTEXT_SIZE         equ 040h
THREAD_CONTEXT_ARRAY_END    equ 03ffffh
KERNEL_SPACE_MASK           equ 80000000h ; 2GB
TRAP_FLAG_MASK              equ 00000100h
BREAK_SINGLE_STEP_FLAG_MASK equ 00004000h ; AKA BS flag AKA BullShit flag of DR6
ALL_DR6_FLAGS               equ 0000f00fh ; See page 485 (15-3) @ 24319202.pdf "Intel Architecture Software Developer's Manuaal Volume 3 System Programming"
BREAK_OTHER_FLAGS           equ 0000a00fh
; From Intel Model-Specific Registers PDF
DEBUGCTLMSR_ID              equ 01D9h
BRANCH_TRAP_FLAG            equ 02h
BRANCH_TRAP_FLAG_CLEAR      equ 0
; Get it from PsGetCurrentProcess @ ntoskrnl.exe
CURRENT_KTHREAD_OFFSET	    equ 0124h
; Get it from _KiTrap01
FS_VALUE                    equ 30h

; Regs ids:		(Note that this is not the same list as the one found in the disassembler)
REG_ID_EIP					equ 00h
REG_ID_EDI					equ 01h
REG_ID_ESI					equ 02h
REG_ID_EBP					equ 03h
REG_ID_EBX					equ 04h
REG_ID_EDX					equ 05h
REG_ID_ECX					equ 06h
REG_ID_EAX					equ 07h
; REG_ID_EIP				equ 08h
REG_ID_ECS					equ 08h
REG_ID_EFLAGS				equ 09h
REG_ID_ESP					equ 0Ah
REG_ID_ESS					equ 0Bh

; Global variables defines
SECTION .data

; Original trap interrupt, if needed.
_orgTrapInterrupt			DD 0
; To simulate a breakpoint
_orgBreakpointInterrupt 	DD 0
; What process are I debugging?
_targetProcessId			DD 0
_target_process				DD 0
; Where should I stop logging
_stopAddress				DD 0
_bottom_log_address         DD 0
_top_log_address            DD 0
; Output buffer
_log_buffer					DD 0
; I got 0x1000 log buffers
_log_buffer_item      times NUMBER_OF_BUFFERS DD 0
_active_log_buffer    DD 0
_used_buffers         DD 0
_next_free_log_buffer DD 0
_lastContext		  DD 0 
_lastLoggedContext    DD 0
_isTrapOnBranchSet    DD 0
; ThreadContext_t is 0x10 dwords (0x40 bytes) and I got a table of 0x1000 entries
align   16
_threads                    times 65536 DD 0 
; LoggingRanges maximum of 0x80 logging ranges
_loggingRanges              times 256 DD 0

; Regs last value offsets in struct:
LAST_THREAD                 equ 00h
LAST_EDI                    equ 04h
LAST_ESI                    equ 08h
LAST_EBP                    equ 0ch
LAST_EBX                    equ 10h
LAST_BH                     equ 11h
LAST_EDX                    equ 14h
LAST_DH                     equ 15h
LAST_ECX                    equ 18h
LAST_CH                     equ 19h
LAST_EAX                    equ 1ch
LAST_AH                     equ 1dh
LAST_EIP                    equ 20h
LAST_ECS                    equ 24h
LAST_EFLAGS                 equ 28h
LAST_ESP                    equ 2ch
SKIP_MEM_LOG                equ 30h
BOTTOM_BOUND                equ 34h
TOP_BOUND                   equ 38h

%ifdef DEBUG
_DebugVar0	DD 0
_DebugVar1	DD 0
_DebugVar2	DD 0
_DebugVar3	DD 0
_DebugVar4	DD 0
_DebugVar5	DD 0
_DebugVar6	DD 0
_DebugVar7	DD 0
%endif

; Macros:
%macro CALL_ORIGINAL_INTERRUPT 0
	popad
    pop fs
	; Call original interrupt handler
	jmp	DWORD [_orgTrapInterrupt]
%endmacro

%macro RETURN_FROM_INTERRUPT_WITH_CHECK 0
    ; Do I need to call original interrupt
    mov eax, dr6
    test eax, BREAK_OTHER_FLAGS
    jz %%JUST_IRET
    %ifdef DEBUG
    mov eax, 3
    mov [_DebugVar3], eax
    %endif
    CALL_ORIGINAL_INTERRUPT
    %%JUST_IRET:
    popad
    pop fs
    iretd
%endmacro

%macro LOG_REGISTER_CHANGE_WITH_STOS 1
	; Get last %1
	mov eax, DWORD [esp + SAVED_%1]
	cmp eax, [ebp + LAST_%1]
	jz %%DONE_WITH_REG
		mov DWORD [ebp + LAST_%1], eax
		xchg eax, edx
		stosb
		xchg eax, edx
		stosd
    %%DONE_WITH_REG:
	inc edx
%endmacro

SECTION .text
align   16

; Function define
GLOBAL	_trap_interrupt@0
; Inside labels for debugging
GLOBAL  _trap_interrupt_target_process@0
GLOBAL  _trap_interrupt_got_log_buffer@0
GLOBAL  _trap_interrupt_got_thread@0
GLOBAL  _trap_interrupt_eip_logged@0
GLOBAL  _trap_interrupt_in_range@0
GLOBAL  _trap_interrupt_check_log_buffer@0
GLOBAL  _trap_interrupt_log_buffer_checked@0
GLOBAL  _trap_interrupt_perform_mem_log@0
GLOBAL  _trap_interrupt_log_registers@0
GLOBAL  _trap_interrupt_save_log_buffer_pos@0
GLOBAL  _trap_interrupt_done@0
GLOBAL  _trap_interrupt_out_of_range@0

;
; trap_interrupt
; 	
; 	Description:
;	 	This function should replace the original trap interrupt.
; 		The purpose of this function is to log the current opcode,
; 		and it's affect on memory, registers and anything else that
; 		might be in the interest of the programmer.
; 		This function shold be as fast, efficient and effective as
; 		possible, cause it is called once for every opcode running.
; 		It is written in mostly pure x86 assembly.
;       
;   Execution plan:
;       0. Check if the interrupt was called from our process and for Single Stepping
;       1. Get a pointer to a output buffer
;       2. Check context switch
;       3. Read n' write last EIP
;       4. Check that there is free space in logging buffer
;       5. Switch log buffer if needed
;       6. Check if I are in an address that I should log
;       7. Write memory changed from last opcode
;       8. Write and update register values
;       9. Write back the last writting point in buffer
;       A. Ret
;
; 	Known issues:
; 		Because this function replaces the original windows trap interrupt,
; 		it is impossable to use debuggers single step function while it is running,
; 		an attempt to do so might cause a blue screen.
;
;
    ; NASM assumes nothing
    ; assume DS:NOTHING, SS:NOTHING, ES:NOTHING
    align 8
_trap_interrupt@0:

; Save all registers
    push fs
	pushad
    ; Set the selector
    mov eax, FS_VALUE
    mov fs, ax

	; Now the stack looks somthing like this:
SAVED_EDI		equ 000h
SAVED_ESI		equ 004h
SAVED_EBP		equ 008h
SAVED_KERNEL_ESP	equ 00ch
SAVED_EBX		equ 010h
SAVED_EDX		equ 014h
SAVED_ECX		equ 018h
SAVED_EAX		equ 01ch
SAVED_FS        equ 020h
; Interrupt call
SAVED_EIP		equ 024h
SAVED_ECS		equ 028h
SAVED_EFLAGS	equ 02ch
SAVED_ESP		equ 030h
SAVED_ESS		equ 034h
; TODO: Do I need to set the FS to 0x30 and DS, ES to 0x23 as in _KiTrap01

; Interrupt 0x01 can be called for five reasons:
;   1. Single Step
;   2. Hardware breakpoint on execution
;   3. Hardware breakpoint on memory
;   4. Task switch
;   5. General Detect Fault - A use of the debug registers when they are not available 
; Check the reason for the Interrupt.
    ; push ebx, pop ebx is faster than mov someGlobal, ebx
    mov eax, dr6
    %ifdef DEBUG
    mov [_DebugVar1], eax
    %endif
    test eax, BREAK_SINGLE_STEP_FLAG_MASK
    jnz INTERRUPT_COZED_BY_SINGLE_STEP
    ; Sometimes the dr6 is just cleared and it is still a single step
    ; I don't quite understand this
    test eax, ALL_DR6_FLAGS
    jz INTERRUPT_COZED_BY_SINGLE_STEP
    ; The interupt was not caused for Single Step issues
    %ifdef DEBUG
    mov eax, 1
    mov [_DebugVar3], eax
    %endif
    CALL_ORIGINAL_INTERRUPT
INTERRUPT_COZED_BY_SINGLE_STEP:

; Check if this is the traced process
; I use the CR3 (The memory page table pointer) as the process UID
    mov ebx, cr3
    %ifdef DEBUG
    mov [_DebugVar2], ebx
    %endif
	mov ecx, [_target_process]
	cmp ebx, ecx
	je THIS_IS_THE_TARGET_PROCESS
    %ifdef DEBUG
    mov eax, 2
    mov [_DebugVar3], eax
    %endif
	CALL_ORIGINAL_INTERRUPT
THIS_IS_THE_TARGET_PROCESS:
_trap_interrupt_target_process@0:

    ; Clear the single step flag from DR6 (http://en.wikipedia.org/wiki/X86_debug_register)
    and eax, ~BREAK_SINGLE_STEP_FLAG_MASK
    mov dr6, eax
%ifdef DEBUG
    mov eax, 1
    %ifdef DEBUG
    mov [_DebugVar0], eax
    %endif
%endif

    ; Is in range

    ; Get output buffer pointer
	; I try to keep the buffer_ptr in eax most of the time coz it's used the most.
	; The next place to write is _log_bufer + _log_buffer_pos (Saved at offset zero of the log_buffer).
	mov ecx, DWORD [_log_buffer]
	mov ebx, DWORD [ecx]
	lea eax, [ebx + ecx]
_trap_interrupt_got_log_buffer@0:
    %ifdef DEBUG
    mov [_DebugVar0], eax
    %endif

	; Check for thread change
    ; EBX would keep the KTHREAD
	mov ebx, [fs:CURRENT_KTHREAD_OFFSET]
    mov ebp, DWORD [_lastContext]
    %ifdef DEBUG
    mov [_DebugVar5], ebp
    %endif
	cmp ebx, DWORD [ebp]
	je NO_THREAD_CHANGE
        ; Load context
        ; Should never fail to find thread context.
        mov edx, ebx
        ; Address is usually DWORD aligned, so for better hashing I shift 2 bits out
        and edx, THREAD_ID_MASK
        ; Find item in hash table
        ; Every entry is 0x40 bytes long
        ; But I use only bits 6 to 12, so I'm already aligend with the index
        IS_THIS_THE_RIGHT_CONTEXT:
            lea ebp, [edx + _threads]
            mov ecx, [ebp] ; .ID
            cmp ecx, ebx
            je CONTEXT_FOUND
            add edx, THREAD_CONTEXT_SIZE
            and edx, THREAD_CONTEXT_ARRAY_END
        jmp IS_THIS_THE_RIGHT_CONTEXT
    CONTEXT_FOUND:
        mov [_lastContext], ebp
    NO_THREAD_CHANGE:
_trap_interrupt_got_thread@0:

	; Log EIP, also indicates a new cycle
    mov ebx, [ebp + LAST_EIP]
    mov edx, [esp + SAVED_EIP]
    mov [ebp + LAST_EIP], edx
    mov edx, ebx
_trap_interrupt_eip_logged@0:
    ; If out of user land, get lost
    and edx, KERNEL_SPACE_MASK
    test edx, edx
    jz NOT_KERNEL_SPACE
        ; Kernel space, get lost
        RETURN_FROM_INTERRUPT_WITH_CHECK
    NOT_KERNEL_SPACE:

    ; Check logging range
    cmp DWORD [ebp + TOP_BOUND], ebx
    jbe OUT_OF_LOGGING_BOUNDS
    TOP_BOUND_OK:
    cmp DWORD [ebp + BOTTOM_BOUND], ebx
    jbe IN_RANGE
    OUT_OF_LOGGING_BOUNDS:
        ; Ok I am now out of the logging range
        ; Go to check other logging ranges
        jmp OUT_OF_LOGGING_RANGE

_trap_interrupt_in_range@0:
    IN_RANGE:
    ; Check if need to write thread change, or not
    mov ecx, [_lastLoggedContext]
    cmp ebp, ecx
    je DONE_LOGGING_THREAD_ID
        ; Need to write thread chnage to log
        mov BYTE [eax], THREAD_CHANGE_SYMBOL
        inc eax
        mov ecx, DWORD [ebp] ; threadContext.ID
        mov DWORD [eax], ecx
        add eax, 4
        mov [_lastLoggedContext], ebp
    DONE_LOGGING_THREAD_ID:

	; Write the EIP reg code
	mov BYTE [eax], 0
    ; I log the last executed opcode, so I need the last EIP
	inc eax
	; Write EIP
	mov DWORD [eax], ebx
	; pos += sizeof( EIP )
    add eax, 4

_trap_interrupt_check_log_buffer@0:
	; Check for output buffer end
    mov ecx, DWORD [_log_buffer]
	mov edx, DWORD [ecx]
	; Lets say 0x7ff bytes are a must for one iteration
	shr edx, BUFFER_MAX_SIZE_BIT_TO_SHIFT
	; If I miss it once I am totaly fucked!
	xor edx, SHIFTED_LOG_BUFFER_MAX_SIZE
	jnz	LOG_BUFFER_HAS_SPACE
		; Move to the next buffer
        ; First save the last writting point.
        ; It's the beginning of the cycle, but I've already written the EIP
        ; and thread ID
        mov edx, DWORD [_log_buffer]
        sub eax, edx
        mov DWORD [edx], eax
        ; Inc the number of buffers used
        loc inc DWORD [_used_buffers]
		; Get the next buffer from the buffers array
		mov edx, DWORD [_active_log_buffer]
		inc edx
		and edx, NUMBER_OF_BUFFERS_MASK
		; TODO: comper with next_free_log_buffer
		mov DWORD [_active_log_buffer], edx
		mov eax, DWORD [_log_buffer_item + edx * SIZE_OF_POINTER]
		mov DWORD [_log_buffer], eax
		; 4 first bytes are used to save the last pos of the buffer
		mov DWORD [eax], SIZE_OF_DWORD
        add eax, SIZE_OF_DWORD

_trap_interrupt_log_buffer_checked@0:
LOG_BUFFER_HAS_SPACE:
    ; Check the skip mem log flag
    mov ecx, DWORD [ebp + SKIP_MEM_LOG]
    test ecx, ecx
    jz PERFORM_MEM_LOG
        ; Skip the current mem log
        xor edx, edx
        mov DWORD [ebp + SKIP_MEM_LOG], edx
        jmp SKIPING_LOGGING_OF_OPCODE_EFFECT
_trap_interrupt_perform_mem_log@0:
PERFORM_MEM_LOG:
	; Parse Opcode
	movzx ecx, BYTE [ebx]
	inc ebx
	jmp [TABLE_ID_0001 + ecx * SIZE_OF_POINTER]

FINISH_LOG_CYCLE:

_trap_interrupt_log_registers@0:
WRITE_ALL_CHANGED_REGISTERS:
	; I'll use edx to hold the regs log ids
	; and ebp to iterate over them
    ; Ids start from 0 which is EIP
	xor edx, edx	
SKIPING_LOGGING_OF_OPCODE_EFFECT:
    ; But I already logged EIP
	inc edx			

	; Get last edi
	mov ecx, DWORD [ebp + LAST_EDI]
	cmp ecx, edi
	jz DONE_WITH_EDI
		mov DWORD [ebp + LAST_EDI], edi
		mov BYTE [eax], dl
		inc eax
		mov DWORD [eax], edi
        add eax, SIZE_OF_DWORD
DONE_WITH_EDI:
	; Inc reg id
	inc edx	; Next is ESI (0x02)
	
	; From now on I shall write them using edi which just got free for use
	mov edi, eax

	; Get last esi
	mov eax, DWORD [ebp + LAST_ESI]
	cmp eax, esi
	jz DONE_WITH_ESI
		mov DWORD [ebp + LAST_ESI], esi
		mov eax, edx
		stosb
		mov eax, esi 
		stosd
DONE_WITH_ESI:
	inc edx ; Next is EBP (0x03)
	
    LOG_REGISTER_CHANGE_WITH_STOS EBP
	; Here comes the kernel esp on the stack, but I don't care about it.
    LOG_REGISTER_CHANGE_WITH_STOS EBX
    LOG_REGISTER_CHANGE_WITH_STOS EDX
    LOG_REGISTER_CHANGE_WITH_STOS ECX
    LOG_REGISTER_CHANGE_WITH_STOS EAX
    inc edx
    ;LOG_REGISTER_CHANGE_WITH_STOS EFLAGS
    inc edx ; Skip EFlags
    LOG_REGISTER_CHANGE_WITH_STOS ESP

_trap_interrupt_save_log_buffer_pos@0:
	; Save log buffer pos (Relatived to the buffer)
	mov eax, DWORD[_log_buffer]
	sub edi, eax
	mov DWORD [eax], edi
	; Continue to return

_trap_interrupt_done@0:
ALL_DONE:
    RETURN_FROM_INTERRUPT_WITH_CHECK

WRITE_LOG_POS_AND_RET:
	; Save log buffer pos (Relatived to the buffer)
	mov edi, DWORD[_log_buffer]
	sub eax, edi
	mov DWORD [edi], eax
    RETURN_FROM_INTERRUPT_WITH_CHECK

CLEAR_TRAP_FLAG_AND_RET:
	; Save log buffer pos (Relatived to the buffer)
	mov edi, DWORD[_log_buffer]
	sub eax, edi
	mov DWORD [edi], eax
	; Clear the trap flag
	mov eax, DWORD [esp + SAVED_EFLAGS]
	and eax, ~TRAP_FLAG_MASK
	mov DWORD [esp + SAVED_EFLAGS], eax
    RETURN_FROM_INTERRUPT_WITH_CHECK

OUT_OF_LOGGING_RANGE:
_trap_interrupt_out_of_range@0:
    ; I got EIP in ebx at this point
    mov ecx, _loggingRanges
    cmp [ecx], ebx
    jbe BOTTOM_RANGE_FOUND
    ; I assume that the ranges are sorted by BOTTOM
    ; Find the first range that starts before EIP
    NEXT_RANGE:
        add ecx, 8  ; sizeof(LoggingRange_t)
        cmp [ecx], ebx
        ja NEXT_RANGE
    BOTTOM_RANGE_FOUND:
    ; Check the TOP bound
    cmp [ecx + 4], ebx
    jbe NOT_IN_ANY_RANGE
    ; Range found
    mov edx, [ecx]
    mov ecx, [ecx + 4]
    mov [ebp + BOTTOM_BOUND], edx
    mov [ebp + TOP_BOUND], ecx
    ; Go back to the beginning of the interrupt
    ; just skip the PUSHAD, coze we already done that
    mov DWORD [ebp + SKIP_MEM_LOG], 1
    ; Clear the trap on branch flag
    mov edx, DWORD [_isTrapOnBranchSet]
    test edx, edx
    jz TRAP_ON_BRANCH_CLEAR
        push eax
        xor edx, edx
        xor eax, eax
        mov ecx, DEBUGCTLMSR_ID
        wrmsr
        pop eax
    TRAP_ON_BRANCH_CLEAR:
    ; Continue as if nothing happend
    jmp IN_RANGE

    NOT_IN_ANY_RANGE:
    mov eax, DWORD [_isTrapOnBranchSet]
    test eax, eax
    jnz TRAP_ON_BRANCH_SET
        ; Switch to trap on branch, because returning into the logging range, 
        ; is more likley to happen on branch, and this way I hope to get better
        ; pref'
        mov ecx, DEBUGCTLMSR_ID
        mov eax, BRANCH_TRAP_FLAG
        ; xor edx, edx - Edx is supposed to be set to zero, but I think it would
        ; be ok to leave it as is, because DEBUGCTLMSR has only 32 relevent bits.
        ; If not, I also need to change the code for clearing the flag.
        wrmsr
    TRAP_ON_BRANCH_SET:
    ; When I return to logging, I would have to skip one log cycle
    ; so all registers would get the right values
    ; I have to do it both here and in the range found, because it might
    ; get back right into the current logging range
    mov DWORD [ebp + SKIP_MEM_LOG], 1
    ; Return for now
    ; Note that I didn't write the last writting offset to the log,
    ; because I want the trace to overwrite this cycle
    RETURN_FROM_INTERRUPT_WITH_CHECK

%include "opcodeSideEffects.auto.asm"
;_trap_interrupt@0 ENDP

;END

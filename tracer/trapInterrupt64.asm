
; Only in MASM
;	TITLE	trap_interrupt.asm
;	.AMD64
;
;	.MODEL flat
BITS 64
DEFAULT REL

; Exportes
GLOBAL	orgTrapInterrupt
GLOBAL	orgBreakpointInterrupt
GLOBAL	targetProcessId
GLOBAL	target_process
GLOBAL	stopAddress
GLOBAL  bottom_log_address
GLOBAL  top_log_address
GLOBAL	log_buffer
GLOBAL	log_buffer_item
GLOBAL	active_log_buffer
GLOBAL  used_buffers
GLOBAL	next_free_log_buffer
GLOBAL	lastContext
GLOBAL  lastLoggedContext
GLOBAL	threads
GLOBAL  loggingRanges
GLOBAL  is_trap_on_branch_set

%ifdef DEBUG
GLOBAL	DebugVar0
GLOBAL	DebugVar1
GLOBAL	DebugVar2
GLOBAL	DebugVar3
GLOBAL	DebugVar4
GLOBAL	DebugVar5
GLOBAL	DebugVar6
GLOBAL	DebugVar7
%endif

; Defines
LOG_BUFFER_SIZE				equ 00004000h
SHIFTED_LOG_BUFFER_MAX_SIZE	equ 00000007h	; (0x3fff >> 0xb)
BUFFER_MAX_SIZE_BIT_TO_SHIFT equ 0000000bh
MAX_BUFFER_OFFSET            equ 00003f40h
SIZE_OF_DWORD               equ 04h
SIZE_OF_QWORD               equ 08h
SIZE_OF_POINTER             equ 08h
NUMBER_OF_BUFFERS           equ 1000h
NUMBER_OF_BUFFERS_MASK      equ 0fffh	; I've got exactly 0x1000 buffers

END_BUFFER_SYMBOL			equ 0ffffffffh
THREAD_CHANGE_SYMBOL		equ 0feh
THREAD_ID_MASK              equ 03ffc0h
THREAD_CONTEXT_SIZE         equ 0100h
THREAD_CONTEXT_ARRAY_END    equ 0fffffh
KERNEL_SPACE_MASK           equ 0fffff80000000000h ; 8TB (Microsoft Windows Internals, Fourth Edition C7. Memory Management - Virtual Address Space Layouts
TRAP_FLAG_MASK              equ 00000100h
BREAK_SINGLE_STEP_FLAG_MASK equ 00004000h ; AKA BS flag AKA BullShit flag of DR6
BREAK_OTHER_FLAGS           equ 0000a007h
; From Intel Model-Specific Registers PDF
DEBUGCTLMSR_ID              equ 01D9h
BRANCH_TRAP_FLAG            equ 02h
BRANCH_TRAP_FLAG_CLEAR      equ 0
; Get it from PsGetCurrentProcess @ ntoskrnl.exe
CURRENT_KTHREAD_OFFSET	    equ 0188h

; Regs ids:		(Note that this is not the same list as the one found in the disassembler)
REG_ID_RIP					equ 00h
REG_ID_RDI					equ 01h
REG_ID_RSI					equ 02h
REG_ID_RBP					equ 03h
REG_ID_RBX					equ 04h
REG_ID_RDX					equ 05h
REG_ID_RCX					equ 06h
REG_ID_RAX					equ 07h
REG_ID_R8                   equ 08h
REG_ID_R9                   equ 09h
REG_ID_R10                  equ 0Ah
REG_ID_R11                  equ 0Bh
REG_ID_R12                  equ 0Ch
REG_ID_R13                  equ 0Dh
REG_ID_R14                  equ 0Eh
REG_ID_R15                  equ 0Fh
; REG_ID_EIP				equ 08h
REG_ID_ECS					equ 10h
REG_ID_EFLAGS				equ 11h
REG_ID_ESP					equ 12h
REG_ID_ESS					equ 13h

; Global variables defines
SECTION .data

; Original trap interrupt, if needed.
orgTrapInterrupt			DQ 0
; To simulate a breakpoint
orgBreakpointInterrupt 	DQ 0
; What process I'm debugging?
targetProcessId			DQ 0
target_process				DQ 0
; Where should I stop logging
stopAddress				DQ 0
bottom_log_address          DQ 0
top_log_address             DQ 0
; Output buffer
log_buffer					DQ 0
; I got 0x100 log buffers
log_buffer_item			times NUMBER_OF_BUFFERS DQ 0
active_log_buffer			DQ 0
used_buffers               DQ 0
next_free_log_buffer		DQ 0
lastContext				DQ 0
lastLoggedContext          DQ 0
is_trap_on_branch_set       DQ 0
; ThreadContext_t is 0x20 qwords (0x100 bytes) and I got a table of 0x1000 entries
align   16
threads                    times 131072 DQ 0
; LoggingRanges maximum of 0x80 logging ranges
loggingRanges              times 256 DQ 0

; Regs last value offsets in struct:
LAST_THREAD                 equ 00h
LAST_RDI                    equ 08h
LAST_EDI                    equ 08h
LAST_RSI                    equ 10h
LAST_ESI                    equ 10h
LAST_EBP                    equ 18h
LAST_RBP                    equ 18h
LAST_RBX                    equ 20h
LAST_EBX                    equ 20h
LAST_BH                     equ 21h
LAST_RDX                    equ 28h
LAST_EDX                    equ 28h
LAST_DH                     equ 29h
LAST_RCX                    equ 30h
LAST_ECX                    equ 30h
LAST_CH                     equ 31h
LAST_RAX                    equ 38h
LAST_EAX                    equ 38h
LAST_AH                     equ 39h
LAST_R8                     equ 40h
LAST_R8D                    equ 40h
LAST_R8W                    equ 40h
LAST_R8B                    equ 40h
LAST_R9                     equ 48h
LAST_R9D                    equ 48h
LAST_R9W                    equ 48h
LAST_R9B                    equ 48h
LAST_R10                    equ 50h
LAST_R10D                   equ 50h
LAST_R10W                   equ 50h
LAST_R10B                   equ 50h
LAST_R11                    equ 58h
LAST_R11D                   equ 58h
LAST_R11W                   equ 58h
LAST_R11B                   equ 58h
LAST_R12                    equ 60h
LAST_R12D                   equ 60h
LAST_R12W                   equ 60h
LAST_R12B                   equ 60h
LAST_R13                    equ 68h
LAST_R13D                   equ 68h
LAST_R13W                   equ 68h
LAST_R13B                   equ 68h
LAST_R14                    equ 70h
LAST_R14D                   equ 70h
LAST_R14W                   equ 70h
LAST_R14B                   equ 70h
LAST_R15                    equ 78h
LAST_R15D                   equ 78h
LAST_R15W                   equ 78h
LAST_R15B                   equ 78h
LAST_RIP                    equ 80h
LAST_EIP                    equ 80h
LAST_ECS                    equ 88h
LAST_RFLAGS                 equ 90h
LAST_EFLAGS                 equ 90h
LAST_RSP                    equ 98h
LAST_ESP                    equ 98h
SKIP_MEM_LOG                equ 0a0h
BOTTOM_BOUND                equ 0a8h
TOP_BOUND                   equ 0b0h

%ifdef DEBUG
DebugVar0	DQ 0
DebugVar1	DQ 0
DebugVar2	DQ 0
DebugVar3	DQ 0
DebugVar4	DQ 0
DebugVar5	DQ 0
DebugVar6	DQ 0
DebugVar7	DQ 0
%endif

; Macros:
%macro PUSH_ALL 0
    push RAX
    push RCX
    push RDX
    push RBX
    push RBP
    push RSI
    push RDI
%endmacro

%macro POP_ALL 0
    pop RDI
    pop RSI
    pop RBP
    pop RBX
    pop RDX
    pop RCX
    pop RAX
%endmacro

%macro CALL_ORIGINAL_INTERRUPT 0
	POP_ALL
    swapgs
	; Call original interrupt handler
	jmp	QWORD [orgTrapInterrupt]
%endmacro

%macro RETURN_FROM_INTERRUPT_WITH_CHECK 0
    ; Do I need to call original interrupt
    mov rbx, dr6
    test rbx, BREAK_OTHER_FLAGS
    jz %%JUST_IRET
    CALL_ORIGINAL_INTERRUPT
    %%JUST_IRET:
    ; Clear the DR6, recommended by the Intel-sys-3B.pdf
    xor rbx, rbx
    mov dr6, rbx
    POP_ALL
    swapgs
    iretq
%endmacro

%macro LOG_REGISTER_CHANGE_WITH_STOS 1
	; Get last %1
	mov rax, QWORD [rsp + SAVED_%1]
	cmp rax, [rbp + LAST_%1]
	jz %%DONE_WITH_REG
		mov QWORD [rbp + LAST_%1], rax
		xchg rax, rdx
		stosb
		xchg rax, rdx
		stosq
    %%DONE_WITH_REG:
	inc edx
%endmacro

%macro LOG_RS_CHANGE_WITH_STOS 1
	cmp %1, [rbp + LAST_%1]
	jz %%DONE_WITH_REG
		mov QWORD [rbp + LAST_%1], %1
        mov eax, edx
		stosb
        mov rax, %1
		stosq
    %%DONE_WITH_REG:
	inc edx
%endmacro

SECTION .text
align   16

; Function define
GLOBAL	trap_interrupt
; Inside labels for debugging
GLOBAL  trap_interrupt_target_process
GLOBAL  trap_interrupt_got_log_buffer
GLOBAL  trap_interrupt_got_thread
GLOBAL  trap_interrupt_eip_logged
GLOBAL  trap_interrupt_in_range
GLOBAL  trap_interrupt_check_log_buffer
GLOBAL  trap_interrupt_log_buffer_checked
GLOBAL  trap_interrupt_perform_mem_log
GLOBAL  trap_interrupt_log_registers
GLOBAL  trap_interrupt_save_log_buffer_pos
GLOBAL  trap_interrupt_done
GLOBAL  trap_interrupt_out_of_range

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
trap_interrupt:

; Save all registers
    swapgs
	PUSH_ALL
	; Now the stack looks somthing like this:
SAVED_RDI		equ 000h
SAVED_RSI		equ 008h
SAVED_RBP		equ 010h
SAVED_RBX		equ 018h
SAVED_RDX		equ 020h
SAVED_RCX		equ 028h
SAVED_RAX		equ 030h
; Interrupt call
SAVED_RIP		equ 038h
SAVED_RCS		equ 040h
SAVED_RFLAGS	equ 048h
SAVED_ESP		equ 050h
SAVED_RSP		equ 050h
SAVED_RSS		equ 058h
; TODO: Do I need to set the FS to 0x30 and DS, ES to 0x23 as in _KiTrap01

; Interrupt 0x01 can be called for five reasons:
;   1. Single Step
;   2. Hardware breakpoint on execution
;   3. Hardware breakpoint on memory
;   4. Task switch
;   5. General Detect Fault - A use of the debug registers when they are not available 
; Check the reason for the Interrupt.
    ; push ebx, pop ebx is faster than mov someGlobal, ebx
    mov rax, dr6
    test rax, BREAK_SINGLE_STEP_FLAG_MASK
    jnz INTERRUPT_COZED_BY_SINGLE_STEP
    ; The interupt was not caused for Single Step issues
    %ifdef DEBUG
    mov [DebugVar1], rax
    %endif
    CALL_ORIGINAL_INTERRUPT
INTERRUPT_COZED_BY_SINGLE_STEP:

; Check if this is the traced process
; I use the CR3 (The memory page table pointer) as the process UID
	mov rbx, cr3
    %ifdef DEBUG
    mov [DebugVar2], rbx
    %endif
	mov rcx, [target_process]
	cmp rbx, rcx
	je THIS_IS_THE_TARGET_PROCESS
	CALL_ORIGINAL_INTERRUPT
THIS_IS_THE_TARGET_PROCESS:
trap_interrupt_target_process:

    ; Clear the single step flag from DR6 (http://en.wikipedia.org/wiki/X86_debug_register)
    and rax, ~BREAK_SINGLE_STEP_FLAG_MASK
    mov dr6, rax

    ; Get output buffer pointer
	; I try to keep the buffer_ptr in rax most of the time coz it's used the most.
	; The next place to write is _log_bufer + _log_buffer_pos (Saved at offset zero of the log_buffer).
    ; TODO: On x64 I should use one huge cyclc buffer
	mov rcx, QWORD [log_buffer]
	mov ebx, DWORD [rcx]
	lea rax, [rbx + rcx]
trap_interrupt_got_log_buffer:

	; Check for thread change
    ; RBX would keep the KTHREAD
	mov rbx, [gs:CURRENT_KTHREAD_OFFSET]
    mov rbp, QWORD [lastContext]
	cmp rbx, QWORD [rbp]
	je NO_THREAD_CHANGE
        ; Load context
        ; Should never fail to find thread context.
        mov rdx, rbx
        ; Address is usually QWORD aligned, so for better hashing I shift 2 bits out
        and rdx, THREAD_ID_MASK
        ; Find item in hash table
        ; Every entry is 0x40 bytes long
        ; But I use only bits 6 to 12, so I'm already aligend with the index
        IS_THIS_THE_RIGHT_CONTEXT:
            lea rbp, QWORD [threads]
            add rbp, rdx
            mov rcx, [rbp] ; .ID
            cmp rcx, rbx
            je CONTEXT_FOUND
        TRY_NEXT_THREAD_CONTEXT:
            add rdx, THREAD_CONTEXT_SIZE
            and rdx, THREAD_CONTEXT_ARRAY_END
            lea rbp, QWORD [threads]
            add rbp, rdx
            mov rcx, [rbp] ; .ID
            cmp rcx, rbx
            jne TRY_NEXT_THREAD_CONTEXT
    CONTEXT_FOUND:
        mov [lastContext], rbp
    NO_THREAD_CHANGE:
trap_interrupt_got_thread:

	; Log EIP, also indicates a new cycle
    mov rbx, [rbp + LAST_RIP]
    mov rdx, [rsp + SAVED_RIP]
    mov [rbp + LAST_RIP], rdx
    mov rdx, rbx
trap_interrupt_eip_logged:
    ; If out of user land, get lost
    mov rdx, KERNEL_SPACE_MASK
    test rdx, rbx
    jz NOT_KERNEL_SPACE
        ; Kernel space, get lost
        RETURN_FROM_INTERRUPT_WITH_CHECK
    NOT_KERNEL_SPACE:

    ; Check logging range
    cmp QWORD [rbp + TOP_BOUND], rbx
    jbe OUT_OF_LOGGING_BOUNDS
    TOP_BOUND_OK:
    cmp QWORD [rbp + BOTTOM_BOUND], rbx
    jbe IN_RANGE
    OUT_OF_LOGGING_BOUNDS:
        ; Ok I am now out of the logging range
        ; Go to check other logging ranges
        jmp OUT_OF_LOGGING_RANGE

trap_interrupt_in_range:
    IN_RANGE:
    ; Check if need to write thread change, or not
    mov rcx, [lastLoggedContext]
    cmp rbp, rcx
    je DONE_LOGGING_THREAD_ID
        ; Need to write thread chnage to log
        mov BYTE [rax], THREAD_CHANGE_SYMBOL
        inc rax
        mov ecx, DWORD [rbp] ; threadContext.ID
        mov DWORD [rax], ecx
        add rax, SIZE_OF_DWORD
        mov [lastLoggedContext], rbp
    DONE_LOGGING_THREAD_ID:

	; Write the EIP reg code
	mov BYTE [rax], 0
    ; I log the last executed opcode, so I need the last EIP
	inc rax
	; Write EIP
	mov QWORD [rax], rbx
	; pos += sizeof( EIP )
    add rax, SIZE_OF_POINTER

; TODO: On x64 I should use one huge cyclc buffer
trap_interrupt_check_log_buffer:
	; Check for output buffer end
    mov rcx, QWORD [log_buffer]
	mov edx, DWORD [rcx]
	; Lets say 0x7ff bytes are a must for one iteration
	shr edx, BUFFER_MAX_SIZE_BIT_TO_SHIFT
	; If I miss it once I am totaly fucked!
	xor edx, SHIFTED_LOG_BUFFER_MAX_SIZE
	jnz	LOG_BUFFER_HAS_SPACE
		; Move to the next buffer
        ; First save the last writting point.
        ; It's the beginning of the cycle, but I've already written the EIP
        ; and thread ID
        mov rdx, QWORD [log_buffer]
        sub rax, rdx
        mov DWORD [rdx], eax
        ; Inc the number of buffers used
        loc inc DWORD [used_buffers]
		; Get the next buffer from the buffers array
		mov edx, DWORD [active_log_buffer]
		inc edx
		and edx, NUMBER_OF_BUFFERS_MASK
		; TODO: comper with next_free_log_buffer
		mov DWORD [active_log_buffer], edx
        lea rax, QWORD [log_buffer_item]
        lea rax, [rax + rdx * SIZE_OF_POINTER]
		mov QWORD [log_buffer], rax
		; 4 first bytes are used to save the last pos of the buffer
		mov DWORD [rax], SIZE_OF_DWORD
        add rax, SIZE_OF_DWORD

trap_interrupt_log_buffer_checked:
LOG_BUFFER_HAS_SPACE:
    ; Check the skip mem log flag
    mov ecx, DWORD [rbp + SKIP_MEM_LOG]
    test ecx, ecx
    jz PERFORM_MEM_LOG
        ; Skip the current mem log
        xor edx, edx
        mov DWORD [rbp + SKIP_MEM_LOG], edx
        jmp SKIPING_LOGGING_OF_OPCODE_EFFECT
trap_interrupt_perform_mem_log:
PERFORM_MEM_LOG:
	; Parse Opcode
	%include "opcodeSideEffects64.auto.asm"
	movzx ecx, BYTE [rbx]
	inc rbx
    lea rdx, QWORD [TABLE_ID_0001]
	jmp [rdx + rcx * SIZE_OF_POINTER]

FINISH_LOG_CYCLE:

trap_interrupt_log_registers:
WRITE_ALL_CHANGED_REGISTERS:
	; I'll use edx to hold the regs log ids
	; and ebp to iterate over them
    ; Ids start from 0 which is RIP
	xor edx, edx	
SKIPING_LOGGING_OF_OPCODE_EFFECT:
    ; But I already logged RIP
	inc edx			

	; Get last edi
	mov rcx, QWORD [rbp + LAST_RDI]
	cmp rcx, rdi
	jz DONE_WITH_RDI
		mov QWORD [rbp + LAST_RDI], rdi
		mov BYTE [rax], dl
		inc rax
		mov QWORD [rax], rdi
        add eax, SIZE_OF_QWORD
DONE_WITH_RDI:
	; Inc reg id
	inc edx	; Next is RSI (0x02)
	
	; From now on I shall write them using rdi which just got free for use
	mov rdi, rax

	; Get last rsi
	mov rax, QWORD [rbp + LAST_RSI]
	cmp rax, rsi
	jz DONE_WITH_RSI
		mov QWORD [rbp + LAST_RSI], rsi
		mov eax, edx
		stosb
		mov rax, rsi 
		stosq
DONE_WITH_RSI:
	inc edx ; Next is RBP (0x03)
	
    LOG_REGISTER_CHANGE_WITH_STOS RBP
	; Here comes the kernel esp on the stack, but I don't care about it.
    LOG_REGISTER_CHANGE_WITH_STOS RBX
    LOG_REGISTER_CHANGE_WITH_STOS RDX
    LOG_REGISTER_CHANGE_WITH_STOS RCX
    LOG_REGISTER_CHANGE_WITH_STOS RAX
    inc edx
    ;LOG_REGISTER_CHANGE_WITH_STOS RFLAGS
    inc edx ; Skip EFlags
    LOG_REGISTER_CHANGE_WITH_STOS RSP
    LOG_RS_CHANGE_WITH_STOS R8
    LOG_RS_CHANGE_WITH_STOS R9
    LOG_RS_CHANGE_WITH_STOS R10
    LOG_RS_CHANGE_WITH_STOS R11
    LOG_RS_CHANGE_WITH_STOS R12
    LOG_RS_CHANGE_WITH_STOS R13
    LOG_RS_CHANGE_WITH_STOS R14
    LOG_RS_CHANGE_WITH_STOS R15

trap_interrupt_save_log_buffer_pos:
	; Save log buffer pos (Relatived to the buffer)
	mov rax, QWORD[log_buffer]
	sub rdi, rax
	mov DWORD [rax], edi
	; Continue to return

trap_interrupt_done:
ALL_DONE:
    RETURN_FROM_INTERRUPT_WITH_CHECK

WRITE_LOG_POS_AND_RET:
	; Save log buffer pos (Relatived to the buffer)
	mov rdi, QWORD[log_buffer]
	sub rax, rdi
	mov DWORD [rdi], eax
    RETURN_FROM_INTERRUPT_WITH_CHECK

CLEAR_TRAP_FLAG_AND_RET:
	; Save log buffer pos (Relatived to the buffer)
	mov rdi, QWORD[log_buffer]
	sub rax, rdi
	mov DWORD [rdi], eax
	; Clear the trap flag
	mov eax, DWORD [rsp + SAVED_RFLAGS]
	and rax, ~TRAP_FLAG_MASK
	mov QWORD [rsp + SAVED_RFLAGS], rax
    RETURN_FROM_INTERRUPT_WITH_CHECK

OUT_OF_LOGGING_RANGE:
trap_interrupt_out_of_range:
    ; I got RIP in ebx at this point
    lea rcx, QWORD [loggingRanges]
    cmp [rcx], rbx
    jbe BOTTOM_RANGE_FOUND
    ; I assume that the ranges are sorted by BOTTOM
    ; Find the first range that starts before EIP
    NEXT_RANGE:
        add rcx, 10h  ; sizeof(LoggingRange_t)
        cmp [rcx], rbx
        ja NEXT_RANGE
    BOTTOM_RANGE_FOUND:
    ; Check the TOP bound
    cmp [rcx + 8], rbx
    jbe NOT_IN_ANY_RANGE
    ; Range found
    mov rdx, [rcx]
    mov rcx, [rcx + 8]
    mov [rbp + BOTTOM_BOUND], rdx
    mov [rbp + TOP_BOUND], rcx
    ; Go back to the beginning of the interrupt
    ; just skip the PUSHAD, coze I already done that, and besids
    ; all the registers are now totaly changed.
    mov DWORD [rbp + SKIP_MEM_LOG], 1
    jmp IN_RANGE

    NOT_IN_ANY_RANGE:
    ; When I return to logging, I would have to skip one log cycle
    ; so all registers would get the right values
    ; I have to do it both here and in the range found, because it might
    ; get back right into the current logging range
    mov DWORD [rbp + SKIP_MEM_LOG], 1
    ; Return for now
    ; Note that I didn't write the last writting offset to the log,
    ; because I want the trace to overwrite this cycle
    RETURN_FROM_INTERRUPT_WITH_CHECK

;trap_interrupt ENDP

;END

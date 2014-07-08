
BITS 64
DEFAULT REL

; Defines
THREAD_ID_MASK              equ 0fffh
THREAD_CONTEXT_SIZE         equ 040h
THREAD_CONTEXT_SIZE_IN_BITS equ 06h
THREAD_CONTEXT_ARRAY_END    equ 03ffffh
SKIP_MEM_READ               equ 030h

; Exports
GLOBAL orgStackFaultInterrupt
GLOBAL orgGPFInterrupt
GLOBAL orgPageFaultInterrupt

; Globals
EXTERN target_process
EXTERN lastContext
EXTERN threads

SECTION .data

orgStackFaultInterrupt DQ 0
orgGPFInterrupt        DQ 0
orgPageFaultInterrupt  DQ 0

SECTION .text

; Exportes
GLOBAL loadIdt64
GLOBAL setInterrupt64
GLOBAL stackFaultInterrupt
GLOBAL GPFInterrupt
GLOBAL pageFaultInterrupt

%macro CHECK_PROCESS_AND_THREAD 1
    pushf
    push rax
    push rbx
    
	mov rbx, cr3
    mov rax, [target_process]
    cmp rax, rbx
    je %%DONE_CHECKING

    mov rax, QWORD [lastContext]
    cmp rbx, QWORD [rbx]
    je %%CONTEXT_FOUND

        ; Load context
        ; Should never fail to find thread context, we set the first thread context
        ; when we set the trap flag on.
        push rcx
        push rdx
        mov rdx, rbx
        ; Address is usually DWORD aligne, so for better hashing we shift 2 bits out
        shr rdx, 2
        and rdx, THREAD_ID_MASK
        ; Find item in hash table
        ; Every entry is 0x40 bytes long
        shl rdx, THREAD_CONTEXT_SIZE_IN_BITS
        %%IS_THIS_THE_RIGHT_CONTEXT:
            lea rax, QWORD [threads]
            add rax, rdx
            mov rcx, [rax]
            cmp rcx, rbx
            je %%CONTEXT_FOUND
            add rdx, THREAD_CONTEXT_SIZE
            and rdx, THREAD_CONTEXT_ARRAY_END
        jmp %%IS_THIS_THE_RIGHT_CONTEXT
        %%CONTEXT_FOUND:
        xor ebx, ebx
        inc ebx
        mov [rax + SKIP_MEM_READ], ebx
    
        pop rdx
        pop rcx

%%DONE_CHECKING:
    pop rax
    pop rbx
    popf
    
    jmp QWORD [%1]
%endmacro

stackFaultInterrupt:
CHECK_PROCESS_AND_THREAD orgStackFaultInterrupt

GPFInterrupt:
CHECK_PROCESS_AND_THREAD orgGPFInterrupt

pageFaultInterrupt:
CHECK_PROCESS_AND_THREAD orgPageFaultInterrupt

loadIdt64:
mov rax, rcx
sidt QWORD [rax]
ret

; Args:    IN ADDRESS idt, IN unsigned char interrupt_index, IN interrupt_info_t * new_interrupt
;                     RCX                        RDX                                R8                 
setInterrupt64:
mov rax, rdx
and rax, 00ffh
shl rax, 4
add rax, rcx
mov rdx, r8
cli
mov rcx, [rdx]
mov [rax], rcx
mov rcx, [rdx + 8]
mov [rax + 8], rcx
sti
ret

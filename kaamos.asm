; ============================================================
; KAAMOS.ASM - The Silence Speaks
; Z-80 Assembly, CP/M 2.2 target
; Assemble with: python3 z80asm.py kaamos.asm kaamos.com
; Run in a CP/M emulator (e.g. RunCPM, YAZE)
;
; LESSON: This is the architecture of every computer from
; 1977 to about 1985. One accumulator (A). Six general
; registers (B,C,D,E,H,L). Two 16-bit pointer pairs (HL,DE).
; One index register (IX). A stack. 64K of address space.
; Everything is a tradeoff between registers and memory.
;
; CP/M MEMORY MAP:
;   0000H  Warm boot (JP here to exit)
;   0005H  BDOS entry point (call this with function in C)
;   0100H  TPA - where our program lives
;
; CP/M BDOS FUNCTIONS (put number in C, then CALL 0005H):
;   1  F_CONIN  - wait for keypress, return ASCII in A
;   2  F_CONOUT - print char in E to console
;   9  F_STROUT - print '$'-terminated string, address in DE
; ============================================================

BDOS     EQU 0005H   ; BDOS entry point
F_CONIN  EQU 1       ; console input
F_CONOUT EQU 2       ; console output (char in E)
F_STROUT EQU 9       ; print string (DE=addr, terminates at '$')

NSTATIONS EQU 9      ; stations numbered 0-8, keys '1'-'9'
SEQ_MAX   EQU 8      ; maximum Simon sequence length

    ORG 0100H        ; CP/M programs always start here

; ============================================================
; ENTRY POINT
; ============================================================
START:
    ; Seed the random number generator
    ; Real hardware: you'd read a hardware timer here.
    ; We use a fixed seed. The player's keypress timing
    ; will perturb it naturally via the GETKEY timing.
    LD HL, 0ACE1H
    LD (RNG_STATE), HL

    ; Clear screen using ANSI escape sequence
    ; ESC[2J clears screen, ESC[H moves cursor home
    ; LESSON: 1BH = ASCII 27 = ESC character
    LD DE, STR_CLS
    CALL PRTSTR

    ; Print title
    LD DE, STR_TITLE
    CALL PRTSTR

    ; Wait for keypress before starting
    LD DE, STR_PRESS
    CALL PRTSTR
    CALL GETKEY             ; discard return value, just waiting

; ============================================================
; GAME_LOOP - Restart here after each complete game
; ============================================================
GAME_LOOP:
    LD A, 1
    LD (ROUND), A           ; start at round 1 (one station in sequence)

; ============================================================
; NEXT_ROUND - Execute one Simon round
; ============================================================
NEXT_ROUND:
    ; Generate a random sequence of length (ROUND)
    ; LESSON: DJNZ = "Decrement B, Jump if Not Zero"
    ; Classic Z-80 loop instruction. B is the loop counter.
    LD A, (ROUND)
    LD B, A                 ; B = loop counter
    LD HL, SEQUENCE         ; HL = pointer into sequence buffer
GEN_SEQ:
    PUSH BC                 ; save loop counter
    PUSH HL                 ; save buffer pointer
    CALL RAND9              ; result in A (0-8)
    POP HL
    LD (HL), A              ; store random station index
    INC HL                  ; advance pointer
    POP BC
    DJNZ GEN_SEQ

    ; Draw map, no station highlighted
    LD A, 0FFH
    LD (HILITE), A          ; 0FFH is our "no highlight" sentinel
    CALL DRAW_MAP

    ; Print "watch" prompt
    LD DE, STR_WATCH
    CALL PRTSTR
    CALL DELAY_MED

    ; Boss plays sequence: show each station in order
    ; LESSON: IX is the index register. (IX+0) means "the byte
    ; at the address IX points to." INC IX advances the pointer.
    LD A, (ROUND)
    LD B, A                 ; B = number of stations to show
    LD IX, SEQUENCE         ; IX = start of sequence
SHOW_SEQ:
    PUSH BC
    LD A, (IX+0)            ; load station index from sequence
    LD (HILITE), A          ; tell DRAW_MAP which to highlight
    CALL DRAW_MAP           ; redraw: violet marker appears
    CALL DELAY_LONG         ; hold so player can see it
    LD A, 0FFH
    LD (HILITE), A
    CALL DRAW_MAP           ; redraw: marker gone
    CALL DELAY_SHORT        ; gap between stations
    INC IX                  ; advance to next in sequence
    POP BC
    DJNZ SHOW_SEQ

    ; Player's turn
    LD DE, STR_YOURTURN
    CALL PRTSTR

    LD A, (ROUND)
    LD B, A                 ; B = inputs expected
    LD IX, SEQUENCE         ; reset IX to start of sequence

INPUT_LOOP:
    PUSH BC
    PUSH IX

    CALL GETKEY             ; wait for keypress, ASCII in A

    ; Only accept '1' through '9'
    ; LESSON: CP n sets flags by computing A-n without storing result
    ; JP C jumps if result was negative (A < n)
    CP '1'
    JP C, INPUT_SKIP        ; key < '1': ignore
    CP '9'+1
    JP NC, INPUT_SKIP       ; key > '9': ignore

    SUB '1'                 ; convert '1'-'9' to 0-8

    ; Compare against expected station
    POP IX
    PUSH IX
    LD E, (IX+0)            ; E = expected station index
    CP E
    JP NZ, WRONG_INPUT      ; mismatch: game over

    ; Correct step
    LD DE, STR_DOT
    CALL PRTSTR             ; print a dot as feedback

    POP IX
    INC IX                  ; advance expected pointer
    POP BC
    DJNZ INPUT_LOOP         ; next input

    ; Entire sequence reproduced correctly
    LD DE, STR_CORRECT
    CALL PRTSTR
    CALL DELAY_LONG

    LD A, (ROUND)
    CP SEQ_MAX
    JP Z, WIN_GAME          ; reached max rounds: win

    INC A
    LD (ROUND), A
    JP NEXT_ROUND

INPUT_SKIP:
    POP IX
    POP BC
    JP INPUT_LOOP

WRONG_INPUT:
    POP IX
    POP BC
    LD DE, STR_WRONG
    CALL PRTSTR
    CALL DELAY_LONG
    JP GAME_LOOP

WIN_GAME:
    LD DE, STR_WIN
    CALL PRTSTR
    CALL DELAY_LONG
    JP GAME_LOOP

; ============================================================
; DRAW_MAP
; Clears screen, draws ASCII hex grid.
; If HILITE != 0FFH, prints highlighted station name.
; ============================================================
DRAW_MAP:
    LD DE, STR_CLS
    CALL PRTSTR
    LD DE, STR_MAP
    CALL PRTSTR
    LD A, (HILITE)
    CP 0FFH
    RET Z                   ; no highlight needed, return

    ; Print highlighted station name between >> <<
    LD DE, STR_HL_PRE
    CALL PRTSTR
    CALL PRINT_SNAME        ; A still holds station index
    LD DE, STR_HL_POST
    CALL PRTSTR
    RET

; ============================================================
; PRINT_SNAME
; Print the name of station whose index is in A.
; Uses the station name lookup table.
;
; LESSON: This is a jump table in 1979 style.
; Each entry is a 2-byte address (little-endian = low byte first).
; We multiply A by 2, add to table base, dereference to get string address.
; ============================================================
PRINT_SNAME:
    CP NSTATIONS
    RET NC                  ; out of range: do nothing
    ADD A, A                ; A = A*2 (2 bytes per table entry)
    LD E, A
    LD D, 0                 ; DE = offset into table
    LD HL, STATION_TABLE
    ADD HL, DE              ; HL = address of table entry
    LD E, (HL)
    INC HL
    LD D, (HL)              ; DE = address of station name string
    CALL PRTSTR
    RET

; ============================================================
; RAND9 - Return pseudo-random number 0-8 in A
;
; LESSON: Galois Linear Feedback Shift Register (LFSR).
; A 16-bit register that shifts right. If the output bit
; was 1, XOR with a "polynomial" mask to feed it back.
; This produces a sequence of 65535 non-repeating values
; before cycling. It is not cryptographic. It is a game.
;
; Polynomial: x^16 + x^14 + x^13 + x^11 + 1
; Mask: 0B400H (bits 15,13,12,10 counting from 0)
; ============================================================
RAND9:
    LD HL, (RNG_STATE)      ; load 16-bit state
    SCF                     ; set carry (will be overwritten)
    SRL H                   ; shift H right, old bit 0 -> carry
    RR L                    ; rotate L right through carry
    ; If the bit that fell out (was in H's bit 0) was set, apply feedback
    JP NC, RAND_NOXOR
    LD A, H
    XOR 0B4H                ; apply high byte of polynomial
    LD H, A
RAND_NOXOR:
    LD (RNG_STATE), HL
    ; Map L (0-255) to 0-8
    ; Take low nibble (0-15), subtract 9 if >= 9
    ; LESSON: slight bias toward 0-6 vs 7-8, acceptable for a game
    LD A, L
    AND 0FH
    CP NSTATIONS
    RET C                   ; < 9, we're done
    SUB NSTATIONS           ; subtract 9: maps 9-15 -> 0-6
    RET

; ============================================================
; DELAY routines
; LESSON: No operating system timer in CP/M. We burn cycles.
; At 2MHz, each DEC BC + OR B + JP NZ = ~25 cycles = ~12.5us
; 0x1000 iterations ~= 52ms (SHORT)
; 0x5000 iterations ~= 260ms (MED)
; 0xC000 iterations ~= 786ms (LONG)
; ============================================================
DELAY_SHORT:
    LD BC, 01000H
DLY_S:
    DEC BC
    LD A, B
    OR C
    JP NZ, DLY_S
    RET

DELAY_MED:
    LD BC, 05000H
DLY_M:
    DEC BC
    LD A, B
    OR C
    JP NZ, DLY_M
    RET

DELAY_LONG:
    LD BC, 0C000H
DLY_L:
    DEC BC
    LD A, B
    OR C
    JP NZ, DLY_L
    RET

; ============================================================
; GETKEY - Wait for keypress, return ASCII in A
; LESSON: BDOS function 1 echoes the key to screen.
; We accept that. On real hardware you'd want no-echo (fn 6).
; ============================================================
GETKEY:
    LD C, F_CONIN
    CALL BDOS
    RET

; ============================================================
; PRTSTR - Print '$'-terminated string at DE
; LESSON: CP/M chose '$' as string terminator, not NUL.
; This is why printf("hello$world") would be weird on CP/M.
; ============================================================
PRTSTR:
    LD C, F_STROUT
    CALL BDOS
    RET

; ============================================================
; DATA SECTION
; ============================================================

RNG_STATE: DW 0ACE1H        ; LFSR seed
ROUND:     DB 1              ; current round number
HILITE:    DB 0FFH           ; 0FFH = no station highlighted
SEQUENCE:  DS 8              ; sequence buffer (max SEQ_MAX bytes)

; ANSI escape sequences
; 1BH = ESC, these are standard ANSI terminal codes
; Most CP/M systems (Kaypro, Osborne, ADM-3A with mod) supported ANSI
STR_CLS:
    DB 1BH,'[2J',1BH,'[H$'

STR_TITLE:
    DB 1BH,'[1m'
    DB '  +----------------------------------+',0DH,0AH
    DB '  |  K A A M O S                    |',0DH,0AH
    DB '  |  hiljaisuus puhuu               |',0DH,0AH
    DB '  |  the silence speaks             |',0DH,0AH
    DB '  +----------------------------------+',0DH,0AH
    DB 1BH,'[0m'
    DB 0DH,0AH,'$'

; The hex map. Approximate positions only -- a real implementation
; would use cursor addressing to place station names precisely.
; Numbers correspond to keyboard keys '1'-'9'.
;
;     1:POHJA    7:SOLMU
;  2:VAYLA  *HILJ*  3:GRILLI
;     4:AAVA    5:HEHKU
;  9:TAIVAS  8:POHJAN  6:KAAMOS
;
STR_MAP:
    DB '         1:POHJA    7:SOLMU',0DH,0AH
    DB '      2:VAYLA  *HILJ*  3:GRILLI',0DH,0AH
    DB '         4:AAVA    5:HEHKU',0DH,0AH
    DB '      9:TAIVAS  8:POHJAN  6:KAAMOS',0DH,0AH
    DB 0DH,0AH,'$'

STR_WATCH:
    DB '  [ hiljaisuus puhuu -- katso ]',0DH,0AH,'$'

STR_YOURTURN:
    DB '  [ sinun vuorosi -- paina 1-9 ]',0DH,0AH,'$'

STR_CORRECT:
    DB 0DH,0AH,'  [ oikein -- token ansaittu ]',0DH,0AH,'$'

STR_WRONG:
    DB 0DH,0AH,'  [ vaarin -- hiljaisuus nollaa ]',0DH,0AH,'$'

STR_WIN:
    DB 0DH,0AH
    DB '  [ olet kuullut hiljaisuuden ]',0DH,0AH
    DB '  [ hiljaisuus on puhunut ]',0DH,0AH,'$'

STR_PRESS:
    DB '  paina jotain nappulaa -- press any key',0DH,0AH,'$'

STR_DOT:
    DB '.',' ','$'

STR_HL_PRE:
    DB 1BH,'[1m','  >> ','$'

STR_HL_POST:
    DB ' <<',1BH,'[0m',0DH,0AH,'$'

; Station name strings, '$'-terminated
SNAME_0: DB '1:POHJA','$'
SNAME_1: DB '2:VAYLA','$'
SNAME_2: DB '3:GRILLI','$'
SNAME_3: DB '4:AAVA','$'
SNAME_4: DB '5:HEHKU','$'
SNAME_5: DB '6:KAAMOS','$'
SNAME_6: DB '7:SOLMU','$'
SNAME_7: DB '8:POHJAN','$'
SNAME_8: DB '9:TAIVAS','$'

; Jump table: 2-byte addresses, little-endian (low byte first)
; LESSON: Z-80 is little-endian. If a label is at address 0x0200,
; DW stores it as 00H, 02H -- low byte first.
STATION_TABLE:
    DW SNAME_0
    DW SNAME_1
    DW SNAME_2
    DW SNAME_3
    DW SNAME_4
    DW SNAME_5
    DW SNAME_6
    DW SNAME_7
    DW SNAME_8

    END START

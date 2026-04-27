#!/usr/bin/env python3
"""
z80asm.py - Minimal two-pass Z-80 assembler
Written for KAAMOS / CP/M. Handles the instruction subset in kaamos.asm.

Usage: python3 z80asm.py kaamos.asm kaamos.com

LESSON: A two-pass assembler works like this:
  Pass 1: Walk every line, track how big each instruction will be,
          record the address of every label. We don't know forward
          references yet (labels defined later in the file), but we
          know addresses.
  Pass 2: Walk every line again. Now all labels are known. Encode
          every instruction to bytes. Write the binary.

Z-80 register codes (used when building opcodes):
  B=0  C=1  D=2  E=3  H=4  L=5  (HL)=6  A=7
  These are 3-bit fields embedded in many opcodes.
"""

import sys
import re

# ─── REGISTER TABLES ──────────────────────────────────────────────────────

# 8-bit register -> 3-bit code
REG8 = {'B': 0, 'C': 1, 'D': 2, 'E': 3, 'H': 4, 'L': 5, 'A': 7}

# 16-bit register pairs for LD rr,nn
REG16 = {'BC': 0, 'DE': 1, 'HL': 2, 'SP': 3}

# PUSH/POP encodings
PUSH_OP = {'BC': 0xC5, 'DE': 0xD5, 'HL': 0xE5, 'AF': 0xF5}
POP_OP  = {'BC': 0xC1, 'DE': 0xD1, 'HL': 0xE1, 'AF': 0xF1}

# All directives and mnemonics (uppercase)
MNEMONICS = {
    'LD','INC','DEC','ADD','SUB','AND','OR','XOR','CP',
    'JP','CALL','RET','PUSH','POP','DJNZ',
    'SRL','RR','RRA','RLA','SCF','NOP',
    'ORG','EQU','DB','DW','DS','END'
}

# ─── LITERAL PARSER ───────────────────────────────────────────────────────

def parse_value(s, labels):
    """
    Parse a numeric expression.
    Supports: hex (0FFH or 0xFF), decimal, char ('A'), label name.
    LESSON: All these formats appear in Z-80 source. The assembler
    must handle all of them.
    """
    s = s.strip()
    if not s:
        raise ValueError("empty value")
    # Hex with H suffix: 0FFH, 0B4H, 0100H
    if re.match(r'^[0-9A-Fa-f]+[Hh]$', s):
        return int(s[:-1], 16)
    # Hex with 0x prefix
    if s.startswith('0x') or s.startswith('0X'):
        return int(s, 16)
    # Decimal
    if re.match(r'^-?\d+$', s):
        return int(s)
    # Character literal: 'A' -> 65
    if re.match(r"^'.'$", s):
        return ord(s[1])
    # Char+1 arithmetic: '9'+1
    m = re.match(r"^'(.)'(\+\d+)$", s)
    if m:
        return ord(m.group(1)) + int(m.group(2))
    # Label
    if re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', s):
        if s.upper() in labels:
            return labels[s.upper()]
        if s in labels:
            return labels[s]
        raise ValueError(f"undefined label: {s!r}")
    raise ValueError(f"cannot parse value: {s!r}")

# ─── DB STRING PARSER ─────────────────────────────────────────────────────

def parse_db_operands(ops_str, labels):
    """
    Parse the operand list for a DB directive.
    Can include quoted strings ('hello'), hex values (0DH), and labels.
    LESSON: DB is the workhorse of data definition. In Z-80 assembly,
    strings live in DB statements. The '$' terminator used by CP/M PRTSTR
    is just ASCII 0x24 - it's not special to the assembler, only to BDOS.
    """
    result = []
    # We need to tokenize carefully because strings may contain commas
    i = 0
    s = ops_str.strip()
    tokens = []
    current = ''
    in_str = False
    quote_char = None

    for ch in s:
        if in_str:
            if ch == quote_char:
                in_str = False
                tokens.append(('str', current))
                current = ''
            else:
                current += ch
        elif ch in ('"', "'"):
            if current.strip():
                tokens.append(('val', current.strip()))
            current = ''
            in_str = True
            quote_char = ch
        elif ch == ',':
            if current.strip():
                tokens.append(('val', current.strip()))
            current = ''
        else:
            current += ch

    if in_str:
        raise ValueError(f"unterminated string: {s!r}")
    if current.strip():
        tokens.append(('val', current.strip()))

    for typ, val in tokens:
        if typ == 'str':
            for ch in val:
                result.append(ord(ch) & 0xFF)
        else:
            result.append(parse_value(val, labels) & 0xFF)

    return result

# ─── INSTRUCTION ENCODER ──────────────────────────────────────────────────

def encode(mnemonic, ops_str, labels, pc):
    """
    Encode one instruction to a list of bytes.

    LESSON: Z-80 opcode structure for common cases:
      LD r, r'  : 01 DDD SSS  (D=dest reg code, S=src reg code)
      LD r, n   : 00 DDD 110 followed by byte n
      LD rr, nn : 00 RR0001   followed by 16-bit nn (little-endian)
      INC r     : 00 DDD 100
      DEC r     : 00 DDD 101
      ADD A, r  : 10 000 SSS
      OR r      : 10 110 SSS
      AND n     : 11 100 110  n
      CP n      : 11 111 110  n
      JP cc,nn  : 11 CCC 010  lo hi
      CALL nn   : 11 001 101  lo hi
      RET       : 11 001 001
      PUSH rr   : 11 RR0101
      POP rr    : 11 RR0001
      DJNZ e    : 00 010 000  offset (signed, relative)
    """
    # Split operands on comma, but not inside parens
    ops = []
    if ops_str:
        depth = 0
        cur = ''
        for ch in ops_str:
            if ch == '(':
                depth += 1
                cur += ch
            elif ch == ')':
                depth -= 1
                cur += ch
            elif ch == ',' and depth == 0:
                ops.append(cur.strip())
                cur = ''
            else:
                cur += ch
        if cur.strip():
            ops.append(cur.strip())

    def val(s):
        return parse_value(s, labels)

    def lo(n): return n & 0xFF
    def hi(n): return (n >> 8) & 0xFF

    def nn_bytes(s):
        n = val(s) & 0xFFFF
        return [lo(n), hi(n)]

    # ── LD ──────────────────────────────────────────────────────────────
    if mnemonic == 'LD':
        dst, src = ops[0], ops[1]

        # LD HL, (addr)
        if dst == 'HL' and src.startswith('(') and src.endswith(')'):
            inner = src[1:-1]
            n = val(inner) & 0xFFFF
            return [0x2A, lo(n), hi(n)]

        # LD (addr), HL
        if dst.startswith('(') and dst.endswith(')') and src == 'HL':
            n = val(dst[1:-1]) & 0xFFFF
            return [0x22, lo(n), hi(n)]

        # LD r, (IX+d)  -- must check before generic (addr) handlers
        ix_src = re.match(r'^\(IX\+(\w+)\)$', src)
        if ix_src and dst in REG8:
            d = val(ix_src.group(1)) & 0xFF
            # opcode: DD 01 DDD 110  (LD r,(IX+d))
            return [0xDD, 0x46 | (REG8[dst] << 3), d]

        # LD (IX+d), r
        ix_dst = re.match(r'^\(IX\+(\w+)\)$', dst)
        if ix_dst and src in REG8:
            d = val(ix_dst.group(1)) & 0xFF
            return [0xDD, 0x70 | REG8[src], d]

        # LD IX, nn
        if dst == 'IX':
            n = val(src) & 0xFFFF
            return [0xDD, 0x21, lo(n), hi(n)]

        # LD (HL), r
        if dst == '(HL)' and src in REG8:
            return [0x70 | REG8[src]]

        # LD r, (HL)
        if dst in REG8 and src == '(HL)':
            return [0x40 | (REG8[dst] << 3) | 6]  # 01 DDD 110

        # LD A, (addr)  [not BC, DE, or HL indirect]
        if dst == 'A' and src.startswith('(') and src.endswith(')'):
            inner = src[1:-1]
            if inner == 'BC': return [0x0A]
            if inner == 'DE': return [0x1A]
            if inner == 'HL': return [0x7E]
            n = val(inner) & 0xFFFF
            return [0x3A, lo(n), hi(n)]

        # LD (addr), A
        if dst.startswith('(') and dst.endswith(')') and src == 'A':
            inner = dst[1:-1]
            if inner == 'HL': return [0x77]
            n = val(inner) & 0xFFFF
            return [0x32, lo(n), hi(n)]

        # LD rr, nn  (16-bit immediate)
        if dst in REG16:
            base_op = [0x01, 0x11, 0x21, 0x31][REG16[dst]]
            return [base_op] + nn_bytes(src)

        # LD r, r'  (register to register)
        if dst in REG8 and src in REG8:
            return [0x40 | (REG8[dst] << 3) | REG8[src]]

        # LD r, n  (8-bit immediate)
        if dst in REG8:
            return [0x06 | (REG8[dst] << 3), val(src) & 0xFF]

        raise ValueError(f"LD not handled: {dst}, {src}")

    # ── INC ─────────────────────────────────────────────────────────────
    if mnemonic == 'INC':
        r = ops[0]
        if r in REG8:       return [0x04 | (REG8[r] << 3)]
        if r == '(HL)':     return [0x34]
        if r == 'BC':       return [0x03]
        if r == 'DE':       return [0x13]
        if r == 'HL':       return [0x23]
        if r == 'SP':       return [0x33]
        if r == 'IX':       return [0xDD, 0x23]
        raise ValueError(f"INC {r}")

    # ── DEC ─────────────────────────────────────────────────────────────
    if mnemonic == 'DEC':
        r = ops[0]
        if r in REG8:       return [0x05 | (REG8[r] << 3)]
        if r == '(HL)':     return [0x35]
        if r == 'BC':       return [0x0B]
        if r == 'DE':       return [0x1B]
        if r == 'HL':       return [0x2B]
        if r == 'SP':       return [0x3B]
        raise ValueError(f"DEC {r}")

    # ── ADD ─────────────────────────────────────────────────────────────
    if mnemonic == 'ADD':
        dst, src = ops[0], ops[1]
        if dst == 'A':
            if src in REG8: return [0x80 | REG8[src]]
            return [0xC6, val(src) & 0xFF]         # ADD A, n
        if dst == 'HL':
            rr = {'BC':0x09,'DE':0x19,'HL':0x29,'SP':0x39}
            return [rr[src]]
        raise ValueError(f"ADD {dst},{src}")

    # ── SUB ─────────────────────────────────────────────────────────────
    if mnemonic == 'SUB':
        r = ops[0]
        if r in REG8: return [0x90 | REG8[r]]
        return [0xD6, val(r) & 0xFF]

    # ── AND / OR / XOR / CP ─────────────────────────────────────────────
    if mnemonic == 'AND':
        r = ops[0]
        if r in REG8: return [0xA0 | REG8[r]]
        return [0xE6, val(r) & 0xFF]

    if mnemonic == 'OR':
        r = ops[0]
        if r in REG8: return [0xB0 | REG8[r]]
        return [0xF6, val(r) & 0xFF]

    if mnemonic == 'XOR':
        r = ops[0]
        if r in REG8: return [0xA8 | REG8[r]]
        return [0xEE, val(r) & 0xFF]

    if mnemonic == 'CP':
        r = ops[0]
        if r in REG8: return [0xB8 | REG8[r]]
        return [0xFE, val(r) & 0xFF]

    # ── JP ──────────────────────────────────────────────────────────────
    if mnemonic == 'JP':
        cc_map = {'NZ':0xC2,'Z':0xCA,'NC':0xD2,'C':0xDA,
                  'PO':0xE2,'PE':0xEA,'P':0xF2,'M':0xFA}
        if len(ops) == 1:
            return [0xC3] + nn_bytes(ops[0])
        cond, tgt = ops[0].upper(), ops[1]
        return [cc_map[cond]] + nn_bytes(tgt)

    # ── CALL ────────────────────────────────────────────────────────────
    if mnemonic == 'CALL':
        if len(ops) == 1:
            return [0xCD] + nn_bytes(ops[0])
        cc_map = {'NZ':0xC4,'Z':0xCC,'NC':0xD4,'C':0xDC}
        return [cc_map[ops[0].upper()]] + nn_bytes(ops[1])

    # ── RET ─────────────────────────────────────────────────────────────
    if mnemonic == 'RET':
        if not ops: return [0xC9]
        cc_map = {'NZ':0xC0,'Z':0xC8,'NC':0xD0,'C':0xD8,
                  'PO':0xE0,'PE':0xE8,'P':0xF0,'M':0xF8}
        return [cc_map[ops[0].upper()]]

    # ── PUSH / POP ──────────────────────────────────────────────────────
    if mnemonic == 'PUSH':
        r = ops[0]
        if r == 'IX': return [0xDD, 0xE5]
        return [PUSH_OP[r]]

    if mnemonic == 'POP':
        r = ops[0]
        if r == 'IX': return [0xDD, 0xE1]
        return [POP_OP[r]]

    # ── DJNZ ────────────────────────────────────────────────────────────
    if mnemonic == 'DJNZ':
        target = val(ops[0]) & 0xFFFF
        offset = target - (pc + 2)
        if offset < -128 or offset > 127:
            raise ValueError(f"DJNZ offset out of range: {offset}")
        return [0x10, offset & 0xFF]

    # ── SHIFTS / ROTATES ────────────────────────────────────────────────
    if mnemonic == 'SRL':
        r = ops[0]
        if r in REG8: return [0xCB, 0x38 | REG8[r]]
        raise ValueError(f"SRL {r}")

    if mnemonic == 'RR':
        r = ops[0]
        if r in REG8: return [0xCB, 0x18 | REG8[r]]
        raise ValueError(f"RR {r}")

    if mnemonic == 'RRA': return [0x1F]
    if mnemonic == 'RLA': return [0x17]
    if mnemonic == 'SCF': return [0x37]
    if mnemonic == 'NOP': return [0x00]

    raise ValueError(f"unknown instruction: {mnemonic} {ops_str!r}")

# ─── LINE PARSER ──────────────────────────────────────────────────────────

def parse_line(raw):
    """
    Parse one source line.
    Returns: (label_or_None, mnemonic_or_None, operands_string_or_None)

    A label is a word at column 0 (possibly followed by a colon).
    A mnemonic starts with whitespace or follows a label.
    """
    # Strip comment
    line = raw
    if ';' in line:
        line = line[:line.index(';')]
    line = line.rstrip()

    if not line.strip():
        return None, None, None

    # Does the line start at column 0?
    starts_at_col0 = line[0] not in (' ', '\t')

    stripped = line.strip()

    # Match: optional_label  optional_mnemonic  optional_operands
    m = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)\s*(.*)', stripped)
    if not m:
        return None, None, None

    word1 = m.group(1).upper()
    rest  = m.group(2).strip()

    if starts_at_col0:
        # word1 might be a label or a mnemonic
        if word1 in MNEMONICS:
            # It's a mnemonic at column 0 (unusual but valid)
            return None, word1, rest
        else:
            # It's a label. Strip optional colon.
            label = m.group(1).rstrip(':')
            # Is there a mnemonic after the label?
            m2 = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)\s*(.*)', rest)
            if m2 and m2.group(1).upper() in MNEMONICS:
                return label, m2.group(1).upper(), m2.group(2).strip()
            return label, None, None
    else:
        # Starts with whitespace: word1 must be a mnemonic
        return None, word1, rest

# ─── INSTRUCTION SIZE ESTIMATOR (Pass 1) ──────────────────────────────────

def estimate_size(mnemonic, ops_str, dummy_labels):
    """
    Estimate the byte size of an instruction for Pass 1.
    We use dummy_labels (all labels = 0) since forward refs aren't resolved yet.
    If estimation fails, return 3 (safe upper bound for most instructions).
    """
    try:
        return len(encode(mnemonic, ops_str, dummy_labels, 0))
    except Exception:
        return 3

# ─── TWO-PASS ASSEMBLER ───────────────────────────────────────────────────

def assemble(source_lines):
    """
    Two-pass Z-80 assembler.
    Returns bytes object: the assembled binary starting at ORG address.
    """
    errors = 0

    # ── PASS 1: Collect labels ────────────────────────────────────────
    labels = {}     # name (uppercase) -> address
    pc = 0x0100     # default start for CP/M
    org = 0x0100

    for lineno, raw in enumerate(source_lines, 1):
        try:
            label, mnemonic, ops_str = parse_line(raw)
        except Exception as e:
            print(f"  Line {lineno}: parse error: {e}", file=sys.stderr)
            errors += 1
            continue

        if label:
            labels[label.upper()] = pc

        if mnemonic is None:
            continue

        ops_str = ops_str or ''

        try:
            if mnemonic == 'ORG':
                pc = parse_value(ops_str.split(',')[0].strip(), labels)
                org = min(org, pc)
            elif mnemonic == 'EQU':
                if label:
                    v = parse_value(ops_str.strip(), labels)
                    labels[label.upper()] = v
            elif mnemonic == 'DB':
                dummy = dict(labels)
                pc += len(parse_db_operands(ops_str, dummy))
            elif mnemonic == 'DW':
                ops = [o.strip() for o in ops_str.split(',')]
                pc += 2 * len(ops)
            elif mnemonic == 'DS':
                pc += int(ops_str.strip().split(',')[0])
            elif mnemonic == 'END':
                break
            else:
                dummy = {k: 0 for k in labels}
                dummy.update(labels)
                pc += estimate_size(mnemonic, ops_str, dummy)
        except Exception as e:
            print(f"  Line {lineno} (pass 1): {e}", file=sys.stderr)
            errors += 1

    # ── PASS 2: Emit bytes ────────────────────────────────────────────
    output = bytearray()
    pc = 0x0100

    for lineno, raw in enumerate(source_lines, 1):
        try:
            label, mnemonic, ops_str = parse_line(raw)
        except Exception:
            continue

        if mnemonic is None:
            continue

        ops_str = ops_str or ''

        try:
            if mnemonic == 'ORG':
                new_pc = parse_value(ops_str.strip(), labels)
                if new_pc > pc:
                    output.extend([0x00] * (new_pc - pc))
                pc = new_pc
            elif mnemonic == 'EQU':
                pass
            elif mnemonic == 'DB':
                data = parse_db_operands(ops_str, labels)
                output.extend(data)
                pc += len(data)
            elif mnemonic == 'DW':
                for op in [o.strip() for o in ops_str.split(',')]:
                    n = parse_value(op, labels) & 0xFFFF
                    output.extend([n & 0xFF, (n >> 8) & 0xFF])
                    pc += 2
            elif mnemonic == 'DS':
                n = int(ops_str.strip().split(',')[0])
                output.extend([0x00] * n)
                pc += n
            elif mnemonic == 'END':
                break
            else:
                encoded = encode(mnemonic, ops_str, labels, pc)
                output.extend(encoded)
                pc += len(encoded)
        except Exception as e:
            print(f"  Line {lineno} [{mnemonic} {ops_str}]: {e}", file=sys.stderr)
            errors += 1

    return bytes(output), errors

# ─── DISASSEMBLY LISTING (educational) ───────────────────────────────────

def print_listing(binary, start_addr=0x0100):
    """Print a hex dump with addresses. Helps you see the bytes."""
    print(f"\n  Address  Bytes                         (first 64 bytes)")
    print(f"  -------  -----")
    for i in range(0, min(64, len(binary)), 8):
        addr = start_addr + i
        chunk = binary[i:i+8]
        hex_part = ' '.join(f'{b:02X}' for b in chunk)
        print(f"  {addr:04X}     {hex_part}")
    print()

# ─── MAIN ─────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 z80asm.py input.asm output.com")
        sys.exit(1)

    src_file = sys.argv[1]
    out_file = sys.argv[2]

    print(f"\n  Z-80 Assembler for KAAMOS")
    print(f"  Input:  {src_file}")
    print(f"  Output: {out_file}\n")

    with open(src_file, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()

    print(f"  Pass 1: collecting labels...")
    binary, errors = assemble(lines)
    print(f"  Pass 2: encoding instructions...")

    if errors:
        print(f"\n  {errors} error(s). Binary may be incomplete.")
    else:
        print(f"  No errors.")

    print(f"  {len(binary)} bytes assembled")

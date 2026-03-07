#!/usr/bin/env python3
"""Compile .po to .mo file."""
import struct
import re
import sys

def parse_po(po_path):
    messages = {}
    with open(po_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split on empty lines or comment lines
    entries = re.split(r'\n(?=msgid )', content)
    
    for entry in entries:
        lines = entry.strip().split('\n')
        msgid_parts = []
        msgstr_parts = []
        current = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('#') or not line:
                continue
            if line.startswith('msgid "'):
                current = 'id'
                msgid_parts.append(line[7:-1])
            elif line.startswith('msgstr "'):
                current = 'str'
                msgstr_parts.append(line[8:-1])
            elif line.startswith('"') and line.endswith('"'):
                if current == 'id':
                    msgid_parts.append(line[1:-1])
                elif current == 'str':
                    msgstr_parts.append(line[1:-1])
        
        msgid = ''.join(msgid_parts)
        msgstr = ''.join(msgstr_parts)
        
        # Unescape
        for old, new in [('\\n', '\n'), ('\\t', '\t'), ('\\"', '"'), ('\\\\', '\\')]:
            msgid = msgid.replace(old, new)
            msgstr = msgstr.replace(old, new)
        
        if msgstr:  # Only add if translation exists
            messages[msgid] = msgstr
    
    return messages


def write_mo(mo_path, messages):
    keys = sorted(messages.keys())
    
    offsets = []
    ids_data = b''
    strs_data = b''
    
    key_offsets = []
    val_offsets = []
    
    for key in keys:
        encoded = key.encode('utf-8')
        key_offsets.append((len(encoded), len(ids_data)))
        ids_data += encoded + b'\x00'
    
    for key in keys:
        encoded = messages[key].encode('utf-8')
        val_offsets.append((len(encoded), len(strs_data)))
        strs_data += encoded + b'\x00'
    
    n = len(keys)
    # Header: magic, version, nstrings, offset_orig, offset_trans, hash_size, hash_offset
    header_size = 7 * 4  # 28 bytes
    table_size = n * 2 * 4  # each entry is (length, offset) = 2 ints
    
    orig_table_offset = header_size
    trans_table_offset = header_size + table_size
    data_offset = header_size + 2 * table_size
    
    output = struct.pack(
        '=Iiiiiii',
        0x950412de,       # magic
        0,                # version
        n,                # nstrings
        orig_table_offset,
        trans_table_offset,
        0, 0              # hash
    )
    
    # Original strings table
    for length, offset in key_offsets:
        output += struct.pack('=ii', length, data_offset + offset)
    
    # Translation strings table
    strs_base = data_offset + len(ids_data)
    for length, offset in val_offsets:
        output += struct.pack('=ii', length, strs_base + offset)
    
    output += ids_data
    output += strs_data
    
    with open(mo_path, 'wb') as f:
        f.write(output)
    
    print(f'Compiled {n} messages to {mo_path}')


if __name__ == '__main__':
    po_path = sys.argv[1] if len(sys.argv) > 1 else 'locale/tr/LC_MESSAGES/django.po'
    mo_path = sys.argv[2] if len(sys.argv) > 2 else 'locale/tr/LC_MESSAGES/django.mo'
    messages = parse_po(po_path)
    write_mo(mo_path, messages)

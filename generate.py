#!/usr/bin/env python3

import json
import os
from pathlib import Path
import shutil
import subprocess
from typing import Dict, List
from zlib import adler32


COUNTRIES = [
    'gb',
    'us'
]

SWAPS = {
    'flip': [
        ['E', 'D'],
        ['R', 'F'],
        ['T', 'G'],
        ['U', 'J'],
        ['I', 'K'],
        ['O', 'L'],
        ['P', ';']
    ]
}
SWAPS['flip-spin'] = [s for s in SWAPS['flip'] if s[0] not in ('O', 'P')] + [ ['O', 'L', ';', 'P'] ]
SWAPS['flip-twist'] = [s for s in SWAPS['flip'] if s[0] not in ('U', )] + [ ['J', 'N'] ]
SWAPS['flip-spin-twist'] = [s for s in SWAPS['flip'] if s[0] not in ('O', 'P', 'U')] + [ ['O', 'L', ';', 'P'], ['J', 'N'] ]


def js(x) -> str:
    return json.dumps(x, ensure_ascii=False)


def format(keymap: Dict) -> str:
    # we could just use json.dumps() but this matches klfc's json format
    shiftlevels = keymap['shiftlevels']
    keys = keymap['keys']
    shiftlevels_str = '[ ' + ', '.join(js(s) for s in shiftlevels)  + ' ]'
    keys_strs = ['    { "pos": ' + js(k["pos"]) + ', "letters": [ ' + ', '.join([js(l) for l in k["letters"]]) + ' ] }' for k in keys]
    keys_str = ',\n'.join(keys_strs)
    lines = [
        '{',
        '  "shiftlevels": ' + shiftlevels_str + ',',
        '  "keys": [',
        keys_str,
        '  ]',
        '}'
    ]
    return '\n'.join(lines) + '\n'


def gen_json_text(json_text: str, move_list: List[str]) -> str:
    no_comments = '\n'.join([l.partition('//')[0] for l in json_text.splitlines()])
    keymap = json.loads(no_comments)
    keys = keymap['keys']
    keys_dict = {key['pos']: key['letters'] for key in keys}
    for move in move_list:
        keys_dict_copy = keys_dict.copy()
        for i in range(len(move)):
            next_i = (i + 1) % len(move)
            keys_dict[move[next_i]] = keys_dict_copy[move[i]]
    keymap['keys'] = [{'pos': k, 'letters': v} for k, v in keys_dict.items()]
    return format(keymap)


def run_klfc(filepath_move_root: str):
    os.mkdir(filepath_move_root)
    subprocess.run(['klfc', '--from-json', f'{filepath_move_root}.json', '-o', filepath_move_root])


def fix_macos_file(country: str, move_name: str):
    # see https://github.com/39aldo39/klfc/issues/42
    layout_name = f'qwerty-{move_name}_{country}'
    path = Path(f'{country}/{layout_name}/keylayout/custom.keylayout')

    # id should be between -32768 and -2 according to:
    # https://github.com/sillsdev/Ukelele/blob/bf60297399b33ce6be0bcb3a8eb656ffcc2a0e0c/Ukelele%20Cocoa/ScriptRanges.h#L14
    new_id = str(adler32(layout_name.encode('utf-8')) % -32768)

    text = path.read_text().replace('-1337', new_id)
    if country == 'us':
        text = text.replace('<key code="10"', '<key code="50"')
    path.write_text(text)


def gen(country: str):
    shutil.rmtree(country)
    os.mkdir(country)
    filepath_in = f'qwerty_{country}.json'  # QWERTY-Flip is based on QWERTY layout
    for move_name, move_list in SWAPS.items():
        filepath_move_root = f'{country}/qwerty-{move_name}_{country}'
        filepath_out = f'{filepath_move_root}.json'
        with open(filepath_in) as file_in, open(filepath_out, 'w') as file_out:
            text_in = file_in.read()
            text_out = gen_json_text(text_in, move_list)
            file_out.write(text_out)
        run_klfc(filepath_move_root)
        fix_macos_file(country, move_name)


def main():
    for country in COUNTRIES:
        gen(country)


if __name__ == '__main__':
    main()

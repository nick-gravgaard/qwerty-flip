#!/usr/bin/env python3

import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from random import randint
from typing import List

def escape_special_chars(xml_string: str) -> str:
    return (xml_string.replace("&", "&amp;"))

def unescape_special_chars(xml_string: str) -> str:
    return (xml_string.replace("&amp;", "&"))

def set_unique_id(tree: ET.ElementTree, name: str) -> ET.ElementTree:
    root = tree.getroot()
    id = randint(-32768, -2)
    root.set('id', str(id))
    root.set('name', name)
    return tree

def prepare_xml(filepath: str) -> tuple[str, str, List[str]]:
    with open(filepath, 'r') as file:
        xml_string = file.read()
        xml_string = escape_special_chars(xml_string)
    
    with open(filepath, 'w') as file:
        file.write(xml_string)

    with open(filepath, 'r') as file:
        lines = file.readlines()
        xml_declaration = lines[0]
        doctype = lines[1]
        comments = []
        index = 2
        while not lines[index].startswith('-->'):
            comments.append(lines[index])
            index += 1
        comments.append(lines[index])

    return xml_declaration, doctype, comments

def fix_ansi_keymap(tree: ET.ElementTree) -> ET.Element:
    root = tree.getroot()
    keymaps = root.findall('.//keyMapSet/keyMap')
    
    key = ET.Element('key')
    key.set('code', '50')
    key.set('output', '`')
    keymaps[0].append(key)

    key = ET.Element('key')
    key.set('code', '50')
    key.set('output', '~')
    keymaps[1].append(key)

    return root

def pretty_print_xml(root: ET.Element) -> str:
    xml_string = ET.tostring(root, encoding='unicode', xml_declaration=False)
    parsed = minidom.parseString(xml_string)
    pretty_string = parsed.toprettyxml(indent='  ')
    pretty_string = "\n".join([line for line in pretty_string.split("\n")[1:] if line.strip()])
    pretty_string = unescape_special_chars(pretty_string)
    return pretty_string

def macos_fix():
    org_filepath  = 'us/qwerty-flip_us/keylayout/custom.keylayout'
    iso_filepath  = 'us/qwerty-flip_us/keylayout/custom_iso.keylayout'
    ansi_filepath = 'us/qwerty-flip_us/keylayout/custom_ansi.keylayout'
    os.rename(org_filepath, iso_filepath)
    os.system(f'cp {iso_filepath} {ansi_filepath}')

    xml_declaration, doctype, comments = prepare_xml(iso_filepath)
    prepare_xml(ansi_filepath)
    
    iso_tree = set_unique_id(ET.parse(iso_filepath), 'Custom Keyboard Layout (ISO)')
    ansi_tree = set_unique_id(ET.parse(ansi_filepath), 'Custom Keyboard Layout (ANSI)')

    ansi_root = fix_ansi_keymap(ansi_tree)
    
    iso_pretty_string = pretty_print_xml(iso_tree.getroot())
    ansi_pretty_string = pretty_print_xml(ansi_root)

    complete_xml_string_iso = xml_declaration + doctype + ''.join(comments) + iso_pretty_string
    complete_xml_string_ansi = xml_declaration + doctype + ''.join(comments) + ansi_pretty_string
    
    with open(iso_filepath, 'w') as file:
        file.write(complete_xml_string_iso)

    with open(ansi_filepath, 'w') as file:
        file.write(complete_xml_string_ansi)

def main():
    macos_fix()

if __name__ == '__main__':
    main()
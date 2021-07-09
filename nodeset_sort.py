#!/usr/bin/env python3

import argparse
from lxml import etree
import pdb

def sortchildrenby(parent, attr):
    parent[:] = sorted(parent, key=lambda child: child.get(attr))

def sortchildrenbytext(parent):
    parent[:] = sorted(parent, key=lambda child: child.text)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')

    args = parser.parse_args()

    tree = etree.parse(args.input)


    root = tree.getroot()

    sortchildrenby(root, 'NodeId')

    references = root.findall('.//{http://opcfoundation.org/UA/2011/03/UANodeSet.xsd}References')
    for _ in references:
        sortchildrenbytext(_)

    tree.write(args.output, encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":
    main()

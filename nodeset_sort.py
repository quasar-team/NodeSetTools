#!/usr/bin/env python3

import argparse
from lxml import etree

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')

    args = parser.parse_args()

    tree = etree.parse(args.input)

    def sortchildrenby(parent, attr):
        parent[:] = sorted(parent, key=lambda child: child.get(attr))

    sortchildrenby(tree.getroot(), 'NodeId')

    tree.write(args.output, encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":
    main()

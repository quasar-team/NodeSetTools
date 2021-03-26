#!/usr/bin/env python3

from lxml import etree
import argparse
import pdb
import sys

NAMESPACES = {'x':'http://opcfoundation.org/UA/2011/03/UANodeSet.xsd'}

def etree_from_filename(fn):
    file = open(fn, 'r', encoding='utf-8')
    return etree.parse(file)

def nodeid_scan(entity_type, reference_tree, test_tree):
    """entity_type to be anything that has NodeId, so any descendant of UANode, e.g. UAVariable, UAObject..."""
    any_failure = False
    for ref_entity in reference_tree.xpath(f'x:{entity_type}', namespaces=NAMESPACES):
        ref_nodeid = ref_entity.attrib["NodeId"]
        #print(f'At: {ref_nodeid}')
        # get the object at test.
        xpath_expr = f"x:{entity_type}[@NodeId='{ref_nodeid}']"
        q = test_tree.xpath(xpath_expr, namespaces=NAMESPACES)
        if len(q) != 1:
            print(f'Error: entity missing in test_tree. Type: {entity_type}, NodeId: {ref_nodeid}')
            any_failure = True
    return any_failure


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("reference")
    parser.add_argument("test")

    args = parser.parse_args()
    print(args.reference)

    reference_tree = etree_from_filename(args.reference)
    test_tree = etree_from_filename(args.test)

    any_failure = False
    
    NodeIdEntities = ['UAObject', 'UAVariable']
    for entity_type in NodeIdEntities:
        fail = nodeid_scan(entity_type, reference_tree, test_tree)
        any_failure = any_failure or fail

    if any_failure:
        sys.exit(1)


if __name__ == "__main__":
    main()
